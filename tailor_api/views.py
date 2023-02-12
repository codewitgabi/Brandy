""" Django Imports """
from django.shortcuts import render
from django.contrib.auth import get_user_model

""" Custom Imports """
from .models import Tailor, Rating
from .serializers import TailorSerializer

""" Third-party Framework """
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class TailorListView(generics.ListAPIView):
	"""
	List all tailors in the database.
	"""
	serializer_class = TailorSerializer
	queryset = Tailor.objects.all()


class TailorCreateView(generics.CreateAPIView):
	"""
	Creates a tailor instance with the logged in user.
	"""
	serializer_class = TailorSerializer
	queryset = Tailor.objects.all()
	permission_classes = (IsAuthenticated,)
	
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
		
		