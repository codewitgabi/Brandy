from django.contrib import admin
from .models import (
	Tailor,
	Rating,
	RatingImage,
	Measurement,
	TaskReminder,
	Task,
	Booking,
	WalletNotification)


@admin.register(Tailor)
class TailorAdmin(admin.ModelAdmin):
	list_display = ("skill", "experience")
	search_fields = ("skill", "experience", "experience", "bank")
	list_filter = ("skill", "experience", "bank")


class RatingImageInline(admin.TabularInline):
	model = RatingImage
	

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	list_display = ("rating", "tailor")
	list_filter = ("rating",)
	inlines = (RatingImageInline,)
	

@admin.register(TaskReminder)
class TaskReminderAdmin(admin.ModelAdmin):
	list_display = ("tailor", "task")
	
	
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ("customer", "tailor", "time_created", "due_date", "delivered")
	
	
@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
	list_display = ("user",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ("user", "tailor", "due_date", "duration")
	

@admin.register(WalletNotification)
class WalletNotificationAdmin(admin.ModelAdmin):
	list_display = ("tailor", "wallet", "date_created")


@admin.register(RatingImage)
class RatingImageAdmin(admin.ModelAdmin):
	list_display = ("image", "rating")

