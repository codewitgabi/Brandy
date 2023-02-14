from rest_framework import serializers
from .models import Tailor, Rating, Task


"""
Gets the username for a user related field
"""
class OneToOneUserField(serializers.RelatedField):
	def to_representation(self, value):
		return value.username
		

class TailorSerializer(serializers.ModelSerializer):
	user = OneToOneUserField(read_only=True)
	class Meta:
		model = Tailor
		fields = (
			"id",
			"user",
			"profile_picture",
			"followers_count",
			"following_count",
			"skill",
			"business_name",
			"phone",
			"experience",
			"business_address",
			"bank",
			"account_number",
			"wallet_balance",
			"money_earned",
			"pending_money",
			"avg_rating",
			"total_ratings",
			"task_list",
			"reminders",
		)
		
		
class TailorRatingSerializer(serializers.Serializer):
	rating = serializers.CharField(max_length=3, min_length=3)
	
	def validate_rating(self, value):
		""" rating choices based on rating model instance """
		choices = ("0.5", "1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0")
		
		if value not in choices:
			raise serializers.ValidationError("Not a valid choice")
		return value

	
class RatingSerializer(serializers.ModelSerializer):
	user = OneToOneUserField(read_only=True)
	class Meta:
		model = Rating
		fields = (
			"id",
			"user",
			"rating",
			"tailor"
		)
		read_only_fields = ("user", "id")


class CustomerListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = (
			"username",
			"address",
			"image",
			"phone",
			"measurement",
		)


class TailorDashboardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tailor
		fields = (
			"wallet_balance",
			"money_earned",
			"pending_money",
			"reminders",
			"task_list",
		)