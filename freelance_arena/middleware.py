from django.utils import timezone


class UpdateLastSeenMiddleware:
    """
    Middleware that updates the authenticated user's last_seen field.
    Only updates if the last seen was more than 5 minutes ago to avoid
    excessive database writes.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            now = timezone.now()
            last_seen = request.user.last_seen
            # Only update if last_seen is None or more than 5 minutes ago
            if last_seen is None or (now - last_seen).total_seconds() > 300:
                # Use update() to avoid triggering signals and save overhead
                from accounts.models import User
                User.objects.filter(pk=request.user.pk).update(last_seen=now)

        return response
