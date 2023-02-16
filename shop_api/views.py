from django.shortcuts import render
from .serializers import ClothUploadSerializer
from .models import *
from auth_api.permissions import IsTailor
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
		

class ClothListView(generics.ListAPIView):
	serializer_class = ClothUploadSerializer
	permission_classes = (IsAuthenticated, IsTailor)
	queryset = Cloth.objects.all()
	
	def list(self, request):
		queryset = self.get_queryset()
		queryset = queryset.filter(uploader=request.user.tailor)
		serializer = ClothUploadSerializer(queryset, many=True)
		return Response(serializer.data)


class ClothUpdateView(generics.RetrieveUpdateAPIView):
	serializer_class = ClothUploadSerializer
	permission_classes = (IsAuthenticated, IsTailor)
	queryset = Cloth.objects.all()
	lookup_field = "id"
	
	def perform_update(self, serializer):
		image = self.request.data.get("image")
		serializer.save(image=image, uploader=self.request.user.tailor)
	