from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ClothUploadSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cloth
		fields = (
			"id",
			"description",
			"category",
			"sub_category",
			"price",
			"discount",
			"available_colors",
			"material",
			"size",
			"length",
			"image",
		)
		read_only_fields = ["id"]
		

class ClothSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cloth
		fields = (
			"id",
			"description",
			"category",
			"sub_category",
			"price",
			"discount",
			"new_price",
			"available_colors",
			"material",
			"size",
			"length",
			"image",
		)
		read_only_fields = ["id"]


class TransactionNotificationSerializer(
	serializers.ModelSerializer):
	class Meta:
		model = TransactionNotification
		fields = (
			"tailor",
			"message",
			"pay"
		)


class FavoriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Favorite
		fields = ("cloth",)
	
	def create(self, validated_data):
		request = self.context.get("request")
		cloth = validated_data.get("cloth")
		if request:
			user = request.user
		
		if not Favorite.objects.filter(user=user, cloth=cloth).exists():
			fav = Favorite.objects.create(
				user=user,
				cloth=cloth
			)
			fav.save()
		else:
			fav = Favorite.objects.get(user=user, cloth=cloth)
			
		return fav