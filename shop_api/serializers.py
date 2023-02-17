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
		fields = "__all__"
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
		
		