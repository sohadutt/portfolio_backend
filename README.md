# Portfolio Backend

Django + Django REST Framework backend for a portfolio site with:

- user profile creation
- JWT login
- one portfolio per user
- public portfolio reads
- public form submission through a share token
- private dashboard submission management through Bearer auth

All API routes are mounted under `/api/`.

## Core Model

Each user has:

- one account
- one share token
- one share toggle: `enable_share_token`
- one portfolio settings record

Important rule:

- one user can have only one `PortfolioSettings`

The share token belongs to the `User`, not the portfolio. Public portfolio reads and public contact-form submissions both resolve through `User.share_token`.

## Auth Model

Dashboard access does not use any separate dashboard token.

Protected endpoints use JWT Bearer authentication.

Login returns:

- `temporary_token`: refresh token
- `bearer_token`: access token
- `token_type`: always `Bearer`

Use the access token like this:

```http
Authorization: Bearer <bearer_token>
```

## Public Portfolio Behavior

There are two public portfolio routes:

- `GET /api/portfolio/`
- `GET /api/portfolio/<share_token>/`

Behavior:

- `/api/portfolio/` returns the default public portfolio
- by current backend rule, the default portfolio is user `id=1`
- if user `id=1` does not exist, it falls back to the earliest user by `id`
- `/api/portfolio/<share_token>/` returns the portfolio for that shared user
- token-based portfolio reads only work when `enable_share_token=true`

This matches frontend routes like:

- `www.mysite.com/portfolio`
- `www.mysite.com/portfolio/<share_token>`

The frontend can map those routes to these backend endpoints:

- `www.mysite.com/portfolio` -> `GET /api/portfolio/`
- `www.mysite.com/portfolio/<share_token>` -> `GET /api/portfolio/<share_token>/`

## Public Form Behavior

The public contact form uses:

```text
POST /api/shares/<share_token>/submissions/
```

Behavior:

- the backend finds the user by `share_token`
- it requires `enable_share_token=true`
- it resolves that user's single `PortfolioSettings`
- it creates `ContactFormSubmission`
- the submission is saved under:
  - `owner = that user`
  - `portfolio = that user's portfolio`

If sharing is disabled, the endpoint returns `404`.

## Main Models

### User

Custom auth user with:

- `email`
- `enable_share_token`
- `share_token`
- `created_at`

Important behavior:

- `share_token` is generated automatically
- `enable_share_token` controls whether public share-token routes work

### PortfolioSettings

This is the single portfolio configuration for one user.

Important behavior:

- each owner can only have one `PortfolioSettings`
- it does not store its own share token
- `PortfolioSettings.share_token` is derived from `owner.share_token`

### ContactFormSubmission

Stores form submissions coming from the public share link.

Important fields:

- `owner`
- `portfolio`
- `name`
- `email`
- `phone`
- `message`
- `for_work`
- `priority`
- `is_dismissed`
- `display_index`

Important behavior:

- `display_index` auto-increments per owner
- submissions can be reordered
- reorder is stored per owner

### Ordered portfolio content models

These models are owner-scoped and ordered:

- `HeroMetric`
- `SkillGroup`
- `Project`
- `Experience`
- `ShowcaseCategory`
- `FeaturedModule`
- `Link`

They all inherit:

- `owner`
- `order`

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

Do not send Python-style payloads in raw JSON.

## API Reference

### 1. CSRF

`GET /api/csrf/`

Auth required: no

Response:

```json
{
  "detail": "CSRF cookie set"
}
```

### 2. Create profile

`POST /api/profiles/`

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
- `password` minimum length is 8

### 3. Login

`POST /api/auth/login/`

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

`POST /api/auth/refresh/`

Auth required: no

Request:

```json
{
  "refresh": "<temporary_token>"
}
```

### 5. Logout

`POST /api/auth/logout/`

Send the refresh token to blacklist it.

Request:

```json
{
  "refresh": "<temporary_token>"
}
```

### 6. Get public default portfolio

`GET /api/portfolio/`

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
    "name": "Soham Dutta",
    "shortName": "SD",
    "title": "Full-stack Developer",
    "subtitle": "JavaScript, Python, Django, React",
    "location": "India",
    "email": "sohadutt@outlook.com",
    "github": "https://github.com/sohadutt",
    "linkedin": "https://linkedin.com/in/sohadutt"
  },
  "navigationLinks": [
    { "label": "About", "href": "#about" }
  ],
  "heroContent": {
    "eyebrow": "Soham Dutta",
    "title": "Backend-focused full-stack developer building reliable systems and polished frontend experiences.",
    "description": "I work across Django, Python automation, PostgreSQL, REST APIs, React, and Tailwind CSS."
  }
}
```

### 7. Get shared public portfolio

`GET /api/portfolio/<share_token>/`

Auth required: no

Rules:

- finds the user by `share_token`
- requires `enable_share_token=true`
- returns that user's frontend-ready portfolio JSON

If the token is invalid or disabled, returns `404`.

### 8. Get share status and token

`GET /api/profile/tokens/`

Auth required: yes

Header:

```http
Authorization: Bearer <bearer_token>
```

Response:

```json
{
  "enable_share_token": true,
  "share_token": "generated-user-share-token"
}
```

### 9. Submit public form

`POST /api/shares/<share_token>/submissions/`

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

### 10. List dashboard submissions

`GET /api/submissions/`

Auth required: yes

Header:

```http
Authorization: Bearer <bearer_token>
```

### 11. Update one dashboard submission

`PATCH /api/submissions/<form_id>/`

Also supported:

`POST /api/submissions/<form_id>/`

Auth required: yes

Request can be partial:

```json
{
  "is_dismissed": true,
  "priority": 2,
  "display_index": 1
}
```

### 12. Reorder dashboard submissions

`POST /api/submissions/reorder/`

Auth required: yes

Request:

```json
{
  "order": [3, 1, 2]
}
```

Rules:

- `order` must be a list of submission ids
- it must include each of the owner's current submissions exactly once

## Common Errors

### Missing auth

Example:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Invalid JSON

Example:

```json
{
  "detail": "JSON parse error - Expecting value: line 2 column 30 (char 31)"
}
```

### Share token disabled or not found

Current behavior:

- returns `404`

This is intentional so disabled public share links do not reveal whether a token belongs to a real user.

## Recommended Frontend Usage

### Owner dashboard

1. Create profile.
2. Log in.
3. Store `bearer_token`.
4. Call `GET /api/profile/tokens/`.
5. Call `GET /api/submissions/`.
6. Update and reorder submissions with Bearer auth.

### Public portfolio

1. For the default page, call `GET /api/portfolio/`.
2. For a shared page, call `GET /api/portfolio/<share_token>/`.
3. Render the returned JSON directly into the frontend sections.
4. Submit the contact form to `POST /api/shares/<share_token>/submissions/`.
5. If the token is disabled, expect `404`.
