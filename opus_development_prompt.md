# Full Development Prompt: Competitive Freelancing Platform Backend
# Target Model: Claude Opus 4.6
# Stack: Django + MySQL (WampServer)

---

## ROLE AND OBJECTIVE

You are a senior Django backend engineer. Your task is to fully develop, from scratch, a production-ready REST API backend for a Competitive Freelancing Platform. This is a university graduation project built on Django (Python) with a MySQL database hosted via WampServer on localhost. You will write every file, every model, every view, every URL, every serializer, and every configuration without stopping until the entire system is complete and fully functional. Do not summarize. Do not skip steps. Do not leave placeholders. Every block of code must be complete and immediately executable.

---

## PROJECT CONTEXT

The platform is called FreelanceArena. It operates as follows:

A client posts a job by writing a detailed description and setting a clear deadline. Instead of selecting a freelancer upfront, the job becomes an open competition. Freelancers browse available competitions, ask questions or request clarifications, then submit either a complete deliverable or a working prototype as their proposal. The client reviews all proposals in isolation (freelancers cannot see each other's submissions), rates them with incremental feedback, and ultimately selects the winning proposal. The winning freelancer receives payment. Losing freelancers receive no payment but may receive feedback.

---

## TECHNICAL REQUIREMENTS

- Python 3.10+
- Django 4.2+
- Django REST Framework (DRF) 3.14+
- mysqlclient for MySQL connectivity
- djangorestframework-simplejwt for JWT authentication
- django-cors-headers for CORS
- Pillow for file/image handling
- django-filter for filtering querysets
- WampServer running MySQL on localhost:3306
- Database name: freelance_arena_db
- All API responses must be JSON
- Authentication: JWT (access + refresh tokens)
- Role-based access control: CLIENT, FREELANCER, ADMIN
- File uploads stored in MEDIA_ROOT
- Full input validation on all endpoints
- Proper HTTP status codes on all responses
- No frontend required, this is a pure backend API

---

## STEP 1: PROJECT INITIALIZATION

Generate the exact terminal commands to:
2. Install all required packages (provide the full pip install command)
3. Create the Django project named freelance_arena
4. Create the following Django apps:
   - accounts (user management and authentication)
   - competitions (job postings and competition management)
   - proposals (freelancer submissions)
   - feedback (ratings and reviews)
   - notifications (in-app notification system)
   - payments (payment tracking)

After showing the commands, immediately write every file.

---

## STEP 2: SETTINGS CONFIGURATION

Write the complete settings.py file with no omissions. It must include:

- SECRET_KEY using os.environ.get with a fallback
- DEBUG = True for development
- ALLOWED_HOSTS including localhost and 127.0.0.1
- INSTALLED_APPS listing all six apps and all third-party packages
- DATABASES configured for MySQL with host=127.0.0.1, port=3306, name=freelance_arena_db, user and password read from environment variables with fallback to root and empty string
- REST_FRAMEWORK settings:
  - DEFAULT_AUTHENTICATION_CLASSES using JWTAuthentication
  - DEFAULT_PERMISSION_CLASSES using IsAuthenticated
  - DEFAULT_FILTER_BACKENDS including DjangoFilterBackend, SearchFilter, OrderingFilter
  - DEFAULT_PAGINATION_CLASS using PageNumberPagination with PAGE_SIZE=10
- SIMPLE_JWT settings with ACCESS_TOKEN_LIFETIME of 60 minutes and REFRESH_TOKEN_LIFETIME of 7 days
- CORS_ALLOWED_ORIGINS including localhost:3000 and localhost:8080
- MEDIA_URL and MEDIA_ROOT pointing to a media folder inside the project
- AUTH_USER_MODEL = 'accounts.User'
- STATIC_URL

---

## STEP 3: ACCOUNTS APP - FULL IMPLEMENTATION

Write every file in the accounts app.

### accounts/models.py

Define a custom User model extending AbstractBaseUser and PermissionsMixin with the following fields:
- id: UUID primary key, auto-generated
- email: unique, used as USERNAME_FIELD
- username: unique, max 50 chars
- first_name, last_name: max 100 chars each
- role: CharField with choices CLIENT, FREELANCER, ADMIN
- bio: TextField, blank and null allowed
- profile_picture: ImageField, upload_to='profile_pictures/', blank and null allowed
- skills: TextField blank and null (comma-separated list for freelancers)
- hourly_rate: DecimalField max_digits=10 decimal_places=2, null and blank allowed
- is_active: BooleanField default True
- is_staff: BooleanField default False
- date_joined: DateTimeField auto_now_add
- last_seen: DateTimeField null and blank allowed
- email_verified: BooleanField default False

Define a custom manager UserManager with create_user and create_superuser methods that handle email normalization and password hashing correctly.

### accounts/serializers.py

Write the following serializers completely:

1. UserRegistrationSerializer: validates email uniqueness, validates password length minimum 8 characters, validates role is either CLIENT or FREELANCER (not ADMIN), hashes password on create using set_password.

2. UserLoginSerializer: accepts email and password, authenticates using Django authenticate, raises validation error with message "Invalid credentials" if authentication fails, raises validation error with message "Account is deactivated" if user is_active is False.

3. UserProfileSerializer: read and write serializer for profile updates, read_only fields include id, email, date_joined, role. Handles profile_picture as ImageField with max size validation of 2MB. Validates skills field format.

4. ChangePasswordSerializer: requires old_password, new_password, confirm_password. Validates old password is correct. Validates new and confirm match. Validates new password is at least 8 characters.

5. AdminUserSerializer: full user detail for admin use, includes all fields.

### accounts/views.py

Write all views as class-based views using DRF APIView or GenericAPIView:

1. RegisterView: POST only, no authentication required. Creates user, returns user data and JWT tokens in response with status 201.

2. LoginView: POST only, no authentication required. Returns access and refresh tokens along with user role and id.

3. LogoutView: POST, authenticated. Blacklists the refresh token provided in the request body. Returns 200 on success.

4. ProfileView: GET returns own profile. PUT/PATCH updates own profile. DELETE deactivates (sets is_active=False) own account. All authenticated.

5. ChangePasswordView: POST, authenticated. Validates and updates password.

6. UserListView: GET only, admin only (role check). Returns paginated list of all users with filters for role and is_active.

7. UserDetailAdminView: GET, PUT, DELETE. Admin only. Manage any user account.

8. FreelancerSearchView: GET, no authentication required. Search freelancers by skills and username. Returns paginated results.

### accounts/urls.py

Write complete URL configuration with named URL patterns for all views above.

### accounts/permissions.py

Write the following custom permission classes:
- IsClient: returns True if request.user.role == 'CLIENT'
- IsFreelancer: returns True if request.user.role == 'FREELANCER'
- IsAdminRole: returns True if request.user.role == 'ADMIN'
- IsOwnerOrAdmin: returns True if object.user == request.user or request.user.role == 'ADMIN'

### accounts/admin.py

Register the User model with the Django admin site with list_display, list_filter, search_fields, and fieldsets configured properly.

---

## STEP 4: COMPETITIONS APP - FULL IMPLEMENTATION

Write every file in the competitions app.

### competitions/models.py

Define the following models:

1. Competition:
   - id: UUID primary key
   - client: ForeignKey to User, limit_choices_to role=CLIENT, on_delete=CASCADE, related_name='competitions'
   - title: CharField max 200 chars
   - description: TextField
   - requirements: TextField (detailed technical requirements)
   - budget: DecimalField max_digits=12 decimal_places=2
   - currency: CharField max 3, default 'USD'
   - deadline: DateTimeField (when the competition closes)
   - submission_deadline: DateTimeField (when proposals must be submitted by)
   - status: CharField with choices DRAFT, OPEN, REVIEW, CLOSED, CANCELLED, default DRAFT
   - category: CharField max 100
   - tags: TextField blank (comma-separated)
   - max_proposals: PositiveIntegerField null and blank (None means unlimited)
   - allow_questions: BooleanField default True
   - created_at: DateTimeField auto_now_add
   - updated_at: DateTimeField auto_now
   - winner: ForeignKey to User null and blank, related_name='won_competitions'
   - winning_proposal: ForeignKey to proposals.Proposal null and blank, related_name='won_for'

   Add a property is_open that returns True if status is OPEN and submission_deadline has not passed.
   Add a property proposal_count that returns count of proposals for this competition.

2. CompetitionQuestion:
   - id: UUID primary key
   - competition: ForeignKey to Competition on_delete=CASCADE related_name='questions'
   - asked_by: ForeignKey to User on_delete=CASCADE related_name='questions_asked'
   - question: TextField
   - answer: TextField null and blank
   - answered_at: DateTimeField null and blank
   - answered_by: ForeignKey to User null and blank related_name='questions_answered'
   - is_public: BooleanField default True (if True all freelancers can see the answer)
   - created_at: DateTimeField auto_now_add

3. CompetitionBookmark:
   - id: UUID primary key
   - competition: ForeignKey to Competition on_delete=CASCADE related_name='bookmarks'
   - user: ForeignKey to User on_delete=CASCADE related_name='bookmarks'
   - created_at: DateTimeField auto_now_add
   Meta: unique_together = ('competition', 'user')

### competitions/serializers.py

Write the following serializers:

1. CompetitionListSerializer: lightweight for list views, includes id, title, client username, budget, currency, deadline, status, category, proposal_count, is_open, created_at. Read only.

2. CompetitionDetailSerializer: full detail including all fields, nested questions (public ones only), client profile info. Read only.

3. CompetitionCreateSerializer: for creating competitions, validates deadline is in the future, validates submission_deadline is before deadline, validates budget is positive, validates max_proposals is positive if provided. On create sets status to DRAFT and client to request.user.

4. CompetitionUpdateSerializer: for updating by client owner, only allows updating title, description, requirements, budget, deadline, submission_deadline, tags, max_proposals, allow_questions, category. Validates same rules as create. Does not allow changing status through this serializer.

5. CompetitionStatusSerializer: only used to change status. Validates state machine transitions: DRAFT can go to OPEN or CANCELLED. OPEN can go to REVIEW or CANCELLED. REVIEW can go to CLOSED. CLOSED and CANCELLED are terminal states.

6. CompetitionQuestionSerializer: for creating and reading questions. On create sets asked_by to request.user and verifies user is a FREELANCER.

7. CompetitionAnswerSerializer: for answering a question. Validates request.user is the competition client. Sets answered_by and answered_at.

### competitions/views.py

Write all views:

1. CompetitionListView: GET returns paginated list of all OPEN competitions. Supports filter by category, status (if admin), search by title and description, ordering by budget, deadline, created_at. No authentication required.

2. CompetitionCreateView: POST, CLIENT only. Creates a competition.

3. CompetitionDetailView: GET returns full competition detail. No authentication required. PUT/PATCH for client owner to update (only when DRAFT or OPEN). DELETE for client owner (only when DRAFT, sets status to CANCELLED instead of deleting).

4. CompetitionStatusView: POST, CLIENT owner only. Changes status according to state machine.

5. MyCompetitionsView: GET, CLIENT only. Returns own competitions with all statuses including DRAFT. Supports status filter.

6. CompetitionQuestionListCreateView: GET returns public questions for a competition (no auth required for public questions). POST for authenticated FREELANCERs only to ask questions.

7. CompetitionAnswerView: POST, competition's CLIENT owner only. Answer a specific question.

8. CompetitionBookmarkView: POST toggles bookmark for authenticated user. GET returns list of user's bookmarked competitions.

9. SelectWinnerView: POST, CLIENT owner only. Accepts proposal_id in body. Validates competition is in REVIEW status. Sets winning_proposal and winner on competition. Sets competition status to CLOSED. Triggers payment record creation. Returns updated competition detail.

### competitions/urls.py

Write complete URL configuration.

### competitions/filters.py

Write a CompetitionFilter class using django_filters.FilterSet with filters for category, status, budget_min, budget_max, deadline_before, deadline_after, tags (contains search).

---

## STEP 5: PROPOSALS APP - FULL IMPLEMENTATION

Write every file in the proposals app.

### proposals/models.py

Define the following models:

1. Proposal:
   - id: UUID primary key
   - competition: ForeignKey to Competition on_delete=CASCADE related_name='proposals'
   - freelancer: ForeignKey to User limit_choices_to role=FREELANCER on_delete=CASCADE related_name='proposals'
   - title: CharField max 200
   - description: TextField (explanation of the approach and solution)
   - proposed_budget: DecimalField max_digits=12 decimal_places=2
   - estimated_duration: PositiveIntegerField (in days)
   - status: CharField choices SUBMITTED, UNDER_REVIEW, ACCEPTED, REJECTED, WITHDRAWN, default SUBMITTED
   - submission_note: TextField blank
   - created_at: DateTimeField auto_now_add
   - updated_at: DateTimeField auto_now
   - client_score: PositiveIntegerField null and blank (1 to 5 rating from client)
   - client_note: TextField null and blank (incremental feedback from client)
   - is_winner: BooleanField default False
   Meta: unique_together = ('competition', 'freelancer') to prevent duplicate submissions

2. ProposalAttachment:
   - id: UUID primary key
   - proposal: ForeignKey to Proposal on_delete=CASCADE related_name='attachments'
   - file: FileField upload_to='proposal_attachments/'
   - original_filename: CharField max 255
   - file_size: PositiveIntegerField (bytes)
   - file_type: CharField max 50
   - uploaded_at: DateTimeField auto_now_add
   - description: CharField max 255 blank

3. ProposalRevision:
   - id: UUID primary key
   - proposal: ForeignKey to Proposal on_delete=CASCADE related_name='revisions'
   - revised_by: ForeignKey to User on_delete=CASCADE
   - description: TextField (what was changed)
   - revision_number: PositiveIntegerField
   - created_at: DateTimeField auto_now_add

### proposals/serializers.py

Write the following serializers:

1. ProposalAttachmentSerializer: handles file upload, validates file size max 10MB, validates file types (pdf, doc, docx, zip, jpg, jpeg, png, mp4), sets original_filename and file_size and file_type automatically from the uploaded file.

2. ProposalCreateSerializer: validates competition is OPEN, validates freelancer has not already submitted a proposal (unique check), validates competition's submission_deadline has not passed, validates competition's max_proposals limit has not been reached, validates proposed_budget is positive. On create sets freelancer to request.user. Includes nested ProposalAttachmentSerializer as write-only for initial attachments.

3. ProposalDetailSerializer: full detail for proposal owner (freelancer) or competition client. Freelancer can see all fields of their own proposal. Client can see all proposals for their competition but the is_winner and client_score/client_note are restricted from freelancers viewing their own proposal before the competition closes.

4. ProposalListSerializer: lightweight list for freelancer's own proposals. Includes competition title, status, created_at, proposed_budget.

5. ClientProposalListSerializer: for client viewing proposals on their competition. Must NOT expose the freelancer's identity or other proposals' details in list view (blind review enforcement). Only shows proposal id, title, proposed_budget, estimated_duration, created_at, client_score.

6. ClientScoreSerializer: for client to add score and feedback to a proposal. Validates score is between 1 and 5. Validates competition is in OPEN or REVIEW status.

7. ProposalWithdrawSerializer: allows freelancer to withdraw their own proposal. Validates status is SUBMITTED. Changes status to WITHDRAWN.

### proposals/views.py

Write all views with strict permission enforcement:

1. ProposalCreateView: POST, FREELANCER only. Validates and creates proposal with attachments.

2. MyProposalsView: GET, FREELANCER only. Returns paginated list of own proposals with optional competition filter and status filter.

3. ProposalDetailView: GET, FREELANCER owner or competition CLIENT only. Freelancer can GET, PUT (only when SUBMITTED), DELETE (sets to WITHDRAWN). Client can GET.

4. AddAttachmentView: POST, FREELANCER owner only. Adds attachment to existing proposal. Proposal must be SUBMITTED.

5. DeleteAttachmentView: DELETE, FREELANCER owner only. Deletes a specific attachment. Proposal must be SUBMITTED.

6. CompetitionProposalsView: GET, competition CLIENT owner only. Returns all proposals for their competition. Uses ClientProposalListSerializer to enforce blind review. Supports ordering by client_score and created_at.

7. ScoreProposalView: POST, competition CLIENT owner only. Adds or updates score and feedback for a specific proposal.

8. WithdrawProposalView: POST, FREELANCER owner only. Withdraws proposal.

### proposals/urls.py

Write complete URL configuration.

---

## STEP 6: FEEDBACK APP - FULL IMPLEMENTATION

Write every file in the feedback app.

### feedback/models.py

Define the following models:

1. Review:
   - id: UUID primary key
   - reviewer: ForeignKey to User on_delete=CASCADE related_name='reviews_given'
   - reviewee: ForeignKey to User on_delete=CASCADE related_name='reviews_received'
   - competition: ForeignKey to Competition on_delete=CASCADE related_name='reviews'
   - rating: PositiveIntegerField (1 to 5)
   - comment: TextField
   - review_type: CharField choices CLIENT_TO_FREELANCER, FREELANCER_TO_CLIENT
   - created_at: DateTimeField auto_now_add
   - is_public: BooleanField default True
   Meta: unique_together = ('reviewer', 'competition') to prevent duplicate reviews per competition

2. UserRating (denormalized for performance):
   - user: OneToOneField to User on_delete=CASCADE related_name='rating'
   - average_rating: DecimalField max_digits=3 decimal_places=2 default 0.00
   - total_reviews: PositiveIntegerField default 0
   - updated_at: DateTimeField auto_now

   Add a classmethod update_for_user(user_id) that recalculates and saves the average from all public reviews for that user.

### feedback/serializers.py

Write:
1. ReviewCreateSerializer: validates competition is CLOSED, validates reviewer participated in competition (client owns it or freelancer submitted a proposal), validates review does not already exist, validates rating is 1-5. Sets reviewer to request.user and determines review_type automatically.
2. ReviewDetailSerializer: full read-only serializer including reviewer username and profile_picture.
3. UserRatingSerializer: read-only summary of user's rating.

### feedback/views.py

Write all views:
1. CreateReviewView: POST, authenticated. Only allowed after competition is CLOSED.
2. UserReviewsView: GET, no authentication required. Returns all public reviews for a specific user by user_id.
3. CompetitionReviewsView: GET, authenticated. Returns all reviews for a competition.

### feedback/signals.py

Write post_save signal on Review model that calls UserRating.update_for_user for the reviewee whenever a review is created or updated.

### feedback/urls.py

Write complete URL configuration.

---

## STEP 7: NOTIFICATIONS APP - FULL IMPLEMENTATION

### notifications/models.py

Define:

1. Notification:
   - id: UUID primary key
   - recipient: ForeignKey to User on_delete=CASCADE related_name='notifications'
   - notification_type: CharField choices: COMPETITION_OPENED, PROPOSAL_RECEIVED, PROPOSAL_SCORED, PROPOSAL_ACCEPTED, PROPOSAL_REJECTED, COMPETITION_CLOSED, QUESTION_ANSWERED, WINNER_SELECTED, NEW_REVIEW, COMPETITION_DEADLINE_APPROACHING
   - title: CharField max 200
   - message: TextField
   - is_read: BooleanField default False
   - read_at: DateTimeField null and blank
   - related_competition_id: UUIDField null and blank
   - related_proposal_id: UUIDField null and blank
   - created_at: DateTimeField auto_now_add

### notifications/utils.py

Write a NotificationService class with the following static methods, each creating the appropriate Notification record:
- notify_proposal_received(competition, proposal): notifies the client
- notify_proposal_scored(proposal): notifies the freelancer
- notify_winner_selected(competition, winning_proposal): notifies winner and all losing freelancers separately
- notify_question_answered(question): notifies the freelancer who asked
- notify_competition_closed(competition): notifies all participating freelancers
- notify_new_review(review): notifies the reviewee

### notifications/serializers.py

Write:
1. NotificationSerializer: full read-only serializer
2. MarkReadSerializer: accepts list of notification ids to mark as read

### notifications/views.py

Write:
1. NotificationListView: GET, authenticated. Returns own notifications, unread_count in response headers or body. Supports filter by is_read and notification_type. Ordered by created_at descending.
2. MarkNotificationsReadView: POST, authenticated. Marks specified notifications as read.
3. MarkAllReadView: POST, authenticated. Marks all own notifications as read.
4. UnreadCountView: GET, authenticated. Returns just the unread count.

### notifications/urls.py

Write complete URL configuration.

---

## STEP 8: PAYMENTS APP - FULL IMPLEMENTATION

### payments/models.py

Define:

1. PaymentRecord:
   - id: UUID primary key
   - competition: OneToOneField to Competition on_delete=CASCADE related_name='payment'
   - client: ForeignKey to User on_delete=CASCADE related_name='payments_made'
   - freelancer: ForeignKey to User null and blank on_delete=SET_NULL related_name='payments_received'
   - amount: DecimalField max_digits=12 decimal_places=2
   - currency: CharField max 3 default USD
   - status: CharField choices PENDING, PROCESSING, COMPLETED, FAILED, REFUNDED default PENDING
   - platform_fee: DecimalField max_digits=10 decimal_places=2 (calculated as 10% of amount)
   - net_amount: DecimalField max_digits=12 decimal_places=2 (amount minus platform_fee)
   - created_at: DateTimeField auto_now_add
   - updated_at: DateTimeField auto_now
   - completed_at: DateTimeField null and blank
   - transaction_reference: CharField max 100 null and blank unique
   - notes: TextField blank

   Add a save override that auto-calculates platform_fee as 10% of amount and net_amount as amount minus platform_fee when amount changes.

### payments/serializers.py

Write:
1. PaymentRecordSerializer: read-only full detail for admin
2. ClientPaymentSerializer: read-only for client, shows competition, amount, status, created_at
3. FreelancerPaymentSerializer: read-only for freelancer, shows net_amount, status, completed_at

### payments/views.py

Write:
1. MyClientPaymentsView: GET, CLIENT only. Returns own payment records.
2. MyFreelancerPaymentsView: GET, FREELANCER only. Returns own payment records received.
3. PaymentDetailView: GET, payment client or payment freelancer or ADMIN only. Returns full payment detail.
4. AdminPaymentListView: GET, ADMIN only. Returns all payments with filters for status and date range.
5. UpdatePaymentStatusView: POST, ADMIN only. Updates payment status. Validates state machine: PENDING to PROCESSING, PROCESSING to COMPLETED or FAILED.

### payments/urls.py

Write complete URL configuration.

---

## STEP 9: MAIN PROJECT URLS

Write the main freelance_arena/urls.py that includes all app url configurations under the following paths:
- api/auth/ for accounts
- api/competitions/ for competitions
- api/proposals/ for proposals
- api/feedback/ for feedback
- api/notifications/ for notifications
- api/payments/ for payments
- Also configure MEDIA files serving in DEBUG mode using static() helper

---

## STEP 10: SIGNALS AND APP CONFIGS

For each app, write the AppConfig class in apps.py with the correct name and a ready() method that imports signals if the app has signals.

Write signals for:
- competitions app: when a Competition status changes to OPEN, notify all bookmarked users
- proposals app: when a Proposal is created, call NotificationService.notify_proposal_received
- proposals app: when client_score is updated on a Proposal, call NotificationService.notify_proposal_scored
- feedback app: already defined in Step 6

---

## STEP 11: MIDDLEWARE

Write a custom middleware class in freelance_arena/middleware.py called UpdateLastSeenMiddleware that updates the authenticated user's last_seen field to timezone.now() on every authenticated request. Attach it to MIDDLEWARE in settings.py after authentication middleware. Only update if the last seen was more than 5 minutes ago to avoid excessive database writes.

---

## STEP 12: MANAGEMENT COMMANDS

Write a management command at competitions/management/commands/close_expired_competitions.py that:
- Finds all competitions with status OPEN where submission_deadline has passed
- Changes their status to REVIEW
- Creates notifications for all participating freelancers using NotificationService
- Prints a summary of how many competitions were updated

Write a management command at competitions/management/commands/remind_deadlines.py that:
- Finds all OPEN competitions where submission_deadline is within 24 hours
- Creates COMPETITION_DEADLINE_APPROACHING notifications for all freelancers who have bookmarked those competitions and have not yet submitted a proposal
- Avoids creating duplicate notifications

---

## STEP 13: ADMIN CONFIGURATION

Write admin.py for each app with the following specifics:

competitions/admin.py:
- CompetitionAdmin: list_display includes title, client, status, budget, deadline, proposal_count. list_filter includes status and category. search_fields includes title and description. Actions include bulk_open, bulk_cancel.

proposals/admin.py:
- ProposalAdmin: list_display includes title, competition, freelancer, status, proposed_budget, client_score. list_filter includes status.

feedback/admin.py:
- ReviewAdmin: list_display includes reviewer, reviewee, competition, rating, review_type, is_public.

payments/admin.py:
- PaymentRecordAdmin: list_display includes competition, client, freelancer, amount, status, created_at. Actions include mark_completed, mark_failed.

notifications/admin.py:
- NotificationAdmin: list_display includes recipient, notification_type, title, is_read, created_at. list_filter includes is_read and notification_type. Action to mark_all_read for selected.

---

## STEP 14: COMPLETE API ENDPOINT REFERENCE

After writing all code, write a complete API reference table with the following columns: Method, URL, Description, Authentication Required, Permissions, Request Body Summary, Response Summary.

Cover every single endpoint across all apps.

---

## STEP 15: DATABASE SETUP INSTRUCTIONS

Write the exact steps for:
1. Opening WampServer MySQL console
2. Creating the database: CREATE DATABASE freelance_arena_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
3. Creating a dedicated user with a password and granting all privileges
4. Running python manage.py makemigrations for all apps in the correct order
5. Running python manage.py migrate
6. Creating a superuser
7. Verifying the server starts with python manage.py runserver

---

## STEP 16: ERROR HANDLING AND VALIDATION

Write a custom exception handler in freelance_arena/exceptions.py. Register it in settings.py under REST_FRAMEWORK EXCEPTION_HANDLER. It must:
- Return all errors as { "success": false, "errors": { ... }, "message": "..." }
- Handle ValidationError, NotFound, PermissionDenied, AuthenticationFailed, and generic exceptions
- Log unhandled exceptions using Python's logging module

Write a freelance_arena/utils.py with a success_response(data, message, status_code) helper that formats all success responses as { "success": true, "message": "...", "data": { ... } }.

All views must use these helpers consistently.

---

## STEP 17: TESTING

Write unit tests in tests.py for each app. For each app, write at minimum:

accounts: test registration with valid data, test registration with duplicate email, test login with valid credentials, test login with invalid credentials, test profile update, test role-based access.

competitions: test create competition as client, test create competition as freelancer (should fail), test status transitions, test asking question as freelancer, test answering question as client.

proposals: test submitting proposal as freelancer, test duplicate proposal (should fail), test submitting after deadline (should fail), test blind review enforcement (client cannot see other freelancers), test selecting winner.

feedback: test review creation after closed competition, test review after open competition (should fail), test duplicate review (should fail).

payments: test payment record creation on winner selection, test platform_fee calculation.

Use Django's TestCase with APIClient and write fixture setup in setUp().

---

## EXECUTION INSTRUCTIONS

You must write every file completely from top to bottom. No file should have a comment saying "rest of code here" or "add remaining methods." Every function must have a full implementation. Every serializer must have all its fields and validators. Every view must have full logic including error handling. Every model must have all its Meta options, __str__ methods, and any custom methods or properties described.

Begin immediately with Step 1 and do not stop until Step 17 is complete. If you finish a step, immediately continue to the next without asking for confirmation.
