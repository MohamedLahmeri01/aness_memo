# FreelanceArena — Complete Application & API Documentation

> **FreelanceArena** is a competitive freelancing platform where clients post competitions, freelancers submit blind proposals, and winners are selected based on merit — not identity. Built with Django 5.2 + Django REST Framework.

---

## Table of Contents

1. [Application Overview](#1-application-overview)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [Getting Started](#4-getting-started)
5. [Authentication & Authorization](#5-authentication--authorization)
6. [API Response Format](#6-api-response-format)
7. [Data Models](#7-data-models)
8. [API Documentation](#8-api-documentation)
   - [Accounts (Auth)](#81-accounts--authentication)
   - [Competitions](#82-competitions)
   - [Proposals](#83-proposals)
   - [Feedback & Reviews](#84-feedback--reviews)
   - [Notifications](#85-notifications)
   - [Payments](#86-payments)
9. [Business Logic & Rules](#9-business-logic--rules)
10. [Management Commands](#10-management-commands)
11. [Full URL Map](#11-full-url-map)

---

## 1. Application Overview

FreelanceArena is a university graduation project that implements a **competitive freelancing** model:

- **Clients** create competitions (projects) with budgets, deadlines, and requirements
- **Freelancers** submit proposals in a **blind review** system — clients score proposals without seeing freelancer identities
- **Winners** are selected based on proposal quality, and automated payment records are generated
- The platform takes a **10% platform fee** on all completed payments
- A full **notification system** keeps all parties informed
- **Questions & Answers** allow freelancers to ask clarifying questions on competitions

### User Roles

| Role | Description |
|------|-------------|
| `CLIENT` | Creates competitions, reviews proposals (blind), selects winners, leaves reviews |
| `FREELANCER` | Searches competitions, submits proposals, asks questions, receives payments |
| `ADMIN` | Full platform management — user management, payment processing, system oversight |

---

## 2. Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend Framework | Django | 5.2.11 |
| REST API | Django REST Framework | 3.16.1 |
| Authentication | SimpleJWT | 5.5.1 |
| Database | MySQL (via mysqlclient) | 9.1.0 / 2.2.8 |
| API Docs | drf-spectacular | 0.29.0 |
| CORS | django-cors-headers | 4.9.0 |
| Filtering | django-filter | 25.2 |
| Image Processing | Pillow | 12.1.1 |
| Language | Python | 3.11 |

---

## 3. Project Structure

```
freelance_arena/              # Django project settings
├── settings.py               # Configuration (DB, JWT, CORS, DRF, etc.)
├── urls.py                   # Root URL routing
├── exceptions.py             # Custom exception handler
├── utils.py                  # Success response helper
├── middleware.py              # UpdateLastSeenMiddleware
├── wsgi.py
└── asgi.py

accounts/                     # User management & authentication
├── models.py                 # Custom User model (UUID PK, roles)
├── serializers.py            # 6 serializers (register, login, profile, etc.)
├── views.py                  # 8 views (register, login, logout, profile, admin)
├── urls.py                   # 8 URL patterns
├── permissions.py            # IsClient, IsFreelancer, IsAdminRole, IsOwnerOrAdmin
└── admin.py

competitions/                 # Competition management
├── models.py                 # Competition, CompetitionQuestion, CompetitionBookmark
├── serializers.py            # 8 serializers (list, create, detail, status, etc.)
├── views.py                  # 10 views (CRUD, status, questions, bookmarks, winner)
├── urls.py                   # 10 URL patterns
├── filters.py                # CompetitionFilter (category, budget, deadline, tags)
├── signals.py                # Notify bookmarked users on status change
└── admin.py

proposals/                    # Proposal management
├── models.py                 # Proposal, ProposalAttachment, ProposalRevision
├── serializers.py            # 7 serializers (create, detail, blind list, score)
├── views.py                  # 8 views (submit, detail, attachments, score, withdraw)
├── urls.py                   # 8 URL patterns
├── signals.py                # Notify on proposal creation and scoring
└── admin.py

feedback/                     # Reviews & ratings
├── models.py                 # Review, UserRating (denormalized)
├── serializers.py            # 4 serializers (create, detail, rating)
├── views.py                  # 3 views (create review, user reviews, competition reviews)
├── urls.py                   # 3 URL patterns
├── signals.py                # Update UserRating on review save
└── admin.py

notifications/                # Notification system
├── models.py                 # Notification (10 types)
├── views.py                  # 4 views (list, mark read, mark all, unread count)
├── urls.py                   # 4 URL patterns
├── utils.py                  # NotificationService (6 static methods)
└── admin.py

payments/                     # Payment records
├── models.py                 # PaymentRecord (auto-calculated fees)
├── serializers.py            # 5 serializers (client, freelancer, admin, detail, status)
├── views.py                  # 5 views (client list, freelancer list, admin, detail, status)
├── urls.py                   # 5 URL patterns
└── admin.py

management/commands/
├── close_expired_competitions.py   # Auto-move OPEN→REVIEW when deadline passes
└── remind_deadlines.py             # Send 24hr deadline reminders
```

---

## 4. Getting Started

### Prerequisites

- Python 3.11+
- MySQL 8.0+ (via WampServer or standalone)
- Git

### Installation

```bash
# 1. Clone and navigate
cd F:\ANES OUSSAIE

# 2. Activate virtual environment
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create MySQL database
# In MySQL: CREATE DATABASE freelance_arena_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 5. Apply migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

### Access Points

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/api/docs/` | **Swagger UI** — Interactive API documentation |
| `http://127.0.0.1:8000/api/redoc/` | **ReDoc** — Readable API reference |
| `http://127.0.0.1:8000/admin/` | **Django Admin** — Backend management panel |
| `http://127.0.0.1:8000/api/schema/` | Raw OpenAPI 3.0 schema |

### Default Admin Credentials

| Field | Value |
|-------|-------|
| Email | `admin@freelancearena.com` |
| Password | `Admin@123` |

---

## 5. Authentication & Authorization

### JWT Authentication

All protected endpoints require a **Bearer token** in the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

| Setting | Value |
|---------|-------|
| Access Token Lifetime | 60 minutes |
| Refresh Token Lifetime | 7 days |
| Rotate Refresh Tokens | Yes |
| Blacklist After Rotation | Yes |

### How to Authenticate

1. **Register** → `POST /api/auth/register/` → Returns `access` and `refresh` tokens
2. **Login** → `POST /api/auth/login/` → Returns `access` and `refresh` tokens
3. **Use** → Include `Authorization: Bearer <access_token>` in every request
4. **Refresh** → When access token expires, use `refresh` token to get a new pair
5. **Logout** → `POST /api/auth/logout/` with `refresh` token → Blacklists the token

### Permission Classes

| Permission | Rule | Used By |
|------------|------|---------|
| `AllowAny` | No authentication required | Public endpoints |
| `IsAuthenticated` | Valid JWT token required | Most endpoints |
| `IsClient` | User must have `role='CLIENT'` | Competition creation, proposal scoring |
| `IsFreelancer` | User must have `role='FREELANCER'` | Proposal submission, questions |
| `IsAdminRole` | User must have `role='ADMIN'` | User management, payment admin |
| `IsOwnerOrAdmin` | Must be object owner or ADMIN | Object-level permission |

---

## 6. API Response Format

### Success Response

All successful responses follow this envelope:

```json
{
  "success": true,
  "message": "Human-readable success message.",
  "data": {
    // Response payload — object or paginated list
  }
}
```

### Error Response

All error responses follow this envelope:

```json
{
  "success": false,
  "message": "Error category description.",
  "errors": {
    "field_name": ["Error detail 1", "Error detail 2"],
    "non_field_errors": ["General error message"]
  }
}
```

### Error Types

| HTTP Status | Message | Triggered By |
|-------------|---------|--------------|
| 400 | `"Validation error."` | Invalid request data |
| 401 | `"Authentication failed."` | Missing/invalid/expired token |
| 403 | `"Permission denied."` | Insufficient role or ownership |
| 404 | `"Resource not found."` | Object does not exist |
| 405 | `"Method not allowed."` | Wrong HTTP method |
| 429 | `"Request was throttled."` | Rate limit exceeded |
| 500 | `"An unexpected error occurred."` | Server error (logged) |

### Pagination

All list endpoints use `PageNumberPagination` with 10 results per page:

```json
{
  "success": true,
  "message": "...",
  "data": {
    "count": 42,
    "next": "http://127.0.0.1:8000/api/competitions/?page=2",
    "previous": null,
    "results": [ ... ]
  }
}
```

Use `?page=N` to navigate pages.

---

## 7. Data Models

### 7.1 User (accounts)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, auto-generated | Unique identifier |
| `email` | EmailField | **unique**, max 254 chars | Login credential (USERNAME_FIELD) |
| `username` | CharField | **unique**, max 50 chars | Display name |
| `first_name` | CharField | max 100 chars, required | First name |
| `last_name` | CharField | max 100 chars, required | Last name |
| `role` | CharField | `CLIENT` / `FREELANCER` / `ADMIN` | User role (default: CLIENT) |
| `bio` | TextField | optional | Profile biography |
| `profile_picture` | ImageField | optional, upload to `profile_pictures/` | Avatar image |
| `skills` | TextField | optional, comma-separated | Freelancer skills list |
| `hourly_rate` | DecimalField | optional, 10 digits / 2 decimal | Freelancer hourly rate |
| `is_active` | BooleanField | default: True | Account active status |
| `is_staff` | BooleanField | default: False | Django admin access |
| `date_joined` | DateTimeField | auto-set on creation | Registration timestamp |
| `last_seen` | DateTimeField | optional | Last activity (updated by middleware) |
| `email_verified` | BooleanField | default: False | Email verification status |

**Computed property**: `full_name` → `"first_name last_name"`

---

### 7.2 Competition

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `client` | ForeignKey → User | must be CLIENT role | Competition creator |
| `title` | CharField | max 200 chars, required | Competition title |
| `description` | TextField | required | Full description |
| `requirements` | TextField | required | Technical requirements |
| `budget` | DecimalField | 12 digits / 2 decimal, required | Project budget |
| `currency` | CharField | max 3 chars, default: `USD` | Currency code |
| `deadline` | DateTimeField | required | Project completion deadline |
| `submission_deadline` | DateTimeField | required | Proposal submission cutoff |
| `status` | CharField | see state machine below | Current status |
| `category` | CharField | max 100 chars, required | Competition category |
| `tags` | TextField | optional, default: empty | Searchable tags |
| `max_proposals` | PositiveIntegerField | optional | Maximum allowed proposals |
| `allow_questions` | BooleanField | default: True | Whether Q&A is enabled |
| `winner` | ForeignKey → User | optional | Selected winner |
| `winning_proposal` | ForeignKey → Proposal | optional | Winning proposal |
| `created_at` | DateTimeField | auto-set | Creation timestamp |
| `updated_at` | DateTimeField | auto-updated | Last modification |

**Computed properties**: `is_open` (status == OPEN and submission_deadline > now), `proposal_count`

#### Competition Status State Machine

```
┌───────┐     ┌──────┐     ┌────────┐     ┌────────┐
│ DRAFT │────▶│ OPEN │────▶│ REVIEW │────▶│ CLOSED │
└───┬───┘     └──┬───┘     └────────┘     └────────┘
    │            │
    ▼            ▼
┌───────────┐
│ CANCELLED │
└───────────┘
```

| From | Allowed Transitions |
|------|-------------------|
| `DRAFT` | → `OPEN`, → `CANCELLED` |
| `OPEN` | → `REVIEW`, → `CANCELLED` |
| `REVIEW` | → `CLOSED` |
| `CLOSED` | *(terminal state)* |
| `CANCELLED` | *(terminal state)* |

---

### 7.3 CompetitionQuestion

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary Key |
| `competition` | FK → Competition | Parent competition |
| `asked_by` | FK → User | Question author (freelancer) |
| `question` | TextField | Question text |
| `answer` | TextField | Answer text (null until answered) |
| `answered_at` | DateTimeField | When answered (null) |
| `answered_by` | FK → User | Who answered (null, should be client) |
| `is_public` | BooleanField | Whether visible to all (default: True) |
| `created_at` | DateTimeField | Creation timestamp |

---

### 7.4 CompetitionBookmark

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary Key |
| `competition` | FK → Competition | Bookmarked competition |
| `user` | FK → User | User who bookmarked |
| `created_at` | DateTimeField | Bookmark timestamp |

**Constraint**: `unique_together = (competition, user)` — one bookmark per user per competition.

---

### 7.5 Proposal

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `competition` | FK → Competition | required | Target competition |
| `freelancer` | FK → User | must be FREELANCER role | Proposal author |
| `title` | CharField | max 200 chars | Proposal title |
| `description` | TextField | required | Proposal details |
| `proposed_budget` | DecimalField | 12 digits / 2 decimal | Proposed price |
| `estimated_duration` | PositiveIntegerField | required | Duration in days |
| `status` | CharField | see below | Proposal status |
| `submission_note` | TextField | optional | Additional notes |
| `client_score` | PositiveIntegerField | 1–5, optional | Client-assigned score |
| `client_note` | TextField | optional | Client scoring note |
| `is_winner` | BooleanField | default: False | Whether this won |
| `created_at` | DateTimeField | auto-set | Submission timestamp |
| `updated_at` | DateTimeField | auto-updated | Last modification |

**Constraint**: `unique_together = (competition, freelancer)` — one proposal per freelancer per competition.

**Proposal Statuses**: `SUBMITTED` → `UNDER_REVIEW` → `ACCEPTED` / `REJECTED` / `WITHDRAWN`

---

### 7.6 ProposalAttachment

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `proposal` | FK → Proposal | required | Parent proposal |
| `file` | FileField | upload to `proposal_attachments/` | Uploaded file |
| `original_filename` | CharField | max 255 | Original file name |
| `file_size` | PositiveIntegerField | in bytes | File size |
| `file_type` | CharField | max 50 | MIME type |
| `description` | CharField | max 255, optional | File description |
| `uploaded_at` | DateTimeField | auto-set | Upload timestamp |

**Validation**: Max **10 MB** per file. Allowed types: `pdf`, `doc`, `docx`, `zip`, `jpg`, `jpeg`, `png`, `mp4`.

---

### 7.7 Review

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `reviewer` | FK → User | required | Who wrote the review |
| `reviewee` | FK → User | required | Who is being reviewed |
| `competition` | FK → Competition | required | Related competition |
| `rating` | PositiveIntegerField | 1–5 | Numeric rating |
| `comment` | TextField | required | Review text |
| `review_type` | CharField | auto-determined | `CLIENT_TO_FREELANCER` or `FREELANCER_TO_CLIENT` |
| `is_public` | BooleanField | default: True | Whether publicly visible |
| `created_at` | DateTimeField | auto-set | Review timestamp |

**Constraint**: `unique_together = (reviewer, competition)` — one review per user per competition.

---

### 7.8 UserRating (Denormalized)

| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOneField → User | Primary Key |
| `average_rating` | DecimalField(3,2) | Calculated average (0.00–5.00) |
| `total_reviews` | PositiveIntegerField | Number of public reviews received |
| `updated_at` | DateTimeField | Last recalculation timestamp |

Auto-updated via signal whenever a Review is saved.

---

### 7.9 Notification

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary Key |
| `recipient` | FK → User | Notification target |
| `notification_type` | CharField | One of 10 types (see below) |
| `title` | CharField(200) | Notification title |
| `message` | TextField | Notification body |
| `is_read` | BooleanField | Read status (default: False) |
| `read_at` | DateTimeField | When marked as read |
| `related_competition_id` | UUID | Optional — related competition |
| `related_proposal_id` | UUID | Optional — related proposal |
| `created_at` | DateTimeField | Creation timestamp |

**Notification Types**:

| Type | Triggered When |
|------|---------------|
| `COMPETITION_OPENED` | Competition status changes to OPEN (sent to bookmarked users) |
| `PROPOSAL_RECEIVED` | New proposal submitted (sent to client) |
| `PROPOSAL_SCORED` | Client scores a proposal (sent to freelancer) |
| `PROPOSAL_ACCEPTED` | Freelancer's proposal wins (sent to winner) |
| `PROPOSAL_REJECTED` | Competition closed, proposal not selected (sent to losers) |
| `COMPETITION_CLOSED` | Competition status changes to CLOSED (sent to all freelancers) |
| `QUESTION_ANSWERED` | Client answers a question (sent to asker) |
| `WINNER_SELECTED` | Winner is chosen (sent to winner) |
| `NEW_REVIEW` | A review is left (sent to reviewee) |
| `COMPETITION_DEADLINE_APPROACHING` | 24 hours before deadline (via management command) |

---

### 7.10 PaymentRecord

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `competition` | OneToOneField → Competition | unique | One payment per competition |
| `client` | FK → User | required | Who pays |
| `freelancer` | FK → User | optional | Who receives |
| `amount` | DecimalField(12,2) | required | Total payment amount |
| `currency` | CharField(3) | default: `USD` | Currency code |
| `status` | CharField(20) | see state machine | Payment status |
| `platform_fee` | DecimalField(10,2) | **auto-calculated**: `amount × 0.10` | 10% platform fee |
| `net_amount` | DecimalField(12,2) | **auto-calculated**: `amount − platform_fee` | Freelancer receives |
| `created_at` | DateTimeField | auto-set | Record creation |
| `updated_at` | DateTimeField | auto-updated | Last update |
| `completed_at` | DateTimeField | optional | When payment completed |
| `transaction_reference` | CharField(100) | unique, optional | External reference |
| `notes` | TextField | optional | Admin notes |

#### Payment Status State Machine

```
┌─────────┐     ┌────────────┐     ┌───────────┐
│ PENDING │────▶│ PROCESSING │────▶│ COMPLETED │────▶ REFUNDED
└─────────┘     └─────┬──────┘     └───────────┘
                      │
                      ▼
                ┌────────┐
                │ FAILED │
                └────────┘
```

| From | Allowed Transitions |
|------|-------------------|
| `PENDING` | → `PROCESSING` |
| `PROCESSING` | → `COMPLETED`, → `FAILED` |
| `COMPLETED` | → `REFUNDED` |
| `FAILED` | *(terminal state)* |
| `REFUNDED` | *(terminal state)* |

---

## 8. API Documentation

---

### 8.1 Accounts / Authentication

---

#### `POST /api/auth/register/` — Register New User

| Property | Value |
|----------|-------|
| **Auth** | None |
| **Permission** | `AllowAny` |

**Request Body** (JSON):

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `email` | string | ✅ | Valid email, must be unique |
| `username` | string | ✅ | Max 50 chars, must be unique |
| `first_name` | string | ✅ | Max 100 chars |
| `last_name` | string | ✅ | Max 100 chars |
| `role` | string | ✅ | Must be `CLIENT` or `FREELANCER` (not `ADMIN`) |
| `password` | string | ✅ | Min 8 chars, Django password validators apply |
| `confirm_password` | string | ✅ | Must match `password` |

**Example Request**:
```json
{
  "email": "john@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "role": "FREELANCER",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

**Success Response** (201 Created):
```json
{
  "success": true,
  "message": "Registration successful.",
  "data": {
    "user": {
      "id": "8d6da5f3-d71a-4fab-8b91-ca7e04835c8f",
      "email": "john@example.com",
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "role": "FREELANCER",
      "bio": null,
      "profile_picture": null,
      "skills": null,
      "hourly_rate": null,
      "is_active": true,
      "date_joined": "2026-02-26T19:23:43.321642Z",
      "last_seen": null,
      "email_verified": false,
      "full_name": "John Doe"
    },
    "tokens": {
      "refresh": "eyJhbGciOiJIUzI1NiIs...",
      "access": "eyJhbGciOiJIUzI1NiIs..."
    }
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "message": "Validation error.",
  "errors": {
    "email": ["user with this email already exists."],
    "confirm_password": ["Passwords do not match."]
  }
}
```

---

#### `POST /api/auth/login/` — Login

| Property | Value |
|----------|-------|
| **Auth** | None |
| **Permission** | `AllowAny` |

**Request Body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | ✅ | Registered email |
| `password` | string | ✅ | Account password |

**Example Request**:
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "user_id": "8d6da5f3-d71a-4fab-8b91-ca7e04835c8f",
    "role": "FREELANCER",
    "tokens": {
      "refresh": "eyJhbGciOiJIUzI1NiIs...",
      "access": "eyJhbGciOiJIUzI1NiIs..."
    }
  }
}
```

**Error Response** (400):
```json
{
  "success": false,
  "message": "Validation error.",
  "errors": {
    "non_field_errors": ["Invalid credentials or account is deactivated."]
  }
}
```

---

#### `POST /api/auth/logout/` — Logout

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

**Request Body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `refresh` | string | ✅ | Refresh token to blacklist |

**Example Request**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Success Response** (200):
```json
{
  "success": true,
  "message": "Logout successful.",
  "data": null
}
```

---

#### `GET /api/auth/profile/` — Get My Profile

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

**Success Response** (200):
```json
{
  "success": true,
  "message": "Profile retrieved.",
  "data": {
    "id": "uuid",
    "email": "john@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "role": "FREELANCER",
    "bio": "Full-stack developer with 5 years experience",
    "profile_picture": "/media/profile_pictures/avatar.jpg",
    "skills": "Python, Django, React",
    "hourly_rate": "45.00",
    "is_active": true,
    "date_joined": "2026-02-26T19:23:43Z",
    "last_seen": "2026-02-26T20:00:00Z",
    "email_verified": false,
    "full_name": "John Doe"
  }
}
```

---

#### `PUT/PATCH /api/auth/profile/` — Update My Profile

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

**Writable Fields**:

| Field | Type | Validation |
|-------|------|------------|
| `username` | string | Max 50 chars |
| `first_name` | string | Max 100 chars |
| `last_name` | string | Max 100 chars |
| `bio` | string | Optional |
| `profile_picture` | file | Max 2 MB (multipart upload) |
| `skills` | string | Comma-separated, no empty entries |
| `hourly_rate` | decimal | Positive number |

**Read-Only Fields** (cannot be updated): `id`, `email`, `role`, `is_active`, `date_joined`

**Example Request** (PATCH — partial update):
```json
{
  "bio": "Updated bio text",
  "skills": "Python, Django, React, TypeScript",
  "hourly_rate": "50.00"
}
```

**Success Response** (200): Full profile object.

---

#### `DELETE /api/auth/profile/` — Deactivate Account

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

Soft-deletes the account by setting `is_active = False`.

**Success Response** (200):
```json
{ "success": true, "message": "Account deactivated.", "data": null }
```

---

#### `POST /api/auth/change-password/` — Change Password

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

**Request Body**:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `old_password` | string | ✅ | Must match current password |
| `new_password` | string | ✅ | Min 8 chars |
| `confirm_password` | string | ✅ | Must match `new_password` |

**Success Response** (200):
```json
{ "success": true, "message": "Password changed successfully.", "data": null }
```

---

#### `GET /api/auth/users/` — List All Users (Admin Only)

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsAdminRole` |

**Query Parameters**:

| Param | Type | Description |
|-------|------|-------------|
| `role` | string | Filter: `CLIENT`, `FREELANCER`, `ADMIN` |
| `is_active` | string | Filter: `true` / `false` |
| `search` | string | Search in: `username`, `email`, `first_name`, `last_name` |
| `ordering` | string | Sort by: `date_joined`, `username`, `email` (prefix `-` for descending) |
| `page` | int | Page number |

**Response**: Paginated list of `AdminUserSerializer` (includes `is_staff`, `is_active`, etc.).

---

#### `GET/PUT/DELETE /api/auth/users/<uuid:user_id>/` — User Detail (Admin Only)

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsAdminRole` |

- **GET** → Full user details
- **PUT** → Update any user field (including `role`, `is_active`, `is_staff`)
- **DELETE** → Soft-deactivate user (`is_active = False`)

---

#### `GET /api/auth/freelancers/search/` — Search Freelancers

| Property | Value |
|----------|-------|
| **Auth** | None |
| **Permission** | `AllowAny` |

Only returns `FREELANCER` users with `is_active = True`.

**Query Parameters**:

| Param | Type | Description |
|-------|------|-------------|
| `search` | string | Search: `username`, `skills`, `first_name`, `last_name` |
| `skills` | string | Filter by skills (comma-separated, icontains match) |
| `ordering` | string | Sort by: `hourly_rate`, `username` |
| `page` | int | Page number |

**Response Fields**: `id`, `username`, `first_name`, `last_name`, `full_name`, `bio`, `profile_picture`, `skills`, `hourly_rate`

---

### 8.2 Competitions

---

#### `GET /api/competitions/` — List Competitions

| Property | Value |
|----------|-------|
| **Auth** | None |
| **Permission** | `AllowAny` |

Only returns competitions with `status = 'OPEN'`.

**Query Parameters (Filters)**:

| Param | Type | Lookup | Description |
|-------|------|--------|-------------|
| `category` | string | exact (case-insensitive) | Filter by category |
| `status` | string | exact (case-insensitive) | Filter by status |
| `budget_min` | decimal | ≥ | Minimum budget |
| `budget_max` | decimal | ≤ | Maximum budget |
| `deadline_before` | datetime | ≤ | Deadline before date |
| `deadline_after` | datetime | ≥ | Deadline after date |
| `tags` | string | contains (case-insensitive) | Search tags |
| `search` | string | — | Search in: `title`, `description`, `category` |
| `ordering` | string | — | Sort by: `budget`, `deadline`, `created_at` |
| `page` | int | — | Page number |

**Response Fields**: `id`, `title`, `client_username`, `budget`, `currency`, `deadline`, `status`, `category`, `proposal_count`, `is_open`, `created_at`

---

#### `POST /api/competitions/create/` — Create Competition

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsClient` |

**Request Body**:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `title` | string | ✅ | Max 200 chars |
| `description` | string | ✅ | Full description |
| `requirements` | string | ✅ | Technical requirements |
| `budget` | decimal | ✅ | Must be > 0 |
| `currency` | string | ❌ | Default: `USD`, max 3 chars |
| `deadline` | datetime | ✅ | Must be in the future |
| `submission_deadline` | datetime | ✅ | Must be in the future AND before `deadline` |
| `category` | string | ✅ | Max 100 chars |
| `tags` | string | ❌ | Comma-separated tags |
| `max_proposals` | int | ❌ | If set, must be > 0 |
| `allow_questions` | boolean | ❌ | Default: true |

**Auto-set**: `client` = current user, `status` = `DRAFT`

**Example Request**:
```json
{
  "title": "Build a Portfolio Website",
  "description": "Need a responsive portfolio website with modern design...",
  "requirements": "HTML5, CSS3, JavaScript, responsive design, SEO optimized",
  "budget": "500.00",
  "deadline": "2026-06-30T23:59:59Z",
  "submission_deadline": "2026-06-15T23:59:59Z",
  "category": "WEB_DEVELOPMENT",
  "tags": "frontend, responsive, portfolio",
  "max_proposals": 20,
  "allow_questions": true
}
```

**Success Response** (201): Full competition detail object.

---

#### `GET /api/competitions/<uuid:id>/` — Competition Detail

| Property | Value |
|----------|-------|
| **Auth** | None |
| **Permission** | `AllowAny` |

Returns all competition fields plus public questions.

---

#### `PUT/PATCH /api/competitions/<uuid:id>/` — Update Competition

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | Must be competition owner |

**Only allowed when** `status` is `DRAFT` or `OPEN`.

---

#### `DELETE /api/competitions/<uuid:id>/` — Cancel Competition

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | Must be competition owner |

**Only allowed when** `status = 'DRAFT'`. Sets status to `CANCELLED`.

---

#### `POST /api/competitions/<uuid:id>/status/` — Change Competition Status

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsClient` (must be owner) |

**Request Body**:
```json
{ "status": "OPEN" }
```

Must follow the **state machine** (see Section 7.2). Invalid transitions return 400.

---

#### `GET /api/competitions/mine/` — My Competitions

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsClient` |

Returns competitions created by the current user. Supports `status` filter, `ordering`, `page`.

---

#### `GET/POST /api/competitions/<uuid:id>/questions/` — List/Ask Questions

| Property | Value |
|----------|-------|
| **Auth** | GET: None, POST: Bearer JWT |
| **Permission** | GET: `AllowAny`, POST: `IsAuthenticated` (must be FREELANCER) |

**GET** → List all public questions for the competition.

**POST** → Submit a question. Only if `allow_questions = True` AND `status = 'OPEN'`.

| Field | Type | Required |
|-------|------|----------|
| `question` | string | ✅ |

---

#### `POST /api/competitions/<uuid:comp_id>/questions/<uuid:q_id>/answer/` — Answer Question

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | Must be competition owner (Client) |

**Request Body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `answer` | string | ✅ | Answer text |
| `is_public` | boolean | ❌ | Default: true |

Auto-sets `answered_by` and `answered_at`. Triggers notification to question asker.

---

#### `POST /api/competitions/<uuid:id>/bookmark/` — Toggle Bookmark

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

**Toggle behavior**: Creates bookmark if none exists (201), removes if exists (200). No request body required.

---

#### `GET /api/competitions/bookmarks/` — My Bookmarks

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

Returns competitions bookmarked by the current user.

---

#### `POST /api/competitions/<uuid:id>/select-winner/` — Select Winner

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsClient` (must be owner) |

**Preconditions**: Competition `status` must be `REVIEW`. Proposal must not be `WITHDRAWN`.

**Request Body**:
```json
{ "proposal_id": "uuid-of-winning-proposal" }
```

**Side Effects**:
1. Competition: `status` → `CLOSED`, `winner` and `winning_proposal` set
2. Winning proposal: `status` → `ACCEPTED`, `is_winner` = true
3. All other proposals: `status` → `REJECTED`
4. **PaymentRecord** created (amount = budget, 10% platform fee)
5. **Notifications** sent: winner selected, competition closed, rejection to losers

---

### 8.3 Proposals

---

#### `POST /api/proposals/submit/` — Submit Proposal

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsFreelancer` |

**Request Body**:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `competition` | UUID | ✅ | Must be `OPEN`, submission_deadline not passed |
| `title` | string | ✅ | Max 200 chars |
| `description` | string | ✅ | Proposal description |
| `proposed_budget` | decimal | ✅ | Must be > 0 |
| `estimated_duration` | int | ✅ | Duration in days, positive integer |
| `submission_note` | string | ❌ | Additional notes |
| `attachments` | array | ❌ | Array of `{file, description}` |

**Validation Rules**:
- Competition must be `OPEN` and `submission_deadline` not passed
- One proposal per freelancer per competition (unique constraint)
- If `max_proposals` is set, cannot exceed limit
- Attachments: max **10 MB** per file, allowed types: `pdf`, `doc`, `docx`, `zip`, `jpg`, `jpeg`, `png`, `mp4`

**Example Request**:
```json
{
  "competition": "abc-def-123",
  "title": "Modern Portfolio Design",
  "description": "I will create a stunning responsive portfolio using React...",
  "proposed_budget": "450.00",
  "estimated_duration": 14,
  "submission_note": "Available to start immediately"
}
```

---

#### `GET /api/proposals/mine/` — My Proposals

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsFreelancer` |

**Query Parameters**:

| Param | Type | Description |
|-------|------|-------------|
| `competition` | UUID | Filter by competition |
| `status` | string | Filter: `SUBMITTED`, `UNDER_REVIEW`, `ACCEPTED`, `REJECTED`, `WITHDRAWN` |
| `ordering` | string | Sort by: `created_at`, `proposed_budget` |
| `page` | int | Page number |

**Response Fields**: `id`, `competition`, `competition_title`, `title`, `status`, `created_at`, `proposed_budget`

---

#### `GET /api/proposals/<uuid:id>/` — Proposal Detail

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | Proposal owner, competition client, or ADMIN |

Returns full proposal details including attachments.

---

#### `PUT /api/proposals/<uuid:id>/` — Update Proposal

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | Proposal owner only |

**Only when** `status = 'SUBMITTED'`. Updatable: `title`, `description`, `proposed_budget`, `estimated_duration`, `submission_note`.

---

#### `DELETE /api/proposals/<uuid:id>/` — Withdraw Proposal (via DELETE)

Sets `status = 'WITHDRAWN'`. Only allowed when `status = 'SUBMITTED'`.

---

#### `POST /api/proposals/<uuid:id>/attachments/` — Add Attachment

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsFreelancer` (proposal owner) |

**Only when** `status = 'SUBMITTED'`.

**Request** (multipart/form-data):

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `file` | file | ✅ | Max 10 MB, allowed types only |
| `description` | string | ❌ | File description |

---

#### `DELETE /api/proposals/<uuid:id>/attachments/<uuid:attachment_id>/` — Remove Attachment

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | Proposal owner only |

**Only when** `status = 'SUBMITTED'`.

---

#### `GET /api/proposals/competition/<uuid:comp_id>/` — Competition Proposals (Client View)

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsClient` (must be competition owner) |

🔒 **BLIND REVIEW** — Freelancer identity is hidden. Response excludes `WITHDRAWN` proposals.

**Response Fields**: `id`, `title`, `proposed_budget`, `estimated_duration`, `created_at`, `client_score`, `description`

**Query Parameters**: `ordering` (client_score, created_at, proposed_budget), `page`

---

#### `POST /api/proposals/<uuid:id>/score/` — Score Proposal

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsClient` (competition owner) |

**Only when** competition status is `OPEN` or `REVIEW`.

**Request Body**:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `client_score` | int | ✅ | 1–5 |
| `client_note` | string | ❌ | Scoring note |

---

#### `POST /api/proposals/<uuid:id>/withdraw/` — Withdraw Proposal

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsFreelancer` (proposal owner) |

**Only when** `status = 'SUBMITTED'`.

---

### 8.4 Feedback & Reviews

---

#### `POST /api/feedback/reviews/` — Create Review

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

**Request Body**:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `competition` | UUID | ✅ | Competition must be `CLOSED` |
| `reviewee` | UUID | ✅ | Person being reviewed |
| `rating` | int | ✅ | 1–5 |
| `comment` | string | ✅ | Review text |
| `is_public` | boolean | ❌ | Default: true |

**Validation Rules**:
- Competition must be `CLOSED`
- One review per user per competition
- Reviewer must have participated (as client or as freelancer with a submitted proposal)
- **If reviewer is CLIENT** → `review_type` = `CLIENT_TO_FREELANCER`, reviewee must be a freelancer who submitted a proposal
- **If reviewer is FREELANCER** → `review_type` = `FREELANCER_TO_CLIENT`, reviewee must be the competition client
- `review_type` is auto-determined (not in request body)

**Side Effects**: Updates `UserRating` for the reviewee, sends notification.

---

#### `GET /api/feedback/users/<uuid:user_id>/reviews/` — User Reviews

| Property | Value |
|----------|-------|
| **Auth** | None |
| **Permission** | `AllowAny` |

Returns public reviews for a user plus `rating_summary`:
```json
{
  "data": {
    "reviews": [...],
    "rating_summary": {
      "average_rating": "4.50",
      "total_reviews": 12
    }
  }
}
```

---

#### `GET /api/feedback/competitions/<uuid:comp_id>/reviews/` — Competition Reviews

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

Returns all reviews associated with a specific competition.

---

### 8.5 Notifications

---

#### `GET /api/notifications/` — List My Notifications

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

**Query Parameters**:

| Param | Type | Description |
|-------|------|-------------|
| `is_read` | string | `true` / `false` |
| `type` | string | Notification type (e.g., `PROPOSAL_RECEIVED`) |
| `page` | int | Page number |

**Response**:
```json
{
  "success": true,
  "message": "Notifications retrieved.",
  "data": {
    "unread_count": 5,
    "notifications": {
      "count": 42,
      "next": "...",
      "previous": null,
      "results": [
        {
          "id": "uuid",
          "notification_type": "PROPOSAL_RECEIVED",
          "title": "New Proposal Received",
          "message": "A new proposal has been submitted to your competition...",
          "is_read": false,
          "read_at": null,
          "related_competition_id": "uuid",
          "related_proposal_id": "uuid",
          "created_at": "2026-02-26T20:00:00Z"
        }
      ]
    }
  }
}
```

---

#### `POST /api/notifications/mark-read/` — Mark Specific Notifications Read

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

**Request Body**:
```json
{
  "notification_ids": ["uuid1", "uuid2", "uuid3"]
}
```

**Response**: `{ "data": { "marked_count": 3 } }`

---

#### `POST /api/notifications/mark-all-read/` — Mark All Read

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

No request body. Marks all unread notifications as read.

**Response**: `{ "data": { "marked_count": 15 } }`

---

#### `GET /api/notifications/unread-count/` — Unread Count

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated` |

**Response**:
```json
{ "success": true, "data": { "unread_count": 5 } }
```

---

### 8.6 Payments

---

#### `GET /api/payments/client/` — Client Payment History

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsClient` |

Returns payments where the current user is the client.

**Response Fields**: `id`, `competition`, `competition_title`, `amount`, `currency`, `status`, `created_at`

---

#### `GET /api/payments/freelancer/` — Freelancer Payment History

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsFreelancer` |

Returns payments where the current user is the freelancer.

**Response Fields**: `id`, `competition`, `competition_title`, `net_amount` (after 10% fee), `currency`, `status`, `completed_at`

---

#### `GET /api/payments/<uuid:id>/` — Payment Detail

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | Must be client, freelancer of the payment, or ADMIN |

Returns full payment record including `platform_fee`, `net_amount`, `transaction_reference`.

---

#### `GET /api/payments/admin/` — Admin Payment List

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsAdminRole` |

**Query Parameters**:

| Param | Type | Description |
|-------|------|-------------|
| `status` | string | Filter: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`, `REFUNDED` |
| `date_from` | date | Created after |
| `date_to` | date | Created before |
| `ordering` | string | Sort by: `created_at`, `amount`, `status` |
| `page` | int | Page number |

---

#### `POST /api/payments/<uuid:id>/update-status/` — Update Payment Status (Admin)

| Property | Value |
|----------|-------|
| **Auth** | Bearer JWT |
| **Permission** | `IsAuthenticated, IsAdminRole` |

**Request Body**:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `status` | string | ✅ | Must follow payment state machine |
| `transaction_reference` | string | ❌ | External payment reference |
| `notes` | string | ❌ | Admin notes |

Must follow the **payment state machine** (see Section 7.10). If status → `COMPLETED`, `completed_at` is auto-set.

---

## 9. Business Logic & Rules

### 9.1 Blind Review System

When a client views proposals for their competition (`GET /api/proposals/competition/<id>/`):
- **Freelancer identity is completely hidden** — no `freelancer` field, no username, no profile info
- Client sees only: `title`, `description`, `proposed_budget`, `estimated_duration`, `client_score`
- This ensures proposals are evaluated **purely on merit**
- Freelancer identity is only revealed after the winner is selected

### 9.2 Competition Lifecycle

1. **DRAFT** — Client creates competition, can still edit freely
2. **OPEN** — Competition is published, freelancers can submit proposals and questions
3. **REVIEW** — Submissions closed, client reviews and scores proposals
4. **CLOSED** — Winner selected, payment record created, reviews can be left
5. **CANCELLED** — Competition cancelled (from DRAFT or OPEN only)

### 9.3 Proposal Constraints

- **One proposal per freelancer per competition** (unique constraint)
- Proposals can only be submitted when competition is `OPEN` and before `submission_deadline`
- `max_proposals` limit is enforced if set
- Proposals can be edited/withdrawn only while `status = 'SUBMITTED'`
- Attachments: max 10 MB per file, allowed formats: PDF, DOC, DOCX, ZIP, JPG, JPEG, PNG, MP4

### 9.4 Review System

- Reviews can only be created for `CLOSED` competitions
- One review per reviewer per competition
- Reviewer must have participated (client of the competition, or freelancer with a submitted proposal)
- `review_type` is auto-determined based on reviewer role
- `UserRating` is auto-updated (denormalized) on every new review via Django signals

### 9.5 Payment Flow

- Payment records are **auto-created** when a winner is selected
- Platform fee is always **10%** of the competition budget
- Net amount (freelancer receives) = `amount - platform_fee`
- Admin manually processes payments through the status state machine
- `completed_at` is auto-set when status changes to `COMPLETED`

### 9.6 Notification System

Notifications are automatically created via signals and service methods:
- New proposal → client
- Proposal scored → freelancer
- Winner selected → winner + rejection notices to others
- Question answered → question asker
- Competition closed → all participating freelancers
- New review → reviewee
- Competition opened → bookmarked users
- Deadline approaching → management command (24hr before)

### 9.7 User Activity Tracking

The `UpdateLastSeenMiddleware` updates the `last_seen` field for authenticated users. To prevent excessive database writes, updates are **throttled to once every 5 minutes**.

---

## 10. Management Commands

### Close Expired Competitions

```bash
python manage.py close_expired_competitions
```

Automatically transitions competitions from `OPEN` → `REVIEW` when their deadline has passed. Intended to run as a **cron job** (e.g., every hour).

### Remind Deadlines

```bash
python manage.py remind_deadlines
```

Sends `COMPETITION_DEADLINE_APPROACHING` notifications to:
- Competition clients with OPEN competitions expiring within 24 hours
- Avoids duplicate notifications (checks for existing notification in the last 24 hours)

Intended to run as a **cron job** (e.g., every hour).

---

## 11. Full URL Map

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| POST | `/api/auth/register/` | — | Any | Register new user |
| POST | `/api/auth/login/` | — | Any | Login (get JWT) |
| POST | `/api/auth/logout/` | JWT | Any | Logout (blacklist token) |
| GET/PUT/PATCH/DELETE | `/api/auth/profile/` | JWT | Any | View/update/deactivate profile |
| POST | `/api/auth/change-password/` | JWT | Any | Change password |
| GET | `/api/auth/users/` | JWT | Admin | List all users |
| GET/PUT/DELETE | `/api/auth/users/<id>/` | JWT | Admin | Manage specific user |
| GET | `/api/auth/freelancers/search/` | — | Any | Search freelancers |
| GET | `/api/competitions/` | — | Any | List open competitions |
| POST | `/api/competitions/create/` | JWT | Client | Create competition |
| GET | `/api/competitions/mine/` | JWT | Client | My competitions |
| GET | `/api/competitions/bookmarks/` | JWT | Any | My bookmarks |
| GET/PUT/PATCH/DELETE | `/api/competitions/<id>/` | Mixed | Owner | Competition detail/edit/cancel |
| POST | `/api/competitions/<id>/status/` | JWT | Owner | Change status |
| GET/POST | `/api/competitions/<id>/questions/` | Mixed | FL(POST) | List/ask questions |
| POST | `/api/competitions/<id>/questions/<qid>/answer/` | JWT | Owner | Answer question |
| POST | `/api/competitions/<id>/bookmark/` | JWT | Any | Toggle bookmark |
| POST | `/api/competitions/<id>/select-winner/` | JWT | Owner | Select winner |
| POST | `/api/proposals/submit/` | JWT | Freelancer | Submit proposal |
| GET | `/api/proposals/mine/` | JWT | Freelancer | My proposals |
| GET/PUT/DELETE | `/api/proposals/<id>/` | JWT | Owner/CL/Admin | Proposal detail/edit/withdraw |
| POST | `/api/proposals/<id>/attachments/` | JWT | FL (owner) | Upload attachment |
| DELETE | `/api/proposals/<id>/attachments/<aid>/` | JWT | FL (owner) | Remove attachment |
| GET | `/api/proposals/competition/<comp_id>/` | JWT | CL (owner) | Blind proposal list |
| POST | `/api/proposals/<id>/score/` | JWT | CL (owner) | Score proposal |
| POST | `/api/proposals/<id>/withdraw/` | JWT | FL (owner) | Withdraw proposal |
| POST | `/api/feedback/reviews/` | JWT | Participant | Create review |
| GET | `/api/feedback/users/<user_id>/reviews/` | — | Any | User reviews |
| GET | `/api/feedback/competitions/<comp_id>/reviews/` | JWT | Any | Competition reviews |
| GET | `/api/notifications/` | JWT | Any | List notifications |
| POST | `/api/notifications/mark-read/` | JWT | Any | Mark specific read |
| POST | `/api/notifications/mark-all-read/` | JWT | Any | Mark all read |
| GET | `/api/notifications/unread-count/` | JWT | Any | Unread count |
| GET | `/api/payments/client/` | JWT | Client | Client payments |
| GET | `/api/payments/freelancer/` | JWT | Freelancer | Freelancer payments |
| GET | `/api/payments/admin/` | JWT | Admin | All payments |
| GET | `/api/payments/<id>/` | JWT | CL/FL/Admin | Payment detail |
| POST | `/api/payments/<id>/update-status/` | JWT | Admin | Update payment status |
| GET | `/api/docs/` | — | Any | Swagger UI |
| GET | `/api/redoc/` | — | Any | ReDoc docs |
| GET | `/api/schema/` | — | Any | OpenAPI schema |
| GET | `/admin/` | Session | Staff | Django admin |

**Legend**: JWT = Bearer token required, CL = Client, FL = Freelancer, Owner = resource owner

---

> **FreelanceArena** — Built as a university graduation project. A fair, merit-based competitive freelancing platform.
