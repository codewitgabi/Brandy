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
			"rating",
			"likes",
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
		fields = ("cloth", "image")
	
	def create(self, validated_data):
		# Get request object
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


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		exclude = ("id",)
		
	def create(self, validated_data):
		# Get request object
		request = self.context.get("request")
		if request:
			user = request.user
		comment = Comment.objects.create(
			user=user,
			comment=validated_data.get("comment"),
			cloth=validated_data.get("cloth")
		)
		
		comment.save()
		return comment


class RetrieveCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cloth
		fields = (
			"comments",
		)


class ClothRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClothRating
		fields = (
			"cloth",
			"rating",
			"feedback"
		)
	
	def create(self, validated_data):
		# Get request object
		cloth = validated_data.get("cloth")
		feedback = validated_data.get("feedback")
		rating = validated_data.get("rating")
		request = self.context.get("request")
		
		if request:
			user = request.user
		
		if not ClothRating.objects.filter(user=user, cloth=cloth).exists():
			new_rating = ClothRating.objects.create(
				user=user,
				cloth=cloth,
				feedback=feedback,
				rating=rating)
			new_rating.save()
		else:
			new_rating = ClothRating.objects.get(user=user, cloth=cloth)
			new_rating.feedback = feedback
			new_rating.rating = rating
			new_rating.save()
			
		return new_rating


class ClothLikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClothLike
		fields = (
			"cloth",
		)
		
	def create(self, validated_data):
		# Get request object
		cloth = validated_data.get("cloth")
		request = self.context.get("request")
		
		if request:
			user = request.user
		
		if not ClothLike.objects.filter(user=user, cloth=cloth).exists():
			like = ClothLike.objects.create(user=user, cloth=cloth)
			like.save()
		else:
			like = ClothLike.objects.get(user=user, cloth=cloth)

		return like;


class CardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Card
		fields = (
			"owner",
			"name",
			"card_number",
			"expiry_date",
			"cvv",
		)


class AmountSerializer(serializers.Serializer):
	amount_paid = serializers.DecimalField(
		max_digits=8, decimal_places=2, default=0.00)

