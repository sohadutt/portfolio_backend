# Portfolio Backend

Django REST Framework backend for a portfolio platform with JWT auth, OTP-based verification, multi-portfolio publishing, public share-token access, contact-form intake, dashboard submission management, and background jobs powered by Celery.

## What This Project Does

This API lets a user:

- register and log in with email/password
- verify their account with OTP
- manage profile data and profile pictures
- publish one or more portfolio variants
- expose portfolios publicly through a share token
- receive contact-form submissions from public portfolio pages
- review, reorder, prioritize, and dismiss submissions from a dashboard

The codebase is built around one Django app, [`portfolio_form`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form), and one Django project config, [`config`](/Users/ssohadutt/developement/portfolio_backend/backend/config).

## Stack

- Python 3.14+
- Django 6
- Django REST Framework
- Simple JWT
- PostgreSQL
- Redis
- Celery
- Pillow + `pillow-heif` for image processing
- Vercel Blob for profile image storage
- `uv` for dependency management

Project metadata and dependencies live in [`pyproject.toml`](/Users/ssohadutt/developement/portfolio_backend/pyproject.toml).

## Repository Layout

```text
.
├── backend/
│   ├── config/                  # Django settings, URLs, WSGI/ASGI, Celery config
│   ├── manage.py                # Django management entrypoint
│   └── portfolio_form/          # Main app: models, serializers, views, tasks, tests
├── Render.yml                   # Render deployment definition
├── start.sh                     # Combined migration + worker + app startup script
├── pyproject.toml               # Project metadata and dependencies
└── README.md
```

## Core Domain Model

### User

Custom auth model extending `AbstractUser` with:

- email as the primary login identifier
- verification state via `is_verified`
- account tier: `FREE`, `PRO`, `PREMIUM`
- theme mode selection
- share-token controls for public portfolio access
- optional profile image URL

