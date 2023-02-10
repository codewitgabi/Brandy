""" django imports """
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import get_user_model

""" custom models imports """
from account.models import Otp
from .serializers import (
	RegisterSerializer,
	UserSerializer,
	ChangePasswordSerializer)
	
""" rest_framework imports """
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


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


#from rest_framework import status
#from rest_framework.authtoken.models import Token
#from rest_framework.decorators import api_view, permission_classes
#from rest_framework.permissions import AllowAny
#from rest_framework.response import Response

#from social_django.utils import psa

#from requests.exceptions import HTTPError


#def register_by_access_token(request, backend):
#    token = request.data.get('access_token')
#    user = request.backend.do_auth(token)
#    print(request)
#    if user:
#        token, _ = Token.objects.get_or_create(user=user)
#        return Response(
#            {
#                'token': token.key
#            },
#            status=status.HTTP_200_OK,
#            )
#    else:
#        return Response(
#            {
#                'errors': {
#                    'token': 'Invalid token'
#                    }
#            },
#            status=status.HTTP_400_BAD_REQUEST,
#        )

		