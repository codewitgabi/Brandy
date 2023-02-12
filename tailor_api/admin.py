from django.contrib import admin
from .models import Tailor, Rating


@admin.register(Tailor)
class TailorAdmin(admin.ModelAdmin):
	list_display = ("skill", "experience")
	search_fields = ("skill", "experience", "experience", "bank")
	list_filter = ("skill", "experience", "bank")
	

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	list_display = ("rating", "tailor")
	list_filter = ("rating",)
	
	