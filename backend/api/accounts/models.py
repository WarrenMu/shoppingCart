from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receive_newsletter = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Settings"   

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"
    
class UserRole(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    permissions = models.TextField()

    def __str__(self):
        return self.role_name   
    
class UserPermission(models.Model):
    permission_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.permission_name 
    
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Session for {self.user.username} created at {self.created_at}" 
    
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=255, unique=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Password reset request for {self.user.username} at {self.requested_at}"    
    
class TwoFactorAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_method = models.CharField(max_length=50)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"2FA for {self.user.username} - {'Enabled' if self.is_enabled else 'Disabled'}" 

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type}"  
    
class UserLoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"Login for {self.user.username} at {self.login_time} from {self.ip_address}"    
    
class AccountVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_token = models.CharField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Account verification for {self.user.username} - {'Verified' if self.is_verified else 'Not Verified'}"  
    
class UserActivitySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_logins = models.IntegerField(default=0)
    total_actions = models.IntegerField(default=0)
    last_active = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Activity summary for {self.user.username}" 
    
class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_name = models.CharField(max_length=100)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Badge {self.badge_name} for {self.user.username}"  
    
class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Subscription {self.subscription_type} for {self.user.username}"    
    
class UserReferral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    referred_email = models.EmailField()
    referred_at = models.DateTimeField(auto_now_add=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"Referral by {self.user.username} to {self.referred_email}"     
    
class UserActivityPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    awarded_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.points} points for {self.user.username} - {self.reason}"
    
     
class UserLanguagePreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)

    def __str__(self):
        return f"Language preference for {self.user.username} - {self.language_code}"
    
