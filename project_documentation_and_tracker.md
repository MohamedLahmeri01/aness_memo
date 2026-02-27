# FreelanceArena - Project Documentation and Development Tracker
# University Graduation Project | Universite Mustapha Stambouli de Mascara
# Academic Year: 2025/2026

---

## Project Identity

Project Title: Development of a Competitive Freelancing Platform (FreelanceArena)
Institution: Universite Mustapha Stambouli de Mascara
Faculty: Faculte des Sciences Exactes
Department: Departement Informatique
Specialty: Systeme Informatique
Supervisor: Abdessamed Ouessai

Students:
- Hamadouche Moncef Afif
- Hassi Mohamed Anes

Submission Date: 01/02/2026

---

## Technology Stack

| Layer              | Technology            | Version       |
|--------------------|----------------------|---------------|
| Language           | Python               | 3.10+         |
| Web Framework      | Django               | 4.2+          |
| API Framework      | Django REST Framework | 3.14+         |
| Database           | MySQL (WampServer)   | 8.0+          |
| DB Connector       | mysqlclient          | Latest        |
| Authentication     | djangorestframework-simplejwt | Latest |
| CORS               | django-cors-headers  | Latest        |
| Image Handling     | Pillow               | Latest        |
| Filtering          | django-filter        | Latest        |
| Local Dev Server   | Django runserver     | Built-in      |
| DB Admin           | WampServer phpMyAdmin | Latest       |

---

## System Architecture Overview

The backend is a RESTful API consumed by any frontend or mobile client. All communication is over HTTP with JSON request and response bodies. Authentication is stateless using JWT tokens. Users are separated into three roles: CLIENT, FREELANCER, and ADMIN. The system enforces blind review so freelancers cannot see competitor submissions.

---

## Django Apps and Responsibilities

| App            | Responsibility                                                       |
|----------------|----------------------------------------------------------------------|
| accounts       | User registration, login, JWT auth, profile management, permissions  |
| competitions   | Job postings, competition lifecycle, questions and answers           |
| proposals      | Freelancer submissions, attachments, scoring, winner selection       |
| feedback       | Post-competition reviews and ratings between clients and freelancers |
| notifications  | In-app notification system for all platform events                   |
| payments       | Payment record tracking and status management                        |

---

## Database Schema Summary

### Table: accounts_user
| Column           | Type          | Notes                            |
|------------------|---------------|----------------------------------|
| id               | UUID (PK)     | Auto-generated                   |
| email            | VARCHAR(254)  | Unique, used as username         |
| username         | VARCHAR(50)   | Unique                           |
| first_name       | VARCHAR(100)  |                                  |
| last_name        | VARCHAR(100)  |                                  |
| role             | VARCHAR(20)   | CLIENT / FREELANCER / ADMIN      |
| bio              | TEXT          | Optional                         |
| profile_picture  | VARCHAR(255)  | File path                        |
| skills           | TEXT          | Comma-separated, freelancers     |
| hourly_rate      | DECIMAL(10,2) | Optional, freelancers            |
| is_active        | BOOLEAN       | Default True                     |
| is_staff         | BOOLEAN       | Default False                    |
| date_joined      | DATETIME      | Auto                             |
| last_seen        | DATETIME      | Updated via middleware            |
| email_verified   | BOOLEAN       | Default False                    |

### Table: competitions_competition
| Column               | Type           | Notes                             |
|----------------------|----------------|-----------------------------------|
| id                   | UUID (PK)      |                                   |
| client_id            | UUID (FK)      | accounts_user                     |
| title                | VARCHAR(200)   |                                   |
| description          | TEXT           |                                   |
| requirements         | TEXT           |                                   |
| budget               | DECIMAL(12,2)  |                                   |
| currency             | VARCHAR(3)     | Default USD                       |
| deadline             | DATETIME       |                                   |
| submission_deadline  | DATETIME       |                                   |
| status               | VARCHAR(20)    | DRAFT/OPEN/REVIEW/CLOSED/CANCELLED|
| category             | VARCHAR(100)   |                                   |
| tags                 | TEXT           | Comma-separated                   |
| max_proposals        | INT            | Nullable                          |
| allow_questions      | BOOLEAN        | Default True                      |
| created_at           | DATETIME       | Auto                              |
| updated_at           | DATETIME       | Auto                              |
| winner_id            | UUID (FK)      | accounts_user, nullable           |
| winning_proposal_id  | UUID (FK)      | proposals_proposal, nullable      |

