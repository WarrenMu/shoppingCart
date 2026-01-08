from django.urls import path
from . import views

urlpatterns = [
    # Define your shop-related URL patterns here
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('settings/', views.UserSettingsView.as_view(), name='user_settings'),
    path('activity_log/', views.UserActivityLogView.as_view(), name='user_activity_log'),
    path('password_reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('session/', views.UserSessionView.as_view(), name='user_session'),
    path('two_factor_auth/', views.TwoFactorAuthView.as_view(), name='two_factor_auth'),
    path('notifications/', views.UserNotificationView.as_view(), name='user_notifications'),

]