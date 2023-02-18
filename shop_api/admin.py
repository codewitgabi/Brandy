from django.contrib import admin
from .models import *


@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
	list_display = ("uploader", "category", "sub_category", "size", "material")
	
	
admin.site.register(Favorite)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ClothRating)
admin.site.register(ClothLike)
admin.site.register(Comment)
admin.site.register(FAQ)
admin.site.register(TransactionNotification)
