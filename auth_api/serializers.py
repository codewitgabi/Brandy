from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import random
from account.models import Otp

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			"id",
			"username",
			"email",
			"image",
			"followers",
			"following",
		)
		extra_kwargs = {
			"email": {"write_only": True}
		}
		

class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(
		style={'input_type': 'password'},
		required=True,
		min_length=10)
		
	class Meta:
		model = User
		fields = (
			"id",
			"username",
			"email",
			"password"
		)
		extra_kwargs = {
			"password": {"write_only": True},
			"id": {"read_only": True}
		}
			
	def create(self, validated_data):
		""" Get request object """
		request = self.context["request"]
		username = validated_data.get("username")
		email = validated_data.get("email")
		password = validated_data.get("password")
		
		user = User.objects.create_user(
			username= username,
			email= email,
			password= password)
			
		user.is_active = False
		user.save()
		
		token = "".join(random.choices("1234567890", k=5))
		
		""" create otp """
		otp = Otp.objects.create(user=user, token=token)
		otp.save()
		
		""" send mail """
		subject = "Otp Verification"
		html_content = render_to_string("otp.html", {"token": token})
		mail = EmailMessage(
			subject,
			html_content,
			to=[email]
		)
		
		mail.content_subtype = "html"
		mail.fail_silently = False
		mail.send()
		
		return user;

	def validate_password(self, value):
		symbols = "@#_~[]{}()$&?%/"
		
		""" MinimumLengthValidator """
		if len(value) < 10:
			raise serializers.ValidationError("Password is too short.")
		
		""" CommonPasswordValidator """
		if value.isdigit() or value.isalpha():
			raise serializers.ValidationError("Password is too common.")
		
		""" NoSymbolValidator """
		if not any([sym in symbols for sym in value]):
			raise serializers.ValidationError(f"Password should contain any of {symbols}")
			
		return value;
		

class ChangePasswordSerializer(serializers.Serializer):
	class Meta:
		model = User
		
		old_password = serializers.CharField(
			style={'input_type': 'password'},
			required=True,
			min_length=10)
			
		new_password1 = serializers.CharField(
			style={'input_type': 'password'},
			required=True,
			min_length=10)
			
		new_password2 = serializers.CharField(
			style={'input_type': 'password'},
			required=True,
			min_length=10)
			

class OtpSerializer(serializers.Serializer):
	class Meta:
		model = Otp
		fields = ["user.email"]
		
		