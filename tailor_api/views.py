""" Django Imports """
from django.shortcuts import render
from django.contrib.auth import get_user_model

""" Custom Imports """
from .models import Tailor, Rating
from .serializers import (
	TailorSerializer,
	RatingSerializer,
	TailorRatingSerializer,
	CustomerListingSerializer,
	TailorDashboardSerializer)
from auth_api.permissions import IsTailorAccountOwner, IsAccountOwner

""" Third-party Imports """
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

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


class TailorDetailView(generics.RetrieveAPIView):
	serializer_class = TailorSerializer
	queryset = Tailor.objects.all()
	permission_classes = (IsAuthenticated, IsTailorAccountOwner)
	lookup_field = "id"
	
	
class TailorUpdateView(generics.UpdateAPIView):
	serializer_class = TailorSerializer
	queryset = Tailor.objects.all()
	permission_classes = (IsAuthenticated, IsTailorAccountOwner)
	lookup_field = "id"
	
	def perform_update(self, serializer):
		serializer.save(user=self.request.user)
		

@permission_classes([IsAuthenticated])
@api_view(["PUT"])
def ratingUpdateWithTailor(request, id):
	"""
	For rating update where a tailors id is readily available, use this.
	"""
	try:
		tailor = Tailor.objects.get(id=id)
		user = request.user
		R = Rating.objects.get(user=user, tailor=tailor)
	except Tailor.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	if request.method == "PUT":
		serializer = TailorRatingSerializer(data=request.data)
		if serializer.is_valid():
			new_rating = serializer.validated_data.get("rating")
			R.rating = new_rating
			R.save()
			return Response({
				"status": "success",
			}, status=status.HTTP_206_PARTIAL_CONTENT)
		else:
			return Response(serializer.errors)
			
	
class RatingCreateView(generics.CreateAPIView):
	"""
	Creates a rating for a tailor
	"""
	serializer_class = RatingSerializer
	queryset = Rating.objects.all()
	permission_classes = (IsAuthenticated,)
	
	def perform_create(self, serializer):
		user = self.request.user
		tailor = serializer.validated_data.get("tailor")
		try:
			Rating.objects.get(tailor=tailor, user=user)
		except Rating.DoesNotExist:
			serializer.save(user=user)
			

class RatingUpdateView(generics.UpdateAPIView):
	"""
	Updates a rating for a tailor via a PATCH request
	For rating update where a rating id is readily available, use this.
	"""
	serializer_class = RatingSerializer
	queryset = Rating.objects.all()
	permission_classes = (IsAuthenticated,)
	lookup_field = "id"

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)


class GetCustomerDetail(APIView):
	permission_classes = (IsAuthenticated, IsAccountOwner)
	def get(self, request):
		user = request.user.tailor
		tasks = user.task_set.all()
		data = []
		serializer = CustomerListingSerializer(tasks, many=True)
		
		for d in serializer.data:
			if not d in data:
				data.append(d)
				
		return Response(data)
		
		
class TailorDashboardView(APIView):
	"""
	Returns data to be used for a tailors dashboard
	"""
	def get(self, request):
		user = request.user.tailor
		serializer = TailorDashboardSerializer(user)
		return Response(serializer.data)
		
		