### Table: competitions_competitionquestion
| Column          | Type       | Notes                          |
|-----------------|------------|--------------------------------|
| id              | UUID (PK)  |                                |
| competition_id  | UUID (FK)  |                                |
| asked_by_id     | UUID (FK)  | accounts_user                  |
| question        | TEXT       |                                |
| answer          | TEXT       | Nullable                       |
| answered_at     | DATETIME   | Nullable                       |
| answered_by_id  | UUID (FK)  | Nullable                       |
| is_public       | BOOLEAN    | Default True                   |
| created_at      | DATETIME   | Auto                           |

### Table: competitions_competitionbookmark
| Column         | Type       | Notes               |
|----------------|------------|---------------------|
| id             | UUID (PK)  |                     |
| competition_id | UUID (FK)  |                     |
| user_id        | UUID (FK)  |                     |
| created_at     | DATETIME   | Auto                |

### Table: proposals_proposal
| Column              | Type           | Notes                                    |
|---------------------|----------------|------------------------------------------|
| id                  | UUID (PK)      |                                          |
| competition_id      | UUID (FK)      |                                          |
| freelancer_id       | UUID (FK)      |                                          |
| title               | VARCHAR(200)   |                                          |
| description         | TEXT           |                                          |
| proposed_budget     | DECIMAL(12,2)  |                                          |
| estimated_duration  | INT            | Days                                     |
| status              | VARCHAR(20)    | SUBMITTED/UNDER_REVIEW/ACCEPTED/REJECTED/WITHDRAWN |
| submission_note     | TEXT           | Optional                                 |
| created_at          | DATETIME       | Auto                                     |
| updated_at          | DATETIME       | Auto                                     |
| client_score        | INT            | 1-5, nullable, set by client             |
| client_note         | TEXT           | Nullable                                 |
| is_winner           | BOOLEAN        | Default False                            |

### Table: proposals_proposalattachment
| Column            | Type         | Notes      |
|-------------------|--------------|------------|
| id                | UUID (PK)    |            |
| proposal_id       | UUID (FK)    |            |
| file              | VARCHAR(255) | File path  |
| original_filename | VARCHAR(255) |            |
| file_size         | INT          | Bytes      |
| file_type         | VARCHAR(50)  |            |
| uploaded_at       | DATETIME     | Auto       |
| description       | VARCHAR(255) | Optional   |

### Table: proposals_proposalrevision
| Column          | Type      | Notes |
|-----------------|-----------|-------|
| id              | UUID (PK) |       |
| proposal_id     | UUID (FK) |       |
| revised_by_id   | UUID (FK) |       |
| description     | TEXT      |       |
| revision_number | INT       |       |
| created_at      | DATETIME  | Auto  |

### Table: feedback_review
| Column         | Type      | Notes                                   |
|----------------|-----------|-----------------------------------------|
| id             | UUID (PK) |                                         |
| reviewer_id    | UUID (FK) |                                         |
| reviewee_id    | UUID (FK) |                                         |
| competition_id | UUID (FK) |                                         |
| rating         | INT       | 1-5                                     |
| comment        | TEXT      |                                         |
| review_type    | VARCHAR(30)| CLIENT_TO_FREELANCER / FREELANCER_TO_CLIENT |
| created_at     | DATETIME  | Auto                                    |
| is_public      | BOOLEAN   | Default True                            |

