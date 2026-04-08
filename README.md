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
- hero actions, focus, badges, and highlights
- about content
- section copy and page copy
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

## API Inputs And Outputs

### General notes

- Authenticated routes require `Authorization: Bearer <access_token>`.
- `PATCH /api/profile/update/` accepts either JSON or `multipart/form-data`.
- `GET /api/dashboard/submissions/view/` can return paginated collections when DRF pagination is active.
- Portfolio write payloads for icon-bearing fields accept `icon` or `iconName`.
- Portfolio reads return the same nested document shape used for writes, with `icon` keys and `profilePicture` inside `personalInfo`.

### Authentication and security

`GET /api/csrf/`

- Accepts: no body.
- Returns:

```json
{
  "detail": "CSRF cookie set"
}
```

`POST /api/auth/register/`

- Accepts:

```json
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

- Returns:

```json
{
  "message": "Profile created. OTP sent to your email.",
  "data": {
    "user_id": 1,
    "email": "user@example.com"
  }
}
```

`POST /api/auth/login/`

- Accepts:

```json
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

- Returns:

```json
{
  "message": "Login successful",
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "username": "user",
    "enable_share_token": false,
    "share_token": "generated-share-token",
    "tokens": {
      "refresh": "jwt-refresh-token",
      "access": "jwt-access-token"
    }
  }
}
```

`POST /api/auth/otp/request/`

- Accepts:

```json
{
  "email": "user@example.com"
}
```

- Returns:

```json
{
  "message": "If an account exists, an OTP will be sent shortly."
}
```

`POST /api/auth/otp/verify/`

- Accepts:

