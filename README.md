# 📘 Portfolio Backend API — Professional Documentation

A scalable, production-ready **Django REST Framework backend** for a portfolio platform featuring secure authentication, multi-portfolio management, public sharing, and a structured dashboard system.

---

# 🌐 Base URL

```bash
/api/
```

---

# 🧱 Architecture Overview

This backend is designed with:

* **Modular portfolio components** (fully JSON-driven)
* **Tier-based feature control** (Free vs Premium)
* **Token-based public access**
* **Secure authentication (JWT + OTP)**
* **Ordered relational data models**
* **Asynchronous task support (email, cleanup jobs)**

---

# 🔐 Authentication & Security

Supports:

* Email + Password login
* OTP-based verification
* JWT (Access + Refresh tokens)
* Token blacklisting for logout

---

## 🔑 Authentication Endpoints

### 1. Register User

**POST** `/api/auth/register/`

Creates a new user and sends an OTP for verification.

#### Request

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

#### Response

```json
{
  "message": "Profile created. OTP sent to your email.",
  "data": {
    "user_id": 1,
    "email": "user@example.com"
  }
}
```

---

### 2. Request OTP

**POST** `/api/auth/otp/request/`

Triggers OTP for login/verification.

```json
{
  "email": "user@example.com"
}
```

---

### 3. Verify OTP

**POST** `/api/auth/otp/verify/`

```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

#### Response

```json
{
  "message": "OTP verified.",
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "username": "user"
  },
  "tokens": {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }
}
```

---

### 4. Login

**POST** `/api/auth/login/`

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

#### Response

```json
{
  "message": "Login successful",
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "username": "user",
    "enable_share_token": true,
    "share_token": "token",
    "tokens": {
      "refresh": "<refresh_token>",
      "access": "<access_token>"
    }
  }
}
```

---

### 5. Refresh Token

**POST** `/api/auth/refresh/`

```json
{
  "refresh": "<refresh_token>"
}
```

---

### 6. Logout

**POST** `/api/auth/logout/`

```json
{
  "refresh": "<refresh_token>"
}
```

---

# 👤 User Profile Management

---

### 1. Get Profile

**GET** `/api/profile/`
🔒 Requires Authentication

#### Response

```json
{
  "user_id": 1,
  "email": "user@example.com",
  "username": "user",
  "first_name": "John",
  "last_name": "Doe",
  "profile_picture": "https://...",
  "theme_mode": 0,
  "tier": 0,
  "is_verified": true,
  "enable_share_token": true,
  "share_token": "token"
}
```

---

### 2. Update Profile

**PATCH** `/api/profile/update/`

Supports JSON and multipart (file upload).

#### Request (JSON)

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "theme_mode": 2
}
```

#### Response

```json
{
  "message": "Profile updated successfully.",
  "data": {
    "first_name": "John",
    "last_name": "Doe",
    "theme_mode": 2,
    "profile_picture": "https://..."
  }
}
```

---

### 3. Toggle Share Token

**POST** `/api/profile/share-toggle/`

Enables/disables public portfolio sharing.

---

### 4. Get Share Token

**GET** `/api/profile/get-token/`

---

# 🌐 Public Portfolio APIs

---

## Default Portfolio

**GET** `/api/portfolio/default/`
**GET** `/api/portfolio/default/<order_index>/`

### Behavior

* Resolves default user:

  1. `id=1`
  2. First available user

---

## Shared Portfolio

**GET** `/api/portfolio/shared/<share_token>/`
**GET** `/api/portfolio/shared/<share_token>/<order_index>/`

### Requirements

* `enable_share_token = true`
* Verified user

---

## Response Structure

```json
{
  "orderIndex": 1,
  "isEnabled": true,
  "tier": 0,
  "themeMode": 0,
  "personalInfo": {},
  "heroContent": {},
  "heroMetrics": [],
  "aboutContent": {},
  "skillGroups": [],
  "projects": [],
  "experience": [],
  "showcaseCategories": [],
  "featuredModules": [],
  "contactMethods": [],
  "navigationLinks": [],
  "footerLinks": [],
  "statusPills": []
}
```

---

# ✏️ Portfolio Management

---

## 1. Create / Replace Portfolio

**POST** `/api/portfolio/submit/`
**POST** `/api/portfolio/submit/<order_index>/`

🔒 Requires Authentication

### Key Characteristics

* Idempotent (creates or replaces)
* Fully JSON-driven
* Rebuilds ordered child models
* Applies tier constraints

---

## 2. Update Portfolio

**POST / PATCH** `/api/portfolio/update/<order_index>/`

### Supports:

* Partial updates
* Reordering portfolios
* Enable/disable state
* Full content updates

---

### Example: Change Order

```json
{
  "new_order_index": 2
}
```

---

### Example: Toggle Visibility

```json
{
  "is_enabled": false
}
```

---

# 📬 Contact Form System

---

## Public Submission

### Default Portfolio

**POST** `/api/forms/submit/default/<order_index>/`

### Shared Portfolio

**POST** `/api/forms/submit/shared/<share_token>/`

---

### Request

```json
{
  "name": "Visitor",
  "email": "visitor@example.com",
  "phone": "1234567890",
  "message": "Hello!",
  "for_work": true,
  "priority": 2
}
```

---

### Features

* IP-based rate limiting
* Priority classification
* Portfolio-linked submissions

---

# 📊 Dashboard APIs (Authenticated)

---

## Submissions

### List

**GET** `/api/dashboard/submissions/`

### Update

**PATCH** `/api/dashboard/submissions/<form_id>/`

```json
{
  "is_dismissed": true,
  "priority": 3,
  "display_index": 1
}
```

---

### Reorder

**POST** `/api/dashboard/submissions/reorder/`

```json
{
  "order": [3, 1, 2]
}
```

---

## Portfolio Management

### List Portfolios

**GET** `/api/dashboard/portfolios/`

### Toggle Portfolio

**PATCH** `/api/dashboard/portfolios/<order_index>/toggle/`

---

# 🧠 Tier-Based Constraints

---

## Free Tier

* Single portfolio only
* Max 3 items per core section
* Max 5 link entries

---

## Premium Tier

* Multiple portfolios
* Unlimited items
* Advanced customization

---

# ⚙️ Background Jobs (Cron APIs)

---

## Cleanup Unverified Users

**GET / POST** `/api/cron/cleanup/`

---

## Urgent Notifications

**GET / POST** `/api/cron/urgent-notifications/`

---

### Security Header

```bash
X-Cron-Secret: <CRON_SECRET_KEY>
```

---

# ⚠️ Error Handling

---

## Authentication Error

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## OTP Failure

```json
{
  "message": "Invalid or expired OTP."
}
```

---

## Tier Restriction

```json
{
  "message": "Upgrade to Premium to create multiple portfolios."
}
```

---

# 🔒 Security Considerations

* JWT-based authentication for protected routes
* OTP verification required for sharing
* Rate limiting on public forms
* Token-based portfolio access
* Secure cron endpoints

---

# 📎 Integration Notes

---

### Authorization Header

```bash
Authorization: Bearer <access_token>
```

---

### Content Type

```bash
Content-Type: application/json
```

---

# 📌 Conclusion

This backend provides a **robust, scalable foundation** for a portfolio platform with:

* Structured content modeling
* Clean API design
* Strong security practices
* Flexible frontend integration

---