### Table: feedback_userrating
| Column         | Type            | Notes          |
|----------------|-----------------|----------------|
| user_id        | UUID (FK, PK)   | OneToOne       |
| average_rating | DECIMAL(3,2)    | Denormalized   |
| total_reviews  | INT             |                |
| updated_at     | DATETIME        | Auto           |

### Table: notifications_notification
| Column                   | Type        | Notes                        |
|--------------------------|-------------|------------------------------|
| id                       | UUID (PK)   |                              |
| recipient_id             | UUID (FK)   |                              |
| notification_type        | VARCHAR(50) | See choices in model         |
| title                    | VARCHAR(200)|                              |
| message                  | TEXT        |                              |
| is_read                  | BOOLEAN     | Default False                |
| read_at                  | DATETIME    | Nullable                     |
| related_competition_id   | UUID        | Nullable                     |
| related_proposal_id      | UUID        | Nullable                     |
| created_at               | DATETIME    | Auto                         |

### Table: payments_paymentrecord
| Column                  | Type           | Notes                          |
|-------------------------|----------------|--------------------------------|
| id                      | UUID (PK)      |                                |
| competition_id          | UUID (FK)      | OneToOne                       |
| client_id               | UUID (FK)      |                                |
| freelancer_id           | UUID (FK)      | Nullable, SET NULL             |
| amount                  | DECIMAL(12,2)  |                                |
| currency                | VARCHAR(3)     | Default USD                    |
| status                  | VARCHAR(20)    | PENDING/PROCESSING/COMPLETED/FAILED/REFUNDED |
| platform_fee            | DECIMAL(10,2)  | 10% of amount, auto-calculated |
| net_amount              | DECIMAL(12,2)  | amount - platform_fee          |
| created_at              | DATETIME       | Auto                           |
| updated_at              | DATETIME       | Auto                           |
| completed_at            | DATETIME       | Nullable                       |
| transaction_reference   | VARCHAR(100)   | Unique, nullable               |
| notes                   | TEXT           | Optional                       |

---

## Competition Status Machine

```
DRAFT -----> OPEN -----> REVIEW -----> CLOSED
  |           |
  v           v
CANCELLED   CANCELLED
```

Rules:
- DRAFT: competition is created but not yet published
- OPEN: freelancers can submit proposals
- REVIEW: submission deadline passed, client reviews proposals
- CLOSED: winner selected, competition ended
- CANCELLED: client cancelled before completion, terminal state

---

## Payment Fee Structure

- Total competition budget = amount paid by client
- Platform fee = 10% of amount
- Freelancer net amount = amount - platform_fee
- Example: $500 budget = $50 platform fee = $450 to freelancer

---

## API Endpoint Reference

### Authentication Endpoints (api/auth/)

| Method | URL                          | Auth Required | Role        | Description                        |
|--------|------------------------------|---------------|-------------|------------------------------------|
| POST   | /api/auth/register/          | No            | Any         | Register new client or freelancer  |
| POST   | /api/auth/login/             | No            | Any         | Login, returns JWT tokens          |
| POST   | /api/auth/logout/            | Yes           | Any         | Logout, blacklists refresh token   |
| GET    | /api/auth/profile/           | Yes           | Any         | Get own profile                    |
| PUT    | /api/auth/profile/           | Yes           | Any         | Update own profile                 |
| PATCH  | /api/auth/profile/           | Yes           | Any         | Partial update own profile         |
| DELETE | /api/auth/profile/           | Yes           | Any         | Deactivate own account             |
| POST   | /api/auth/change-password/   | Yes           | Any         | Change password                    |
| GET    | /api/auth/users/             | Yes           | Admin       | List all users                     |
| GET    | /api/auth/users/{id}/        | Yes           | Admin       | Get specific user                  |
| PUT    | /api/auth/users/{id}/        | Yes           | Admin       | Update specific user               |
| DELETE | /api/auth/users/{id}/        | Yes           | Admin       | Deactivate specific user           |
| GET    | /api/auth/freelancers/search/| No            | Any         | Search freelancers by skills       |

