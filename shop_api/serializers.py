from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ClothUploadSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cloth
		fields = (
			"description",
			"category",
			"sub_category",
			"price",
			"available_colors",
			"material",
			"size",
			"length",
			"image",
		)
		
		