from django.shortcuts import render
from rest_framework import generics
from .serializers import (
	RegisterSerializer,
	UserSerializer,
	ChangePasswordSerializer)
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import get_user_model
from rest_framework import status

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
			

class AppLoginView(KnoxLoginView):
	permission_classes = (permissions.AllowAny,)
	
	def post(self, request, format=None):
		serializer = AuthTokenSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		login(request, user)
		return super(AppLoginView, self).post(request, format=None)
		

class ChangePassword(generics.UpdateAPIView):
	serializer_class = ChangePasswordSerializer
	permission_classes = (permissions.IsAuthenticated,)
	model = User
	
	
	def update(self, request, *args, **kwargs):
		user = self.request.user
		serializer = self.get_serializer(data=request.data)
		print(request.data)
		
		if serializer.is_valid():
			"""
			Get Passwords
			"""
			old_password = request.data.get("old_password")
			new_password = request.data.get("new_password")
			
			if not user.check_password(old_password):
				return Response(
					{
						"error": "Value for old password is incorrect"
					}, status=status.HTTP_400_BAD_REQUEST
				)
				
			if old_password == new_password:
				return Response(
					{
						"status": "failed",
						"error": "New password cannot have same value as old password"
					},
					status=status.HTTP_400_BAD_REQUEST
				)
				
			user.set_password(new_password)
			user.save()
			
			return Response({
				"status": "success",
				"message": "Password reset was successful!",
			}, status=status.HTTP_200_OK)
			
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		