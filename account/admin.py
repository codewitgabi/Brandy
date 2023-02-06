from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User, Otp


@admin.register(User)
class UserAdmin(BaseAdmin):
	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": ("username", "email", "password1", "password2")
		}),
	)
	
	list_display = ("username", "email")
	
	
	
@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
	list_display = ("token", "valid")
	
	