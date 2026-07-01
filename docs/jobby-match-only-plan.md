# Jobby Match-Only Refactor Plan

## Goal

Make job enrichment reusable across portfolios. A job's extracted tags and other stable AI metadata should live on the `Job` record once, while each portfolio only gets its own `match_score`.

After raw site JSON files are created and jobs are in the database, a `--match-only` command flag or `match_only=true` view query should run a cheaper AI prompt that returns only:

```json
[
  {"job_id": "358335", "match_score": 65.0}
]
```

This keeps the response easy to map back to existing jobs and allows larger batches because the prompt no longer sends full job descriptions or asks for tags again.

## Current State

- `backend/jobby/models.py`
  - `Job` stores raw job identity/display fields only.
  - `PortfolioJobMatch` stores both `match_score` and `tags`, so tags are duplicated per portfolio.
- `backend/jobby/jobby.py`
  - `MAIN_PROCESS_PROMPT` asks Gemini for both `match_score` and `tags`.
  - `JobManager.process_jobs()` skips jobs already present in `{site}_matches_output.json`.
  - `DatabaseUpdater.save_batch_to_db()` saves raw jobs to `Job` and AI output to `PortfolioJobMatch`.
- `backend/portfolio_form/tasks.py`
  - `run_job_pipeline()` always uses one processing path when `run_processor=True`.
  - Batch size is currently `10`.
- `backend/jobby/management/commands/jobby_run.py`
  - Supports `--no-scrape`, `--no-process`, and `--async`, but not `--match-only`.
- `backend/jobby/views.py`
  - `SignalStart` supports `scraper` and `processor` query params, but not `match_only`.

## Model Changes

Move stable AI job metadata onto `Job`:

```python
class Job(models.Model):
    ...
    tags = models.JSONField(default=list, help_text="Stable AI-generated job tags")
    ai_metadata = models.JSONField(default=dict, blank=True, help_text="Stable AI-generated job metadata")
    ai_processed_at = models.DateTimeField(blank=True, null=True)
```

Keep portfolio-specific matching on `PortfolioJobMatch`:

```python
class PortfolioJobMatch(models.Model):
    ...
    match_score = models.FloatField(help_text="Match percentage from 0 to 100")
```

`PortfolioJobMatch.tags` should be removed after a migration copies any existing match tags into `Job.tags` where possible. If backward compatibility is needed for the frontend, expose `tags` from `job.tags` in the serializer instead of storing it on the pivot.

## Migration Plan

1. Add `Job.tags`, `Job.ai_metadata`, and `Job.ai_processed_at`.
2. Data migration:
   - For each `PortfolioJobMatch` that has tags, copy tags to the related `Job` if `Job.tags` is empty.
   - If multiple portfolios have different tag lists for the same job, prefer the longest non-empty list for now because tags were previously portfolio-contaminated but usually describe the job.
3. Remove `PortfolioJobMatch.tags`.
4. Update serializers and API responses so matched jobs still show tags through the nested `job`.

## Pipeline Changes

Split the AI pipeline into two modes.

### Full Processing Mode

Used when new raw jobs need stable enrichment.

- Input: raw jobs from `{site}_jobs_output.json`.
- Prompt asks for job-level metadata only, not portfolio scoring.
- Output shape:

```json
[
  {
    "job_id": "358335",
    "tags": ["Backend Development", "API Integration", "SQL"],
    "ai_metadata": {
      "role_family": "Software Engineering",
      "seniority": "Consultant",
      "primary_skills": ["Python", "SQL", "API Integration"]
    }
  }
]
```

- Save output to something like `{site}_job_analysis_output.json`.
- Save raw job fields plus tags/metadata to `Job`.
- This mode can still use smaller batches because it may send long descriptions.

### Match-Only Mode

Used for another portfolio after jobs are already enriched.

- Input: portfolio summary plus compact job records from the database.
- Job payload should include only:
  - `job_id`
  - `title`
  - `company`
  - `location`
  - `tags`
  - compact `ai_metadata`
- Prompt asks for `job_id` and `match_score` only.
- Output shape:

