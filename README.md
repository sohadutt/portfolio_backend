# Portfolio Backend

This project is a Django + Django REST Framework backend for a portfolio site with:

- user profile creation
- JWT login
- one portfolio per user
- public form submission through a share link
- private submission management for the portfolio owner

All API routes are mounted under `/api/`.

## How It Works

### Core idea

Each user has:

- one account
- one share token
- one share toggle: `enable_share_token`
- one portfolio settings record

The public share link uses the user's share token:

```text
/api/shares/<user_share_token>/submissions/
```

If `enable_share_token` is `false`, that shared link does not work.

If `enable_share_token` is `true`, anyone can submit the public contact form through that link, and the submission is saved for:

- the owner user
- that owner's single portfolio

### Ownership model

The backend follows this rule:

- one user can have only one `PortfolioSettings`

Portfolio-related models are owned by a user. The main ownership field is `owner`.

For form submissions:

- `ContactFormSubmission.owner` is the user who receives the form
- `ContactFormSubmission.portfolio` is the portfolio the submission belongs to

### Auth model

Protected endpoints use JWT Bearer authentication.

Login returns:

- `temporary_token`: refresh token
- `bearer_token`: access token
- `token_type`: always `Bearer`

Use the access token like this:

```http
Authorization: Bearer <bearer_token>
```

Refresh with the refresh token when needed.

## Main Models

### User

Custom auth user with:

- `email`
- `enable_share_token`
- `share_token`
- `dashboard_token`
- `created_at`

Important behavior:

- `share_token` is generated automatically
- `enable_share_token` controls whether the public share link works

### PortfolioSettings

This is the single portfolio configuration for one user.

Important behavior:

- each owner can only have one `PortfolioSettings`
- it does not store its own share token anymore
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

## Request Rules

### Content type

Write endpoints expect JSON:

```http
Content-Type: application/json
```

Do not use form-data for normal API writes.

### JSON example

Correct:

```json
{
  "email": "alice@example.com",
  "password": "testpass123"
}
```

Incorrect in Postman/raw JSON:

```python
{
    "email": self.user.email,
    "password": "testpass123",
}
```

That is valid Python in tests, but not valid raw JSON.

## Full Flow

### 1. Create account

Create a user profile first.

Endpoint:

`POST /api/profiles/`

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

Notes:

- `username` is generated from the email
- `enable_share_token` starts as `false`
- the user gets a `share_token` immediately, but the public link should be considered inactive until sharing is enabled

### 2. Log in

Endpoint:

`POST /api/auth/login/`

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

### 3. Read the user's share configuration

Endpoint:

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

This endpoint tells the frontend:

- what the public share token is
- whether that share token should currently be usable

### 4. Public visitor submits the form

Endpoint:

`POST /api/shares/<user_share_token>/submissions/`

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

What happens internally:

1. the backend finds the user by `share_token`
2. it checks `enable_share_token=True`
3. it finds that user's single `PortfolioSettings`
4. it creates `ContactFormSubmission`
5. the submission is saved under:
   - `owner = that user`
   - `portfolio = that user's portfolio`

If sharing is disabled, the endpoint returns `404`.

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

Typical invalid credentials response:

```json
{
  "non_field_errors": [
    "Invalid email or password"
  ]
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

Response:

```json
{
  "access": "new-access-token"
}
```

### 5. Logout

`POST /api/auth/logout/`

Auth required: no bearer token header is required by the built-in endpoint, but you must send the refresh token to blacklist it.

Request:

```json
{
  "refresh": "<temporary_token>"
}
```

### 6. Get share status and token

`GET /api/profile/tokens/`

Auth required: yes

Response:

```json
{
  "enable_share_token": true,
  "share_token": "generated-user-share-token"
}
```

### 7. Submit public form

`POST /api/shares/<user_share_token>/submissions/`

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

Fields:

- `name`: required
- `email`: required
- `phone`: optional
- `message`: required
- `for_work`: optional boolean
- `priority`: optional integer

Priority values:

- `0` = Low
- `1` = Medium
- `2` = High
- `3` = Urgent

### 8. List submissions

`GET /api/submissions/`

Auth required: yes

Response:

```json
{
  "owner": "alice",
  "owner_user_id": 1,
  "submissions": [
    {
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
  ]
}
```

### 9. Update one submission

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

Updatable fields:

- `is_dismissed`
- `priority`
- `display_index`

### 10. Reorder all submissions

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

Response:

```json
{
  "message": "Submissions reordered successfully",
  "submissions": [
    {
      "id": 3,
      "display_index": 1,
      "owner": "alice",
      "owner_user_id": 1,
      "portfolio_id": 1,
      "name": "Visitor 3",
      "email": "visitor3@example.com",
      "phone": null,
      "message": "Hello",
      "for_work": false,
      "priority": 0,
      "priority_label": "Low",
      "is_dismissed": false,
      "submitted_at": "2026-04-03T10:00:00+05:30"
    }
  ]
}
```

## Share Link Rules

This is the most important business rule in the app.

### Public share URL

The app uses the user's share token:

```text
/api/shares/<user_share_token>/submissions/
```

### Share link works only when enabled

The link works only if:

- the user exists
- the token matches `User.share_token`
- `User.enable_share_token == true`

If sharing is off, the backend behaves like the link does not exist.

### Portfolio token behavior

There is no separate stored portfolio share token.

Instead:

- the user owns the share token
- the portfolio inherits that token conceptually
- the form is always submitted to the owner of that shared link

Because one user can only have one portfolio, the backend can safely attach the submission to that user's portfolio.

## Ordered Portfolio Models

Several content models are owner-scoped and ordered:

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

This makes them user-specific and sortable for portfolio rendering.

## Common Errors

### Invalid JSON

Example:

```json
{
  "detail": "JSON parse error - Expecting value: line 2 column 30 (char 31)"
}
```

Usually caused by:

- invalid raw JSON
- using Python expressions in Postman
- missing quotes
- trailing commas

### Missing auth

Example:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Share link disabled or not found

Current behavior:

- returns `404`

This is intentional so disabled share links do not reveal whether a token belongs to a real user.

## Development Notes

- The backend uses a custom `User` model
- Protected routes use JWT auth from SimpleJWT
- Write endpoints are JSON-only
- Submission ordering is stored with `display_index`
- One owner can have only one `PortfolioSettings`

## Recommended Frontend Usage

### For the owner dashboard

1. create profile
2. log in
3. store `bearer_token`
4. call `/api/profile/tokens/`
5. show:
   - `share_token`
   - `enable_share_token`
6. call `/api/submissions/` to manage incoming forms

### For the public portfolio site

1. build the shared form URL using the user's `share_token`
2. submit to:

```text
/api/shares/<user_share_token>/submissions/
```

3. if the share link is disabled, expect `404`
