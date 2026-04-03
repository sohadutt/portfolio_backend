# Portfolio Backend API

This project exposes a JSON API under `/api/`.

## Base Rules

- Base prefix: `/api/`
- Write endpoints expect `Content-Type: application/json`
- Protected endpoints require:

```http
Authorization: Bearer <bearer_token>
```

- Public form submissions use a profile's `share_token`
- Login returns:
  - `temporary_token`: refresh token
  - `bearer_token`: access token
  - `token_type`: always `Bearer`

## Auth Flow

1. Create a profile with `POST /api/profiles/`
2. Log in with `POST /api/auth/login/`
3. Use the returned `bearer_token` in protected requests
4. Refresh the bearer token with `POST /api/auth/refresh/` when needed

## Endpoints

### 1. Get CSRF Cookie

`GET /api/csrf/`

Auth: none

Request body: none

Example response:

```json
{
  "detail": "CSRF cookie set"
}
```

### 2. Create Profile

`POST /api/profiles/`

Auth: none

Request body:

```json
{
  "email": "bob@example.com",
  "password": "bobpass123"
}
```

Example success response:

```json
{
  "message": "Profile created successfully",
  "data": {
    "user_id": 2,
    "email": "bob@example.com",
    "username": "bob",
    "share_token": "share-token-here"
  }
}
```

Typical error response:

```json
{
  "message": "A user with this email already exists"
}
```

### 3. Login

`POST /api/auth/login/`

Auth: none

Request body:

```json
{
  "email": "alice@example.com",
  "password": "testpass123"
}
```

Example success response:

```json
{
  "message": "Login successful",
  "data": {
    "user_id": 1,
    "email": "alice@example.com",
    "username": "alice",
    "share_token": "share-token-here",
    "temporary_token": "refresh-token-here",
    "bearer_token": "access-token-here",
    "token_type": "Bearer"
  }
}
```

Typical error response:

```json
{
  "non_field_errors": [
    "Invalid email or password"
  ]
}
```

### 4. Refresh Bearer Token

`POST /api/auth/refresh/`

Auth: none

Request body:

```json
{
  "refresh": "<temporary_token>"
}
```

Example success response:

```json
{
  "access": "new-access-token-here"
}
```

### 5. Get Profile Tokens

`GET /api/profile/tokens/`

Auth: bearer token required

Request body: none

Example success response:

```json
{
  "share_token": "share-token-here"
}
```

### 6. Submit Public Form

`POST /api/shares/<share_token>/submissions/`

Auth: none

Request body:

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

Notes:

- `phone` is optional
- `for_work` should be `true` or `false`
- `priority` is an integer
- If omitted, `priority` defaults to `0`

Example success response:

```json
{
  "message": "Form submitted successfully",
  "data": {
    "id": 1,
    "display_index": 1,
    "owner": "alice",
    "owner_user_id": 1,
    "name": "Visitor",
    "email": "visitor@example.com",
    "phone": "1234567890",
    "message": "Hello Alice",
    "for_work": true,
    "priority": 1,
    "is_dismissed": false,
    "submitted_at": "2026-04-03T10:00:00+05:30"
  }
}
```

### 7. List Your Submissions

`GET /api/submissions/`

Auth: bearer token required

Request body: none

Example success response:

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
      "name": "Visitor",
      "email": "visitor@example.com",
      "phone": "1234567890",
      "message": "Hello Alice",
      "for_work": true,
      "priority": 1,
      "is_dismissed": false,
      "submitted_at": "2026-04-03T10:00:00+05:30"
    }
  ]
}
```

Typical auth error response:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 8. Update Submission

`PATCH /api/submissions/<form_id>/`

Also supported:

`POST /api/submissions/<form_id>/`

Auth: bearer token required

Request body can be partial. Example:

```json
{
  "is_dismissed": true,
  "priority": 2,
  "display_index": 1
}
```

You can also send only one field:

```json
{
  "display_index": 1
}
```

Supported updatable fields:

- `is_dismissed`
- `priority`
- `display_index`

Example success response:

```json
{
  "message": "Form updated successfully",
  "data": {
    "id": 3,
    "display_index": 1,
    "owner": "alice",
    "owner_user_id": 1,
    "name": "Visitor 2",
    "email": "visitor2@example.com",
    "phone": null,
    "message": "Hello 2",
    "for_work": false,
    "priority": 2,
    "is_dismissed": true,
    "submitted_at": "2026-04-03T10:00:00+05:30"
  }
}
```

## Quick Request Examples

### Login

```http
POST /api/auth/login/
Content-Type: application/json
```

```json
{
  "email": "alice@example.com",
  "password": "testpass123"
}
```

### Protected Request

```http
GET /api/submissions/
Authorization: Bearer <bearer_token>
```

### Refresh Token

```http
POST /api/auth/refresh/
Content-Type: application/json
```

```json
{
  "refresh": "<temporary_token>"
}
```

## Important Notes

- Use JSON, not form-data, for API writes
- In tests, Python expressions like `self.user.email` are valid because Django builds the request body
- In Postman, Insomnia, or Thunder Client, replace those expressions with real strings
- If you send invalid JSON, the API returns an error like:

```json
{
  "detail": "JSON parse error - Expecting value: line 2 column 30 (char 31)"
}
```
