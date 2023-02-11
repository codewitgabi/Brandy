""" django imports """
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

""" custom models imports """
from account.models import Otp
from .serializers import (
	RegisterSerializer,
	UserSerializer,
	ChangePasswordSerializer,
	OtpSerializer)
	
""" rest_framework imports """
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.serializers import AuthTokenSerializer

""" regular imports """
import random

User = get_user_model()


class RegisterView(generics.GenericAPIView):
	serializer_class = RegisterSerializer
	
	def post(self, request, *args, **kwargs):
	       serializer = self.get_serializer(data=request.data)
	       serializer.is_valid(raise_exception=True)
	       user = serializer.save()
	       return Response({
	       	"user": UserSerializer(
	       		user,
	       		context= self.get_serializer_context()).data,
			})


@api_view(["GET"])
def verify_OTP(request, otp):
	""" 
	Verifies user account by sending the otp passed in the url
	"""
	if request.method == "GET":
		try:
			otp_obj = Otp.objects.get(token=otp, valid=True)
			if otp_obj.has_expired:
				return Response({
					"status": "failed",
					"message": "The given otp has expired"
				}, status= status.HTTP_404_NOT_FOUND)
			else:
				""" Activate user account """
				user = Otp.objects.get(token=otp).user
				user.is_active = True
				user.save()
				""" Make code invalid """
				otp_obj.valid = False
				otp_obj.save()
				return Response({
					"status": "success",
					"message": "verification complete"
				}, status= status.HTTP_200_OK)
				
		except Otp.DoesNotExist:
			return Response({
				"status": "failed",
				"message": "The given otp does not exist"
			}, status= status.HTTP_404_NOT_FOUND)
			

class ResendOtpView(generics.UpdateAPIView):
	serializer_class = OtpSerializer
	model = User
	
	def update(self, request, *args, **kwargs):
		email = request.data.get("email")
		try:
			user = User.objects.get(email=email)
			""" create otp """
			token = "".join(random.choices("1234567890", k=5))
			otp = Otp.objects.create(user=user, token=token)
			otp.save()
			
			""" send otp """
			subject = "Resent Otp Verification"
			html_content = render_to_string("otp.html", {"token": token})
			mail = EmailMessage(
				subject,
				html_content,
				to=[email]
			)
				
			mail.content_subtype = "html"
			mail.fail_silently = False
			mail.send()
			
			return Response({"status": "success"}, status=status.HTTP_200_OK)
				
		except User.DoesNotExist:
			return Response({
				"status": "failure",
				"message": "Invalid credential provided"},
				status=status.HTTP_404_NOT_FOUND)
		

class LogoutView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	
	def post(self, request):
		try:
			refresh_token = request.data["refresh_token"]
			token = RefreshToken(refresh_token)
			token.blacklist()
			
			return Response({
				"status": "success"
			}, status=status.HTTP_205_RESET_CONTENT)
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		

class ChangePassword(generics.UpdateAPIView):
	serializer_class = ChangePasswordSerializer
	permission_classes = (permissions.IsAuthenticated,)
	model = User
		
	def update(self, request, *args, **kwargs):
		user = self.request.user
		serializer = self.get_serializer(data=request.data)
		
		if serializer.is_valid():
			"""
			Get Passwords
			"""
			old_password = request.data.get("old_password")
			new_password1 = request.data.get("new_password1")
			new_password2 = request.data.get("new_password2")
			
			if not user.check_password(old_password):
				return Response(
					{"error": "Value for old password is incorrect"
					}, status=status.HTTP_400_BAD_REQUEST)
				
			if old_password == new_password1:
				return Response({
					"status": "failed",
					"error": "New password cannot have same value as old password"},
					status=status.HTTP_400_BAD_REQUEST)
			
			if new_password1 != new_password2:
				return Response({
					"status": "failed",
					"error": "Passwords do not match"},
					status=status.HTTP_400_BAD_REQUEST)
				
			user.set_password(new_password1)
			user.save()
			
			return Response({
				"status": "success",
				"message": "Password reset was successful!",
			}, status=status.HTTP_200_OK)
			
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		
