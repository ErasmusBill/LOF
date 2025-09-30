from django.contrib import admin
from .models import CustomUser,PasswordResetRequest,Tithe

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(PasswordResetRequest)
admin.site.register(Tithe)