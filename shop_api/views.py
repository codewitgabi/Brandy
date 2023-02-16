from django.shortcuts import render
from .serializers import ClothUploadSerializer
from .models import *
from auth_api.permissions import IsTailorAccountOwner, IsAccountOwner
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class ClothUploadView(generics.CreateAPIView):
	serializer_class = ClothUploadSerializer
	permission_classes = (IsAuthenticated,)
	queryset = Cloth.objects.all()
	
	def perform_create(self, serializer):
		image = self.request.data.get("image")
		serializer.save(image=image, uploader=self.request.user.tailor)