### Competition Endpoints (api/competitions/)

| Method | URL                                              | Auth Required | Role        | Description                         |
|--------|--------------------------------------------------|---------------|-------------|-------------------------------------|
| GET    | /api/competitions/                               | No            | Any         | List all open competitions          |
| POST   | /api/competitions/create/                        | Yes           | Client      | Create new competition              |
| GET    | /api/competitions/{id}/                          | No            | Any         | Get competition detail              |
| PUT    | /api/competitions/{id}/                          | Yes           | Client (owner)| Update competition                |
| PATCH  | /api/competitions/{id}/                          | Yes           | Client (owner)| Partial update competition        |
| DELETE | /api/competitions/{id}/                          | Yes           | Client (owner)| Cancel competition                |
| POST   | /api/competitions/{id}/status/                   | Yes           | Client (owner)| Change competition status         |
| GET    | /api/competitions/mine/                          | Yes           | Client      | List own competitions               |
| GET    | /api/competitions/{id}/questions/                | No            | Any         | List public questions               |
| POST   | /api/competitions/{id}/questions/                | Yes           | Freelancer  | Ask a question                      |
| POST   | /api/competitions/{id}/questions/{qid}/answer/   | Yes           | Client (owner)| Answer a question                 |
| POST   | /api/competitions/{id}/bookmark/                 | Yes           | Any         | Toggle bookmark                     |
| GET    | /api/competitions/bookmarks/                     | Yes           | Any         | List bookmarked competitions        |
| POST   | /api/competitions/{id}/select-winner/            | Yes           | Client (owner)| Select winning proposal           |

### Proposal Endpoints (api/proposals/)

| Method | URL                                        | Auth Required | Role             | Description                     |
|--------|--------------------------------------------|---------------|------------------|---------------------------------|
| POST   | /api/proposals/submit/                     | Yes           | Freelancer       | Submit proposal to competition  |
| GET    | /api/proposals/mine/                       | Yes           | Freelancer       | List own proposals              |
| GET    | /api/proposals/{id}/                       | Yes           | Freelancer or Client | Get proposal detail         |
| PUT    | /api/proposals/{id}/                       | Yes           | Freelancer (owner)| Update submitted proposal      |
| POST   | /api/proposals/{id}/attachments/           | Yes           | Freelancer (owner)| Add attachment to proposal     |
| DELETE | /api/proposals/{id}/attachments/{aid}/     | Yes           | Freelancer (owner)| Delete attachment              |
| GET    | /api/proposals/competition/{comp_id}/      | Yes           | Client (owner)   | List all proposals for own competition |
| POST   | /api/proposals/{id}/score/                 | Yes           | Client (owner)   | Score a proposal                |
| POST   | /api/proposals/{id}/withdraw/              | Yes           | Freelancer (owner)| Withdraw proposal              |

### Feedback Endpoints (api/feedback/)

| Method | URL                                   | Auth Required | Role  | Description                       |
|--------|---------------------------------------|---------------|-------|-----------------------------------|
| POST   | /api/feedback/reviews/                | Yes           | Any   | Create review after closed comp   |
| GET    | /api/feedback/users/{id}/reviews/     | No            | Any   | Get all public reviews for user   |
| GET    | /api/feedback/competitions/{id}/reviews/ | Yes        | Any   | Get reviews for competition       |

### Notification Endpoints (api/notifications/)

| Method | URL                                  | Auth Required | Role | Description                   |
|--------|--------------------------------------|---------------|------|-------------------------------|
| GET    | /api/notifications/                  | Yes           | Any  | List own notifications        |
| POST   | /api/notifications/mark-read/        | Yes           | Any  | Mark selected as read         |
| POST   | /api/notifications/mark-all-read/    | Yes           | Any  | Mark all as read              |
| GET    | /api/notifications/unread-count/     | Yes           | Any  | Get unread count              |

### Payment Endpoints (api/payments/)

