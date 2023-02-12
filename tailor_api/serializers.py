from rest_framework import serializers
from .models import Tailor


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
			"skill",
			"business_name",
			"phone",
			"experience",
			"business_address",
			"bank",
			"account_number",
			"avg_rating"
		)
		
	#def create(self, validated_data):
#		user = self.request.user
		
		