# Portfolio Backend

Django + Django REST Framework backend for a portfolio site with:

- email-based profile creation
- JWT login with refresh + access tokens
- one portfolio per user
- public portfolio reads
- public contact submissions for the default portfolio and shared portfolios
- authenticated dashboard access for submission management

All API routes are mounted under `/api/`.

## Stack

- Python `>=3.14`
- Django `6.0.3`
- Django REST Framework
- `djangorestframework-simplejwt`
- PostgreSQL

## Data Model

### User

Custom auth user fields used by this project:

- `email` is unique
- `username` is generated from the email prefix on signup
- `enable_share_token` gates token-based public routes
- `share_token` is auto-generated and unique

### PortfolioSettings

Each user can have exactly one portfolio record.

`PortfolioSettings.share_token` is derived from `owner.share_token`; the portfolio model does not store a separate token.

### Ordered portfolio content

These models are owner-scoped and ordered:

- `HeroMetric`
- `SkillGroup`
- `Project`
- `Experience`
- `ShowcaseCategory`
- `FeaturedModule`
- `Link`

`Link.type` is one of:

- `NAV`
- `FOOTER`
- `CONTACT`
- `STATUS`

### ContactFormSubmission

Public submissions are stored with:

- `owner`
- `portfolio` (nullable)
- `display_index`
- `priority`
- `is_dismissed`
- request IP when available

`display_index` auto-increments per owner and can be reordered later from the dashboard.

## Public Routing Rules

### Default public portfolio

`GET /api/portfolio`

The backend resolves the default owner like this:

1. User with `id=1`, if present
2. Otherwise the earliest user by `id`

If no users exist, the endpoint returns `404`.

### Shared public portfolio

`GET /api/portfolio/<share_token>`

This only works when the target user exists and `enable_share_token=true`. Otherwise it returns `404`.

### Public contact form

There are two public submission endpoints:

- `POST /api/forms/submit` submits to the default public portfolio owner
- `POST /api/forms/submit/<share_token>` submits to the shared owner resolved by token

For token-based submissions, the backend also requires `enable_share_token=true`.

## Auth Model

Protected routes use JWT Bearer auth.

Login returns:

- `temporary_token`: refresh token
- `bearer_token`: access token
- `token_type`: always `Bearer`

Use the access token like this:

```http
Authorization: Bearer <bearer_token>
```

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Configure PostgreSQL environment variables.
4. Run migrations.
5. Start the server.

Example:

```bash
pip install -e .
cd backend
python manage.py migrate
python manage.py runserver
```

Environment variables used by `backend/config/settings.py`:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `PG_NAME`
- `PG_USER`
- `PG_PASSWORD`
- `PG_HOST`
- `PG_PORT`

Defaults are development-oriented, but the database engine is PostgreSQL, so a reachable Postgres instance is still required unless you change settings.

## Request Rules

Write endpoints expect JSON:

```http
Content-Type: application/json
```

Example:

```json
{
  "email": "alice@example.com",
  "password": "testpass123"
}
```

## API Reference

### 1. CSRF cookie

`GET /api/csrf`

Auth required: no

Response:

```json
{
  "detail": "CSRF cookie set"
}
```

### 2. Create profile

`POST /api/profiles`

Auth required: no

Request:

```json
{
  "email": "alice@example.com",
  "password": "testpass123"
}
```

Response:

```json
{
  "message": "Profile created successfully",
  "data": {
    "user_id": 1,
    "email": "alice@example.com",
    "username": "alice",
    "enable_share_token": false,
    "share_token": "generated-user-share-token"
  }
}
```

Validation:

- `email` must be unique
- `password` minimum length is `8`

### 3. Login

`POST /api/auth/login`

Auth required: no

Request:

```json
{
  "email": "alice@example.com",
  "password": "testpass123"
}
```

Response:

```json
{
  "message": "Login successful",
  "data": {
    "user_id": 1,
    "email": "alice@example.com",
    "username": "alice",
    "enable_share_token": true,
    "share_token": "generated-user-share-token",
    "temporary_token": "jwt-refresh-token",
    "bearer_token": "jwt-access-token",
    "token_type": "Bearer"
  }
}
```

### 4. Refresh token

`POST /api/auth/refresh`

Auth required: no

Request:

```json
{
  "refresh": "<temporary_token>"
}
```

### 5. Logout

`POST /api/auth/logout`

Auth required: no

Request:

```json
{
  "refresh": "<temporary_token>"
}
```

### 6. Get public default portfolio

`GET /api/portfolio`

Auth required: no

Response shape is frontend-oriented and includes:

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

Example:

```json
{
  "personalInfo": {
    "name": "Alice Doe",
    "shortName": "AD",
    "title": "Full Stack Developer",
    "subtitle": "Building reliable products",
    "location": "Kolkata, India",
    "email": "alice@example.com",
    "github": "https://github.com/alice",
    "linkedin": "https://linkedin.com/in/alice"
  },
  "navigationLinks": [
    { "label": "About", "href": "#about" }
  ],
  "heroContent": {
    "eyebrow": "Available for work",
    "title": "I build products end to end.",
    "description": "Focused on thoughtful UX and maintainable systems."
  }
}
```

### 7. Get shared public portfolio

`GET /api/portfolio/<share_token>`

Auth required: no

If the token is invalid or disabled, returns `404`.

### 8. Create or replace authenticated portfolio

`POST /api/portfolio/submit`

Auth required: yes

Header:

```http
Authorization: Bearer <bearer_token>
```

Request body:

