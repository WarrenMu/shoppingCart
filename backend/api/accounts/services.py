from .models import Address, TwoFactorAuth, UserNotification, UserSettings, UserActivityLog, UserRole, UserPermission, UserSession, PasswordResetRequest
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

# Service functions for account-related operations
def create_user(username, email, password):
    """
    Handles creating a new user, including password validation.
    """
    # Validate password
    try:
        validate_password(password)
    except Exception as e:
        raise ValidationError({"password": list(e.messages)})

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def update_user_settings(user, receive_newsletter=None, dark_mode=None):
    """
    Updates user settings.
    """
    settings, created = UserSettings.objects.get_or_create(user=user)
    if receive_newsletter is not None:
        settings.receive_newsletter = receive_newsletter
    if dark_mode is not None:
        settings.dark_mode = dark_mode
    settings.save()
    return settings

def log_user_activity(user, activity_type, description=""):
    """
    Logs user activity.
    """
    log = UserActivityLog(user=user, activity_type=activity_type, description=description)
    log.save()
    return log

def create_password_reset_request(user):
    """
    Creates a password reset request for the user.
    """
    import uuid
    reset_token = str(uuid.uuid4())
    reset_request = PasswordResetRequest(user=user, reset_token=reset_token)
    reset_request.save()
    return reset_request

def create_user_session(user, expires_at):
    """
    Creates a new user session.
    """
    import uuid
    session_token = str(uuid.uuid4())
    session = UserSession(user=user, session_token=session_token, expires_at=expires_at)
    session.save()
    return session  

def enable_two_factor_auth(user, auth_method):
    """
    Enables two-factor authentication for the user.
    """
    two_fa, created = TwoFactorAuth.objects.get_or_create(user=user, auth_method=auth_method)
    two_fa.is_enabled = True
    two_fa.save()
    return two_fa

def create_user_notification(user, notification_type):
    """
    Creates a user notification.
    """
    notification = UserNotification(user=user, notification_type=notification_type)
    notification.save()
    return notification

