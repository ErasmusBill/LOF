from ast import mod
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings



# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN","admin"),
        ("REGULAR_USER","regular_user")
    )
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="REGULAR_USER")
    avatar = models.ImageField(upload_to="avatar/",null=True,blank=True)
    # token = models.CharField(max_length=64, unique=True)
    # is_active = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    # def save(self, *args, **kwargs):
    #     if not self.token:
    #         self.token = get_random_string(64)
    #     super().save(*args, **kwargs)

    # def is_valid(self):
    #     expiration_time = self.created_at + timezone.timedelta(hours=1)
    #     return timezone.now() < expiration_time
    
    
    # def send_register_email_token(self):
    #     activation_link = f"http://localhost:8000/authentication/send_verify_account/{self.token}/"
    #     subject = "Account activation"
    #     message = f"Click the link below to activate your account:\n{activation_link}\nThis link will expire in 1 hour."
    #     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
    
    
    def __str__(self) -> str:
        return self.username
    
    
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(64)
        super().save(*args, **kwargs)

    def is_valid(self):
        expiration_time = self.created_at + timezone.timedelta(hours=1)
        return timezone.now() < expiration_time and not self.is_used

    def send_reset_email(self):
        reset_link = f"{settings.BASE_URL}/{self.token}/"
        subject = "Password Reset Request"
        message = f"Click the link below to reset your password:\n{reset_link}\nThis link will expire in 1 hour."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.user.email])

    def __str__(self):
        return f"PasswordResetRequest for {self.user.email} at {self.created_at}"

class Tithe(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    
   
    def __str__(self):
        return f"{self.user.username} - ₵{self.amount} on {self.date}"