```json
{
  "personalInfo": {
    "name": "Alice Doe",
    "shortName": "AD",
    "title": "Full Stack Developer",
    "subtitle": "Building reliable products",
    "location": "Kolkata, India",
    "email": "alice@example.com",
    "github": "https://github.com/alice",
    "linkedin": "https://linkedin.com/in/alice"
  },
  "navigationLinks": [
    { "label": "About", "href": "#about" }
  ],
  "heroContent": {
    "eyebrow": "Available for work",
    "title": "I build products end to end.",
    "description": "Focused on thoughtful UX and maintainable systems."
  },
  "heroMetrics": [
    { "value": "3+", "label": "Years Experience" }
  ],
  "aboutContent": {
    "title": "About Me",
    "description": "I enjoy building dependable software."
  },
  "skillGroups": [
    {
      "title": "Backend",
      "description": "APIs and systems",
      "items": ["Django", "PostgreSQL"]
    }
  ],
  "projects": [
    {
      "title": "Portfolio Backend",
      "eyebrow": "Featured",
      "description": "A portfolio backend with nested content.",
      "stack": ["Django", "DRF"],
      "stat": "Live"
    }
  ],
  "experience": [
    {
      "period": "2024 - Present",
      "title": "Developer",
      "company": "Example Co",
      "relation": "Full-time",
      "summary": "Builds backend and frontend systems.",
      "highlights": ["Shipped APIs"],
      "relatedComponents": ["Portfolio", "Dashboard"]
    }
  ],
  "showcaseCategories": [
    {
      "title": "Web Apps",
      "icon": "Monitor",
      "relation": "Featured",
      "preview": "Modern product engineering work.",
      "items": ["Dashboards", "Portfolio Sites"]
    }
  ],
  "featuredModules": [
    {
      "title": "Case Studies",
      "icon": "Briefcase",
      "relation": "Selected Work",
      "body": "High-impact builds and experiments.",
      "details": "Backend systems, UX improvements, and launches."
    }
  ],
  "contactMethods": [
    {
      "label": "Email",
      "value": "alice@example.com",
      "href": "mailto:alice@example.com",
      "icon": "Mail"
    }
  ],
  "footerLinks": [
    { "label": "GitHub", "href": "https://github.com/alice" }
  ],
  "statusPills": [
    { "label": "Open to Work", "icon": "Sparkles" }
  ]
}
```

Behavior:

- creates the portfolio if it does not exist
- updates the portfolio if it already exists
- replaces all ordered child collections for that owner

### 9. Partially update authenticated portfolio

`POST /api/portfolio/update`

Auth required: yes

This route performs a partial update using the same payload shape as `/api/portfolio/submit`.

If the user has no existing portfolio, it returns `404`.

### 10. Get share status and token

`GET /api/profile/tokens`

Auth required: yes

Response:

```json
{
  "enable_share_token": true,
  "share_token": "generated-user-share-token"
}
```

### 11. Submit to the default public portfolio

`POST /api/forms/submit`

Auth required: no

This creates a `ContactFormSubmission` for the default public owner.

Request:

```json
{
  "name": "Visitor",
  "email": "visitor@example.com",
  "phone": "1234567890",
  "message": "Hello there",
  "for_work": true,
  "priority": 1
}
```

### 12. Submit to a shared public portfolio

`POST /api/forms/submit/<share_token>`

Auth required: no

Request:

```json
{
  "name": "Visitor",
  "email": "visitor@example.com",
  "phone": "1234567890",
  "message": "Hello Alice",
  "for_work": true,
  "priority": 1
}
```

Priority values:

- `0` = Low
- `1` = Medium
- `2` = High
- `3` = Urgent

Example success response:

```json
{
  "message": "Form submitted successfully",
  "data": {
    "id": 1,
    "display_index": 1,
    "owner": "alice",
    "owner_user_id": 1,
    "portfolio_id": 1,
    "name": "Visitor",
    "email": "visitor@example.com",
    "phone": "1234567890",
    "message": "Hello Alice",
    "for_work": true,
    "priority": 1,
    "priority_label": "Medium",
    "is_dismissed": false,
    "submitted_at": "2026-04-03T10:00:00+05:30"
  }
}
```

### 13. List dashboard submissions

`GET /api/forms/submissions`

Auth required: yes

Response:

```json
{
  "owner": "alice",
  "owner_user_id": 1,
  "submissions": []
}
```

### 14. Update one dashboard submission

`PATCH /api/forms/submissions/<form_id>`

Also supported:

`POST /api/forms/submissions/<form_id>`

Auth required: yes

Request can be partial:

```json
{
  "is_dismissed": true,
  "priority": 2,
  "display_index": 1
}
```

If `display_index` is provided, the backend reorders the owner's submission list.

### 15. Reorder dashboard submissions

`POST /api/forms/submissions/reorder`

Auth required: yes

Request:

```json
{
  "order": [3, 1, 2]
}
```

Rules:

- `order` must include each current submission exactly once
- the reorder happens within the authenticated owner only

## Common Errors

### Missing auth

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Unsupported media type

If a JSON-only endpoint receives form-encoded data:

```json
{
  "detail": "Unsupported media type \"multipart/form-data\" in request."
}
```

### Invalid JSON

```json
{
  "detail": "JSON parse error ..."
}
```

### Share token disabled or not found

Current behavior:

- returns `404`

This intentionally avoids revealing whether a disabled token belongs to a real user.

## Frontend Integration Notes

Default public site:

- `GET /api/portfolio`
- `POST /api/forms/submit`

Shared public site:

- `GET /api/portfolio/<share_token>`
- `POST /api/forms/submit/<share_token>`

Owner dashboard:

- `POST /api/auth/login`
- `GET /api/profile/tokens`
- `POST /api/portfolio/submit`
- `POST /api/portfolio/update`
- `GET /api/forms/submissions`
- `PATCH /api/forms/submissions/<form_id>`
- `POST /api/forms/submissions/reorder`