```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

- Returns:

```json
{
  "message": "OTP verified.",
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "username": "user"
  },
  "tokens": {
    "refresh": "jwt-refresh-token",
    "access": "jwt-access-token"
  }
}
```

`POST /api/auth/refresh/`

- Accepts:

```json
{
  "refresh": "jwt-refresh-token"
}
```

- Returns:

```json
{
  "access": "new-jwt-access-token"
}
```

`POST /api/auth/logout/`

- Accepts:

```json
{
  "refresh": "jwt-refresh-token"
}
```

- Returns: Simple JWT blacklist response with `205 Reset Content` on success.

### Profile

`GET /api/profile/`

- Accepts: no body.
- Returns:

```json
{
  "user_id": 1,
  "email": "user@example.com",
  "username": "user",
  "first_name": "Soham",
  "last_name": "Dutta",
  "profile_picture": "https://...",
  "theme_mode": 0,
  "tier": 0,
  "portfolio_count": 1,
  "is_verified": true,
  "enable_share_token": false,
  "share_token": null
}
```

`PATCH /api/profile/update/`

- Accepts any subset of:

```json
{
  "first_name": "Soham",
  "last_name": "Dutta",
  "theme_mode": 0
}
```

- Also accepts `profile_picture` as a multipart file field.
- Returns:

```json
{
  "message": "Profile updated successfully.",
  "data": {
    "first_name": "Soham",
    "last_name": "Dutta",
    "theme_mode": 0,
    "profile_picture": "https://..."
  }
}
```

`PATCH /api/profile/share-toggle/`

- Accepts either no body to toggle automatically, or:

```json
{
  "enable_share_token": true
}
```

- Returns:

```json
{
  "enable_share_token": true,
  "share_token": "generated-share-token"
}
```

`GET /api/profile/get-token/`

- Accepts: no body.
- Returns:

```json
{
  "enable_share_token": true,
  "share_token": "generated-share-token"
}
```

### Portfolio write payload

`POST /api/portfolio/submit/<order_index>/`

- Accepts the full portfolio document:

```json
{
  "new_order_index": 1,
  "is_enabled": true,
  "personalInfo": {
    "name": "Soham Dutta",
    "shortName": "sohadutt",
    "title": "Full-stack Developer",
    "subtitle": "JavaScript, Python, Django, React",
    "location": "India",
    "email": "sohadutt@outlook.com",
    "github": "https://github.com/sohadutt",
    "linkedin": "https://linkedin.com/in/sohadutt",
    "profilePicture": "https://example.com/profile.webp"
  },
  "navigationLinks": [
    { "label": "About", "href": "#about" },
    { "label": "Projects", "href": "#projects" }
  ],
  "heroContent": {
    "eyebrow": "Soham Dutta",
    "title": "Backend-focused full-stack developer building reliable systems and polished frontend experiences.",
    "description": "I work across Django, Python automation, PostgreSQL, REST APIs, React, and Tailwind CSS."
  },
  "heroActions": {
    "primary": {
      "label": "View projects",
      "href": "#projects"
    },
    "secondary": {
      "label": "GitHub",
      "href": "https://github.com/sohadutt"
    }
  },
  "heroMetrics": [
    { "value": "2024", "label": "started backend and config automation work at Imagine.io" }
  ],
  "heroFocus": {
    "eyebrow": "Current focus",
    "title": "Automation + product delivery",
    "areas": [
      { "label": "Backend systems", "value": 78 }
    ]
  },
  "heroBadges": [
    { "label": "Full-stack" }
  ],
  "heroHighlights": [
    {
      "title": "Backend systems",
      "description": "Django, APIs, automation workflows and scalable backend logic."
    }
  ],
  "aboutContent": {
    "title": "A portfolio shaped around your actual engineering profile.",
    "description": "This version reflects backend automation, frontend delivery, and workflow thinking."
  },
  "skillGroups": [
    {
      "title": "Backend & APIs",
      "description": "Building Django services, safe admin tooling, and API-driven automation for production systems.",
      "items": ["Python", "Django", "REST APIs"]
    }
  ],
  "projects": [
    {
      "title": "Internal Config Management Tool",
      "eyebrow": "Backend automation",
      "description": "Developed Django management commands and Python API scripts for secure configuration management.",
      "stack": ["Django", "Python", "REST APIs"],
      "stat": "70% fewer routine config requests"
    }
  ],
  "experience": [
    {
      "period": "2024 - Present",
      "title": "Associate - Backend & Config Automation",
      "company": "Imagine.io | Delhi, India",
      "relation": "automation",
      "summary": "Designed Django management commands for controlled database updates.",
      "highlights": ["Controlled config changes through safe Django command flows."],
      "relatedComponents": ["Command", "Alert Dialog", "Data Table", "Toast"]
    }
  ],
  "showcaseCategories": [
    {
      "title": "Data & Forms",
      "icon": "Workflow",
      "relation": "automation",
      "preview": "Forms and data controls connect directly to the automation work.",
      "items": ["Command", "Data Table", "Alert Dialog"]
    }
  ],
  "featuredModules": [
    {
      "title": "Config automation",
      "icon": "Database",
      "relation": "automation",
      "body": "Highlights your backend work around Django management commands, data safety, and automation.",
      "details": "This state emphasizes data-heavy components and safer review patterns."
    }
  ],
  "contactMethods": [
    {
      "label": "Email",
      "value": "sohadutt@outlook.com",
      "href": "mailto:sohadutt@outlook.com",
      "icon": "Mail"
    }
  ],
  "footerLinks": [
    { "label": "GitHub", "href": "https://github.com/sohadutt" }
  ],
  "statusPills": [
    { "label": "Backend and config automation", "icon": "ArrowUpRight" }
  ],
  "sectionCopy": {
    "projects": {
      "eyebrow": "Projects",
      "title": "Selected work from configuration systems to frontend delivery.",
      "description": "These cards reflect secure configuration tooling, deployment reliability, and reusable UI work."
    },
    "experience": {
      "eyebrow": "Experience",
      "title": "Experience across backend automation, frontend delivery, and production workflows.",
      "description": "Hover a role to expand the story and related component direction."
    },
    "components": {
      "eyebrow": "UI System",
      "title": "Related components now respond to the same hover story.",
      "description": "The page feels connected instead of sectioned off."
    },
    "contact": {
      "eyebrow": "Contact",
      "title": "Open to roles and collaborations where backend reliability meets strong product thinking.",
      "description": "Reach out for backend automation, Django and API work, or frontend implementation."
    }
  },
  "pageCopy": {
    "loadingTitle": "Loading portfolio",
    "loadingDescription": "Preparing the showcase experience."
  }
}
```

- Returns:

```json
{
  "message": "Portfolio saved.",
  "data": {
    "new_order_index": 1,
    "is_enabled": true,
    "tier": 0,
    "themeMode": 0,
    "personalInfo": {
      "name": "Soham Dutta",
      "shortName": "sohadutt",
      "title": "Full-stack Developer",
      "subtitle": "JavaScript, Python, Django, React",
      "location": "India",
      "email": "sohadutt@outlook.com",
      "github": "https://github.com/sohadutt",
      "linkedin": "https://linkedin.com/in/sohadutt",
      "profilePicture": "https://..."
    },
    "heroContent": {
      "eyebrow": "Soham Dutta",
      "title": "Backend-focused full-stack developer building reliable systems and polished frontend experiences.",
      "description": "I work across Django, Python automation, PostgreSQL, REST APIs, React, and Tailwind CSS."
    },
    "heroActions": {
      "primary": {
        "label": "View projects",
        "href": "#projects"
      },
      "secondary": {
        "label": "GitHub",
        "href": "https://github.com/sohadutt"
      }
    },
    "heroMetrics": [
      { "value": "2024", "label": "started backend and config automation work at Imagine.io" }
    ],
    "heroFocus": {
      "eyebrow": "Current focus",
      "title": "Automation + product delivery",
      "areas": [
        { "label": "Backend systems", "value": 78 }
      ]
    },
    "heroBadges": [
      { "label": "Full-stack" }
    ],
    "heroHighlights": [
      {
        "title": "Backend systems",
        "description": "Django, APIs, automation workflows and scalable backend logic."
      }
    ],
    "aboutContent": {
      "title": "A portfolio shaped around your actual engineering profile.",
      "description": "This version reflects backend automation, frontend delivery, and workflow thinking."
    },
    "skillGroups": [],
    "projects": [],
    "experience": [],
    "showcaseCategories": [],
    "featuredModules": [],
    "contactMethods": [
      {
        "label": "Email",
        "value": "sohadutt@outlook.com",
        "href": "mailto:sohadutt@outlook.com",
        "icon": "Mail"
      }
    ],
    "navigationLinks": [
      { "label": "About", "href": "#about" },
      { "label": "Projects", "href": "#projects" }
    ],
    "footerLinks": [
      { "label": "GitHub", "href": "https://github.com/sohadutt" }
    ],
    "statusPills": [
      { "label": "Backend and config automation", "icon": "ArrowUpRight" }
    ],
    "sectionCopy": {
      "projects": {
        "eyebrow": "Projects",
        "title": "Selected work from configuration systems to frontend delivery.",
        "description": "These cards reflect secure configuration tooling, deployment reliability, and reusable UI work."
      }
    },
    "pageCopy": {
      "loadingTitle": "Loading portfolio",
      "loadingDescription": "Preparing the showcase experience."
    }
  }
}
```

`PATCH /api/portfolio/update/<order_index>/`

- Accepts either the same full payload as `submit`, a partial nested portfolio payload, or a settings-only payload:

```json
{
  "new_order_index": 2,
  "is_enabled": true
}
```

- Returns:

```json
{
  "message": "Portfolio updated.",
  "data": {
    "...": "same serialized portfolio shape as submit"
  }
}
```

or, for settings-only updates:

```json
{
  "message": "Portfolio settings updated.",
  "data": {
    "...": "same serialized portfolio shape as submit"
  }
}
```

Validation and persistence are handled in [`serializers.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/serializers.py). Public responses are assembled in [`views.py`](/Users/ssohadutt/developement/portfolio_backend/backend/portfolio_form/views.py).