| Method | URL                               | Auth Required | Role      | Description                    |
|--------|-----------------------------------|---------------|-----------|--------------------------------|
| GET    | /api/payments/client/             | Yes           | Client    | Own payments made              |
| GET    | /api/payments/freelancer/         | Yes           | Freelancer| Own payments received          |
| GET    | /api/payments/{id}/               | Yes           | Client/Freelancer/Admin | Payment detail  |
| GET    | /api/payments/admin/              | Yes           | Admin     | All payments with filters      |
| POST   | /api/payments/{id}/update-status/ | Yes           | Admin     | Update payment status          |

---

## Development Progress Tracker

Instructions: Update status for each task as development proceeds. Statuses: NOT_STARTED, IN_PROGRESS, DONE, BLOCKED.

### Phase 1: Project Setup
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| Virtual environment created                | NOT_STARTED |       |
| Dependencies installed                     | NOT_STARTED |       |
| Django project initialized                 | NOT_STARTED |       |
| All apps created                           | NOT_STARTED |       |
| settings.py configured                     | NOT_STARTED |       |
| Database created in WampServer             | NOT_STARTED |       |
| MySQL connection verified                  | NOT_STARTED |       |

### Phase 2: Models and Migrations
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| accounts.User model written                | NOT_STARTED |       |
| competitions models written                | NOT_STARTED |       |
| proposals models written                   | NOT_STARTED |       |
| feedback models written                    | NOT_STARTED |       |
| notifications model written                | NOT_STARTED |       |
| payments model written                     | NOT_STARTED |       |
| All migrations generated                   | NOT_STARTED |       |
| All migrations applied                     | NOT_STARTED |       |

### Phase 3: Authentication and Accounts API
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| UserRegistrationSerializer                 | NOT_STARTED |       |
| UserLoginSerializer                        | NOT_STARTED |       |
| UserProfileSerializer                      | NOT_STARTED |       |
| ChangePasswordSerializer                   | NOT_STARTED |       |
| RegisterView                               | NOT_STARTED |       |
| LoginView                                  | NOT_STARTED |       |
| LogoutView                                 | NOT_STARTED |       |
| ProfileView                                | NOT_STARTED |       |
| Custom permission classes                  | NOT_STARTED |       |
| accounts URL configuration                 | NOT_STARTED |       |

### Phase 4: Competitions API
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| All competition serializers                | NOT_STARTED |       |
| All competition views                      | NOT_STARTED |       |
| Status machine enforced                    | NOT_STARTED |       |
| Questions and answers endpoints            | NOT_STARTED |       |
| Bookmark endpoints                         | NOT_STARTED |       |
| Select winner endpoint                     | NOT_STARTED |       |
| Competition URL configuration              | NOT_STARTED |       |

### Phase 5: Proposals API
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| All proposal serializers                   | NOT_STARTED |       |
| Blind review logic implemented             | NOT_STARTED |       |
| File upload and validation                 | NOT_STARTED |       |
| Scoring endpoint                           | NOT_STARTED |       |
| Withdraw endpoint                          | NOT_STARTED |       |
| Proposal URL configuration                 | NOT_STARTED |       |

### Phase 6: Feedback API
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| Review model and serializers               | NOT_STARTED |       |
| UserRating denormalization                 | NOT_STARTED |       |
| Signals for rating updates                 | NOT_STARTED |       |
| Feedback URL configuration                 | NOT_STARTED |       |

### Phase 7: Notifications
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| Notification model                         | NOT_STARTED |       |
| NotificationService utility class          | NOT_STARTED |       |
| All notification triggers connected        | NOT_STARTED |       |
| Notifications URL configuration            | NOT_STARTED |       |

### Phase 8: Payments
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| PaymentRecord model with auto-calculations | NOT_STARTED |       |
| Payment creation on winner selection       | NOT_STARTED |       |
| Payment views and permissions              | NOT_STARTED |       |
| Payments URL configuration                 | NOT_STARTED |       |

