""" Django imports """
from django.shortcuts import render
from django.db.models import Q

""" Custom imports """
from .serializers import (
	ClothUploadSerializer,
	TransactionNotificationSerializer,
	ClothSerializer)
from .models import *
from auth_api.permissions import IsTailor

""" third-party imports """
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ClothUploadView(generics.CreateAPIView):
	serializer_class = ClothUploadSerializer
	permission_classes = (IsAuthenticated, IsTailor)
	queryset = Cloth.objects.all()
	
	def perform_create(self, serializer):
		image = self.request.data.get("image")
		serializer.save(image=image, uploader=self.request.user.tailor)
		

class TailorStoreListView(generics.ListAPIView):
	"""
	Displays all cloth uploaded by a particular tailor.
	"""
	serializer_class = ClothUploadSerializer
	permission_classes = (IsAuthenticated, IsTailor)
	queryset = Cloth.objects.all()
	
	def list(self, request):
		queryset = self.get_queryset()
		queryset = queryset.filter(uploader=request.user.tailor)
		serializer = ClothUploadSerializer(queryset, many=True)
		return Response(serializer.data)


class ClothUpdateView(generics.RetrieveUpdateAPIView):
	"""
	Updates a cloth uploaded by a tailor. For better result, use a PUT request.
	"""
	serializer_class = ClothUploadSerializer
	permission_classes = (IsAuthenticated, IsTailor)
	queryset = Cloth.objects.all()
	lookup_field = "id"
	
	def patch(self, request, *args, **kwargs):
		id = self.kwargs.get("id")
		prev_img = Cloth.objects.get(id=id).image
		image = request.data.get("image") if request.data.get("image") is not None else prev_img
		print(request.data)
		serializer = ClothUploadSerializer(
			instance= Cloth.objects.get(id=id),
			partial=True,
			data=request.data,
		)
		if serializer.is_valid():
			serializer.save(image=image)
			return Response({"status": "success", "data": serializer.data})
		return Response(serializer.errors)
	
	def perform_update(self, serializer):
		image = self.request.data.get("image")
		serializer.save(image=image, uploader=self.request.user.tailor)
		
	
class ClothListView(generics.ListAPIView):
	"""
	Returns all cloth in the database based on category query param passed to the url
	requires:
		?category=<category> on url
	"""
	serializer_class = ClothSerializer
	permission_classes = (IsAuthenticated,)
	queryset = Cloth.objects.all()
	
	def list(self, request):
		category = request.query_params.get("q", "")
		sub_category = request.query_params.get("category", "")
		queryset = self.get_queryset()
		queryset = queryset.filter(
			Q(category__icontains=category) &
			Q(sub_category__icontains=sub_category)
		).order_by("?")
		serializer = ClothSerializer(queryset, many=True)
		return Response(serializer.data)
		

class GetTransactionNotificationView(generics.ListAPIView):
	serializer_class = TransactionNotificationSerializer
	permission_classes = (IsAuthenticated, IsTailor)
	queryset = TransactionNotification.objects.all()
	
	def list(self, request):
		queryset = self.get_queryset()
		queryset = queryset.filter(tailor=request.user.tailor)
		serializer = TransactionNotificationSerializer(queryset, many=True)
		return Response(serializer.data)