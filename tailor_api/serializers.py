from rest_framework import serializers
from .models import Tailor, Rating, Task, Booking, WalletNotification


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
			"skill",
			"experience",
			"location",
			"avg_rating",
			"total_ratings",
		)
		
		
class TailorRatingSerializer(serializers.Serializer):
	rating = serializers.CharField(max_length=3, min_length=3)
	
	def validate_rating(self, value):
		""" rating choices based on rating model instance """
		choices = ("1", "2", "3", "4", "5")
		
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
			"tailor",
			"feedback",
			"image",
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
			"username",
			"wallet_balance",
			"money_earned",
			"pending_money",
			"reminders",
			"task_list",
			"schedules",
			"followers_count",
			"following_count",
			"skill",
			"experience",
			"location",
			"total_ratings",
			"avg_rating",
			"completed_task"
		)
		

class TailorBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tailor
		fields = ("schedules",)


class BookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = (
			"tailor",
			"user_detail",
			"user",
			"due_date",
			"duration",
		)
		read_only_fields = ["user"]
		
		
	def create(self, validated_data):
		tailor = validated_data.get("tailor")
		due_date = validated_data.get("due_date")
		request = self.context.get("request")
		
		if request:
			user = request.user
			
		booking = Booking.objects.create(
			user=user,
			tailor=tailor,
			due_date=due_date
		)
		booking.save()
		
		return booking


class AcceptBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ("accepted", "declined")
		read_only_fields = ["declined"]
		

class DeclineBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ("accepted", "declined")
		read_only_fields = ["accepted"]


class WalletNotificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = WalletNotification
		fields = (
			"message",
			"wallet",
			"payer",
			"date_created",
		)