### Phase 9: System Features
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| Custom exception handler                   | NOT_STARTED |       |
| Success response utility                   | NOT_STARTED |       |
| UpdateLastSeenMiddleware                   | NOT_STARTED |       |
| close_expired_competitions command         | NOT_STARTED |       |
| remind_deadlines command                   | NOT_STARTED |       |
| Admin configurations for all apps         | NOT_STARTED |       |

### Phase 10: Testing
| Task                                       | Status      | Notes |
|--------------------------------------------|-------------|-------|
| accounts tests                             | NOT_STARTED |       |
| competitions tests                         | NOT_STARTED |       |
| proposals tests                            | NOT_STARTED |       |
| feedback tests                             | NOT_STARTED |       |
| payments tests                             | NOT_STARTED |       |
| All tests passing                          | NOT_STARTED |       |

---

## Known Constraints and Design Decisions

1. Blind Review: The ClientProposalListSerializer intentionally excludes freelancer identity and peer proposal content. This is a core business rule and must not be bypassed.

2. Unique Proposal Per Competition: The unique_together constraint on (competition, freelancer) ensures a freelancer cannot submit twice. This is enforced at both the model level and the serializer level.

3. Status Machine: Competition status transitions follow a strict directed graph. No transition outside the defined paths is allowed. This is enforced in the CompetitionStatusSerializer, not at the model level, so the admin can override if needed.

4. Payment Auto-Creation: When a winner is selected via the SelectWinnerView, a PaymentRecord is automatically created in PENDING status. No separate endpoint is needed to initiate payment.

5. Denormalized Ratings: UserRating is intentionally denormalized for read performance. It is updated via a post_save signal on Review, not on every read.

6. File Storage: In this project, files are stored on the local filesystem via MEDIA_ROOT. For production deployment, this should be migrated to object storage (e.g., AWS S3 or MinIO).

7. Email Verification: The email_verified field is present in the model but email sending is not implemented in this backend scope. It is reserved for future integration.

8. Admin Role: ADMIN users cannot be created via the registration endpoint. They must be created via python manage.py createsuperuser or via the admin panel.

---

## Local Development Quick Reference

Start WampServer and verify MySQL is running on port 3306.

Create the database:
    Open phpMyAdmin or MySQL console
    Run: CREATE DATABASE freelance_arena_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Set environment variables (Windows):
    set DB_USER=root
    set DB_PASSWORD=
    set DB_NAME=freelance_arena_db
    set SECRET_KEY=your-secret-key-here

Apply migrations and start:
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Run scheduled commands manually during development:
    python manage.py close_expired_competitions
    python manage.py remind_deadlines

Run tests:
    python manage.py test

---

## Folder Structure Expected

freelance_arena/
    freelance_arena/
        __init__.py
        settings.py
        urls.py
        wsgi.py
        asgi.py
        middleware.py
        exceptions.py
        utils.py
    accounts/
        __init__.py
        apps.py
        admin.py
        models.py
        serializers.py
        views.py
        urls.py
        permissions.py
        tests.py
    competitions/
        __init__.py
        apps.py
        admin.py
        models.py
        serializers.py
        views.py
        urls.py
        filters.py
        signals.py
        tests.py
        management/
            __init__.py
            commands/
                __init__.py
                close_expired_competitions.py
                remind_deadlines.py
    proposals/
        __init__.py
        apps.py
        admin.py
        models.py
        serializers.py
        views.py
        urls.py
        signals.py
        tests.py
    feedback/
        __init__.py
        apps.py
        admin.py
        models.py
        serializers.py
        views.py
        urls.py
        signals.py
        tests.py
    notifications/
        __init__.py
        apps.py
        admin.py
        models.py
        serializers.py
        views.py
        urls.py
        utils.py
        tests.py
    payments/
        __init__.py
        apps.py
        admin.py
        models.py
        serializers.py
        views.py
        urls.py
        tests.py
    media/
        profile_pictures/
        proposal_attachments/
    requirements.txt
