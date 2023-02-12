from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User, Otp
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(BaseAdmin):
	fieldsets = (
		(None, {"fields": ("username", "password")}),
		(_("Personal Info"), {"fields": ("first_name", "last_name", "email", "image")}),
		("Interaction", {"fields": ("followers", "following")}),
		(
			_("Permissions"),
			{
				"fields": (
					"is_active",
					"is_staff",
					"is_superuser",
					"groups",
					"user_permissions",
				),
			},
		),
		(_("Important dates"), {"fields": ("last_login", "date_joined")}),
	)
	
	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": ("username", "email", "password1", "password2")
		}),
	)
	
	list_display = ("id", "username", "email")
	filter_horizontal = ("followers", "following")
	
	
@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
	list_display = ("token", "valid")
	
	