```json
[
  {"job_id": "358335", "match_score": 65.0}
]
```

- Save only `PortfolioJobMatch.match_score`.
- Do not update `Job.tags` or `Job.ai_metadata`.
- Batch size can be increased, for example from `10` to `50` or `100`, because each job payload is much smaller.

## Command Changes

Update `backend/jobby/management/commands/jobby_run.py`:

- Add `--match-only`.
- When `--match-only` is set:
  - Do not scrape.
  - Do not run full enrichment.
  - Require existing enriched `Job` rows for the site.
  - Run scoring only for the selected portfolio.
- Suggested usage:

```bash
uv run python manage.py jobby_run --site deloitte --portfolio 2 --match-only
```

The command should pass `match_only=True` into `run_job_pipeline()`.

## View Changes

Update `backend/jobby/views.py`:

- Read `match_only=true` from `SignalStart`.
- Pass it into `run_job_pipeline.delay(...)`.
- Example:

```http
POST /jobs/signals/start/deloitte/?order_index=2&match_only=true
```

When `match_only=true`, the view should ignore `scraper=true` unless we explicitly decide to reject conflicting query params with a `400`.

## Task Signature

Update `run_job_pipeline()` in `backend/portfolio_form/tasks.py` from:

```python
def run_job_pipeline(self, site_name, run_scraper, run_processor, portfolio_id):
```

to:

```python
def run_job_pipeline(self, site_name, run_scraper, run_processor, portfolio_id, match_only=False):
```

Behavior:

- `match_only=False`: current scrape/process behavior, but full processing should enrich `Job` instead of writing portfolio tags.
- `match_only=True`: skip scraper and full processor, load enriched jobs from DB, and run score-only batches.

## Prompt Changes

Keep two separate prompts:

- `JOB_ENRICHMENT_PROMPT`
  - No portfolio.
  - Returns `job_id`, `tags`, and optional stable metadata.
- `MATCH_ONLY_PROMPT`
  - Includes portfolio.
  - Includes compact enriched job list.
  - Returns only `job_id` and `match_score`.

The match-only prompt should explicitly say not to return tags, explanations, markdown, or changed IDs.

## Serializer Changes

Update `JobSerializer` to include:

- `tags`
- `ai_metadata` if useful for the frontend, or omit `ai_metadata` if it should stay internal.

Update `PortfolioJobMatchSerializer`:

- Remove stored `tags`.
- Either rely on nested `job.tags`, or add a read-only `tags = serializers.JSONField(source="job.tags")` compatibility field.

## Validation and Edge Cases

- If `match_only=True` and no enriched jobs exist for the site, return a clear error/result like:

```json
{"status": "error", "message": "No enriched jobs found for deloitte. Run full processing first."}
```

- If some jobs have no tags yet, either:
  - exclude them from match-only, or
  - include title/location only with a lower-confidence score.
- Keep `platform_name + platform_job_id` as the stable mapping key.
- Normalize all AI `job_id` values to strings before lookup.
- Clamp `match_score` to `0..100` before saving.

## Tests To Add

- Model/data migration test for copying `PortfolioJobMatch.tags` to `Job.tags`.
- Unit test for match-only DB saving:
  - existing `Job(tags=[...])`
  - AI returns only `job_id` and `match_score`
  - `PortfolioJobMatch` is created/updated without modifying job tags.
- Command test for `--match-only` passing `match_only=True`.
- View test for `match_only=true` passing through to the Celery task.
- Serializer test proving matched responses still expose tags through the job payload.

## Implementation Order

1. Add schema fields and migration.
2. Update serializers to read tags from `Job`.
3. Split prompts and analyzer methods.
4. Split `DatabaseUpdater` into job-enrichment save and match-score save paths.
5. Add `JobManager.process_jobs()` full mode and `JobManager.process_match_only()` score mode.
6. Update Celery task signature and branching.
7. Add `--match-only` to the management command.
8. Add `match_only=true` support to the signal view.
9. Add focused tests.
10. Run migrations check and app tests.
