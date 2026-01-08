from django.forms import ValidationError
from django.shortcuts import render
from .services import create_user, update_user_settings, log_user_activity, create_password_reset_request, create_user_session, enable_two_factor_auth, create_user_notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CreateUserView(APIView):
    def post(self, request):
        if not all(k in request.data for k in ("username", "email", "password")):
            return Response({"error": "Missing required fields"}, status=400)
        username = request.data.get("username")
        email = request.data.get("email")   
        password = request.data.get("password")
        try:
            user = create_user(username, email, password)   
        except ValidationError as e:
            return Response({"error": e.detail}, status=400)
        return Response({"message": "User created successfully", "user_id": user.id})
    
    
class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        settings = update_user_settings(request.user)
        return Response({
            "receive_newsletter": settings.receive_newsletter,
            "dark_mode": settings.dark_mode
        })

    def post(self, request):
        receive_newsletter = request.data.get("receive_newsletter")
        dark_mode = request.data.get("dark_mode")
        settings = update_user_settings(request.user, receive_newsletter, dark_mode)
        return Response({"message": "Settings updated"})    
    
class UserActivityLogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        activity_type = request.data.get("activity_type")
        description = request.data.get("description", "")
        log = log_user_activity(request.user, activity_type, description)
        return Response({"message": "Activity logged", "log_id": log.id})      
    
class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        reset_request = create_password_reset_request(user)
        return Response({"message": "Password reset request created", "reset_token": reset_request.reset_token})    

class UserSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from datetime import datetime, timedelta
        expires_at = datetime.now() + timedelta(hours=1)
        session = create_user_session(request.user, expires_at)
        return Response({"message": "User session created", "session_token": session.session_token})    
    
class TwoFactorAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_method = request.data.get("auth_method")
        two_fa = enable_two_factor_auth(request.user, auth_method)
        return Response({"message": "Two-factor authentication enabled", "auth_method": two_fa.auth_method})    
    
class UserNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.data.get("notification_type"):
            return Response({"error": "Notification type is required"}, status=400)
        notification_type = request.data.get("notification_type")
        notification = create_user_notification(request.user, notification_type)
        return Response({"message": "User notification created", "notification_id": notification.id})
        return notification


def create_user_notification(user, notification_type):
    """
    Creates a user notification.
    """
    notification = UserNotification(user=user, notification_type=notification_type) 
    notification.save()
    return notification 