Defined in [`models.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/models.py).

### PortfolioSettings

Each user can own one or more portfolio records, identified by `order_index`.

Each portfolio stores:

- personal information
- hero content
- about content
- enabled/disabled state
- tier snapshot

Related ordered child models hold sections such as:

- `HeroMetric`
- `SkillGroup`
- `Project`
- `Experience`
- `ShowcaseCategory`
- `FeaturedModule`
- `Link`

### ContactFormSubmission

Stores public contact-form messages associated with an owner and optionally a portfolio. Submissions support:

- priority levels
- dashboard ordering through `display_index`
- dismiss state
- sender metadata and IP capture

## Tier Rules

The code enforces feature limits for non-paying users:

- free-tier users can only maintain one portfolio
- most portfolio section arrays are limited to 3 items
- navigation/footer/contact/status link groups are limited to 5 items

These rules are enforced in [`models.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/models.py) and [`serializers.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/serializers.py).

## Public API Shape

All routes are mounted under `/api/`.

### Authentication

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/otp/request/`
- `POST /api/auth/otp/verify/`
- `POST /api/auth/refresh/`
- `POST /api/auth/logout/`
- `GET /api/csrf/`

### Profile

- `GET /api/profile/`
- `PATCH /api/profile/update/`
- `PATCH /api/profile/share-toggle/`
- `GET /api/profile/get-token/`

### Public portfolio reads

- `GET /api/portfolio/default/`
- `GET /api/portfolio/default/<order_index>/`
- `GET /api/portfolio/shared/<share_token>/`
- `GET /api/portfolio/shared/<share_token>/<order_index>/`

### Authenticated portfolio writes

- `POST /api/portfolio/submit/<order_index>/`
- `PATCH /api/portfolio/update/<order_index>/`
- `PATCH /api/dashboard/portfolios/<order_index>/toggle/`
- `GET /api/dashboard/portfolios/all/`

### Public contact-form submission

- `POST /api/forms/submit/default/<order_index>/`
- `POST /api/forms/submit/shared/<share_token>/`

### Dashboard submission management

- `GET /api/dashboard/submissions/view/`
- `PATCH /api/dashboard/submissions/update/<form_id>/`
- `POST /api/dashboard/submissions/reorder/`

### Cron-style triggers

- `GET|POST /api/cron/cleanup/`
- `GET|POST /api/cron/urgent-notifications/`

Full route definitions are in [`urls.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/urls.py).

## Portfolio Payload Contract

The create/update portfolio endpoints expect a nested JSON payload with these top-level keys:

- `personalInfo`
- `navigationLinks`
- `heroContent`
- `heroMetrics`
- `aboutContent`
- `skillGroups`
- `projects`
- `experience`
- `showcaseCategories`
- `featuredModules`
- `contactMethods`
- `footerLinks`
- `statusPills`

Validation and persistence are handled in [`serializers.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/serializers.py). Public responses are assembled in [`views.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/views.py).

## Background Jobs

Celery tasks currently support:

- sending OTP emails
- deleting stale unverified users
- sending daily urgent-submission digests

Task implementations are in [`tasks.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/tasks.py), and Celery app setup is in [`celery.py`](/Users/ssohadutt/developement/portfolio_backend/backend/config/celery.py).

## Contact Form Protections

The public contact form is rate limited by IP using Django cache.

Configurable settings:

- `CONTACT_FORM_RATE_LIMIT_MAX_REQUESTS`
- `CONTACT_FORM_RATE_LIMIT_WINDOW_SECONDS`
- `CONTACT_FORM_BLOCK_SECONDS`

Current default behavior:

- 10 requests allowed
- measured over 300 seconds
- blocked for 24 hours after limit exhaustion

## Image Upload Behavior

Profile image uploads are accepted through `PATCH /api/profile/update/` and processed before storage:

- HEIC files are supported
- images are resized down to a max of 1000x1000
- uploads are converted to WebP
- old images are deleted from Vercel Blob when replaced

Compression logic lives in [`utils.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/utils.py).

## Environment Variables

The application loads environment variables from `.env` using `python-dotenv`.

### Required for a realistic local setup

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

PG_NAME=postgres
PG_USER=postgres
PG_PASSWORD=postgres
PG_HOST=localhost
PG_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@example.com

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

CRON_SECRET_KEY=replace-this-with-a-long-random-string

CONTACT_FORM_RATE_LIMIT_MAX_REQUESTS=10
CONTACT_FORM_RATE_LIMIT_WINDOW_SECONDS=300
CONTACT_FORM_BLOCK_SECONDS=86400
```

### Also needed depending on enabled features

- Vercel Blob credentials for profile image upload
- production-safe host/origin values for `ALLOWED_HOSTS`, CORS, and CSRF configuration

The environment lookups are defined in [`settings.py`](/Users/ssohadutt/developement/portfolio_backend/backend/config/settings.py).

## Local Development

### Prerequisites

- Python 3.14+
- PostgreSQL running locally
- Redis running locally
- `uv` installed

### Install dependencies

From the repository root:

```bash
uv sync
```

### Run migrations

```bash
uv run python3 backend/manage.py migrate
```

### Create a superuser

```bash
uv run python3 backend/manage.py createsuperuser
```

### Start the Django API

```bash
uv run python3 backend/manage.py runserver
```

### Start Celery in a second terminal

```bash
uv run celery -A backend.config.celery worker --loglevel=info
```

If you want OTP emails and urgent-digest jobs to behave like production, Redis and the Celery worker need to be running.

## Deployment Notes

This repository includes a [`Render.yml`](/Users/ssohadutt/developement/portfolio_backend/Render.yml) that provisions:

- one Python web service
- one Redis service

The included [`start.sh`](/Users/ssohadutt/developement/portfolio_backend/start.sh) is intended to:

- apply migrations
- start a Celery worker
- start Gunicorn

Before production deployment, verify:

- correct working directory assumptions for `manage.py`
- correct Gunicorn app import path for your deployment root
- production `ALLOWED_HOSTS`
- production CORS and CSRF origins
- secure email credentials
- Vercel Blob credentials

## Useful Management Commands

Custom commands available under [`management/commands`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/management/commands):

- `purge_unverified`: interactive cleanup of old unverified users
- `set_user_one <username>`: reassign a chosen user to primary key `1`
- `change_share enable|disable|regenerate`: bulk share-token maintenance

## Testing

There is an existing test module at [`tests.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/tests.py).

Run tests with:

```bash
uv run python3 backend/manage.py test
```

If you switch to `pytest`, make sure the dependency is installed first; it is not declared in [`pyproject.toml`](/Users/ssohadutt/developement/portfolio_backend/pyproject.toml).

## Important Implementation Notes

- The default public portfolio endpoint resolves user `id=1` first, then falls back to the first user in the database.
- Share-token portfolio access only works when `enable_share_token=True`.
- Profile updates accept JSON and multipart form data.
- OTPs are cached server-side and expire quickly.
- Unverified-user cleanup can be triggered either by Celery task usage or by the protected cron endpoint.
- Redis is used for Celery; contact-form rate limiting currently uses Django local-memory cache unless you change the cache backend.

## Known Gaps To Keep In Mind

- CORS and CSRF allowed origins are currently hard-coded for local development in [`settings.py`](/Users/ssohadutt/developement/portfolio_backend/backend/config/settings.py).
- The project depends on several external services, but not all provider-specific credential names are documented in code.
- Some tests appear older than the current API surface, so treat the existing test file as something to review alongside runtime verification.

## Entry Points

- Root URL `/` redirects to Django admin.
- Django admin is served at `/admin/`.
- API routes are mounted at `/api/`.

Project URL configuration is in [`config/urls.py`](/Users/ssohadutt/developement/portfolio_backend/backend/config/urls.py).