### Public portfolio reads

`GET /api/portfolio/default/`
`GET /api/portfolio/default/<order_index>/`
`GET /api/portfolio/shared/<share_token>/`
`GET /api/portfolio/shared/<share_token>/<order_index>/`

- Accepts: no body.
- Returns the same serialized portfolio shape shown above under `data`, without the outer `message` wrapper.

### Public contact-form submission

`POST /api/forms/submit/default/<order_index>/`
`POST /api/forms/submit/shared/<share_token>/`

- Accepts:

```json
{
  "name": "Visitor Name",
  "email": "visitor@example.com",
  "phone": "+91-9999999999",
  "message": "I would like to work together.",
  "for_work": true,
  "priority": 2
}
```

- Returns:

```json
{
  "message": "Message sent."
}
```

- Priority values are `0=Low`, `1=Medium`, `2=High`, `3=Urgent`.

### Dashboard submission management

`GET /api/dashboard/submissions/view/`

- Accepts: no body.
- Returns a paginated DRF response when pagination is active:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 10,
      "display_index": 1,
      "owner_username": "user",
      "owner_user_id": 1,
      "portfolio_id": 3,
      "name": "Visitor Name",
      "email": "visitor@example.com",
      "phone": "+91-9999999999",
      "message": "I would like to work together.",
      "for_work": true,
      "priority": 2,
      "priority_label": "High",
      "is_dismissed": false,
      "submitted_at": "2026-04-09T10:00:00Z"
    }
  ]
}
```

`PATCH /api/dashboard/submissions/update/<form_id>/`

- Accepts any subset of:

```json
{
  "is_dismissed": true,
  "priority": 3,
  "display_index": 1
}
```

- Returns:

```json
{
  "message": "Updated.",
  "data": {
    "id": 10,
    "display_index": 1,
    "owner_username": "user",
    "owner_user_id": 1,
    "portfolio_id": 3,
    "name": "Visitor Name",
    "email": "visitor@example.com",
    "phone": "+91-9999999999",
    "message": "I would like to work together.",
    "for_work": true,
    "priority": 3,
    "priority_label": "Urgent",
    "is_dismissed": true,
    "submitted_at": "2026-04-09T10:00:00Z"
  }
}
```

`POST /api/dashboard/submissions/reorder/`

- Accepts:

```json
{
  "order": [10, 8, 5]
}
```

- Returns:

```json
{
  "submissions": [
    {
      "id": 10,
      "display_index": 1,
      "owner_username": "user",
      "owner_user_id": 1,
      "portfolio_id": 3,
      "name": "Visitor Name",
      "email": "visitor@example.com",
      "phone": "+91-9999999999",
      "message": "I would like to work together.",
      "for_work": true,
      "priority": 2,
      "priority_label": "High",
      "is_dismissed": false,
      "submitted_at": "2026-04-09T10:00:00Z"
    }
  ]
}
```

### Dashboard portfolio management

`PATCH /api/dashboard/portfolios/<order_index>/toggle/`

- Accepts: no body.
- Returns:

```json
{
  "message": "Portfolio 1 is now enabled.",
  "is_enabled": true
}
```

`GET /api/dashboard/portfolios/all/`

- Accepts: no body.
- Returns:

```json
{
  "message": "Portfolios retrieved successfully.",
  "portfolios": [
    {
      "order_index": 1,
      "name": "Soham Dutta",
      "title": "Backend Developer",
      "is_enabled": true,
      "theme_mode": 0
    }
  ]
}
```

### Cron-style triggers

`GET|POST /api/cron/cleanup/`
`GET|POST /api/cron/urgent-notifications/`

- Accepts either the `X-Cron-Secret` header or `?secret=<CRON_SECRET_KEY>`.
- Returns:

```json
{
  "message": "Cleanup task executed successfully.",
  "details": {}
}
```

or:

```json
{
  "message": "Urgent notifications processed.",
  "details": {}
}
```

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
