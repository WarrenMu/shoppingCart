from django.contrib import admin
from .models import User, Address, TwoFactorAuth, UserSettings, UserActivityLog, UserRole, UserPermission, UserSession, PasswordResetRequest    


# Register your models here.
admin.site.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'state', 'postal_code', 'country')
    search_fields = ('user__username', 'street', 'city', 'country')

admin.site.register(TwoFactorAuth)  
class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'auth_method', 'is_enabled')
    search_fields = ('user__username', 'auth_method')

admin.site.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'receive_newsletter', 'dark_mode')
    search_fields = ('user__username',) 

admin.site.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp')
    search_fields = ('user__username', 'activity_type')

admin.site.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)
    search_fields = ('role_name',)

admin.site.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('permission_name',)
    search_fields = ('permission_name',)    

admin.site.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_token', 'created_at', 'expires_at')
    search_fields = ('user__username', 'session_token') 

admin.site.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_token', 'requested_at', 'is_used')
    search_fields = ('user__username', 'reset_token')

admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')   
