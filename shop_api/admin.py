from django.contrib import admin
from .models import *


class ClothImageInline(admin.TabularInline):
	model = ClothImage
	

@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
	inlines = [ClothImageInline]
	list_display = ("uploader", "category", "size", "material_type")
	
	
admin.site.register(SubCategory)
admin.site.register(Color)
admin.site.register(Material)
admin.site.register(ClothImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ClothRating)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(FAQ)

