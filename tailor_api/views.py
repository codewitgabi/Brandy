""" Django Imports """
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.utils import OperationalError

""" Custom Imports """
from .models import (
	Tailor,
	Rating,
	TaskReminder,
	Task,
	Booking,
	WalletNotification)
from .serializers import (
	TailorSerializer,
	RatingSerializer,
	TailorRatingSerializer,
	CustomerListingSerializer,
	TailorDashboardSerializer,
	BookingSerializer,
	AcceptBookingSerializer,
	DeclineBookingSerializer,
	TailorBookingSerializer,
	WalletNotificationSerializer,
	TaskSerializer)
from auth_api.permissions import IsTailorAccountOwner, IsAccountOwner
from threading import Thread
from datetime import datetime, date
import time
from shop_api.models import CartItem

""" Third-party Imports """
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

User = get_user_model()


def create_reminders():
	while True:
		time.sleep(1)
		try:
			tasks = Task.objects.filter(delivered=False)
			for task in tasks:
				year, month, day = task.due_date.year, task.due_date.month, task.due_date.day
				cur = datetime.now()
				to_datetime = datetime(year, month, day)
				
				dt = to_datetime - cur
				mins, _ = divmod(dt.total_seconds(), 60)
				mins = int(mins)
	
				# create 1 day reminder
				if mins == 1_440:
					try:
						TaskReminder.objects.get(
							task=task,
							message="You have 24 hours to complete this task",)
					except TaskReminder.DoesNotExist:
						TaskReminder.objects.create(
							tailor=task.tailor,
							task=task,
							message="You have 24 hours to complete this task")
				
				# create 12 hrs reminder
				if mins == 720:
					try:
						TaskReminder.objects.get(
							task=task,
							message="You have 12 hours to complete this task")
					except TaskReminder.DoesNotExist:
						TaskReminder.objects.create(
							tailor=task.tailor,
							task=task,
							message="You have 12 hours to complete this task")
				
				# creates 6 hrs reminder
				if mins == 360:
					try:
						TaskReminder.objects.get(
							task=task,
							message="You have 6 hours to complete this task")
					except TaskReminder.DoesNotExist:
						TaskReminder.objects.create(
							tailor=task.tailor,
							task=task,
							message="You have 6 hours to complete this task")
		except OperationalError:
			pass


class TailorListView(generics.ListAPIView):
	"""
	List all tailors in the database.
	"""
	serializer_class = TailorSerializer
	queryset = Tailor.objects.all()
	
	def list(self, request):
		# Get user queries
		query = request.query_params
		q = query.get("q", "")
		exp = query.get("exp", "0")
		exp = int(exp)
		loc = query.get("loc", "")
		
		# sort queries
		default_order = ["?"]
		ordering = query.getlist("order", default_order)
		
		# get tailors by queries
		queryset = self.get_queryset()
		queryset = queryset.filter(
			Q(experience__gte=exp) &
			Q(skill__icontains=q) & 
			Q(location__icontains=loc)
		).order_by(*ordering)
		
		serializer = TailorSerializer(queryset, many=True)
		
		return Response(serializer.data)


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
		

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_rating_image(request, tailor_id):
	images = request.data
	try:
		rating = Rating.objects.get(user=request.user, tailor_id=tailor_id)
		print(images)
		for img in images:
			RatingImage.objects.create(rating=rating, image=images[img])
		return Response({"status": "success"})
	except:
		return Response({"status": "failed"})

	
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


class GetTailorCustomerList(APIView):
	"""
	Get Tailors customers list
	"""
	permission_classes = (IsAuthenticated,)
	
	def get(self, request):
		try:
			user = request.user.tailor
			tasks = user.task_set.all()
			data = []
			serializer = CustomerListingSerializer(tasks, many=True)
			
			for d in serializer.data:
				if not d in data:
					data.append(d)
					
			return Response(data)
			
		except User.tailor.RelatedObjectDoesNotExist:
			return Response({"error": "User is not a valid tailor instance"}, status=status.HTTP_403_FORBIDDEN)
		
		
class TailorDashboardView(generics.RetrieveAPIView):
	"""
	Returns data to be used for a tailors dashboard
	"""
	serializer_class = TailorDashboardSerializer
	queryset = Tailor.objects.all()
	permission_classes = (IsAuthenticated,)
	lookup_field = "id"
		

class TailorBookingEvent(generics.CreateAPIView):
	"""
	Books a tailor to discuss plan for a task.
	"""
	serializer_class = BookingSerializer
	queryset = Booking.objects.all()
	permission_classes = (IsAuthenticated,)


class TailorBookingList(generics.ListAPIView):
	serializer_class = BookingSerializer
	queryset = Booking.objects.all()
	permission_classes = (IsAuthenticated,)
	
	def list(self, request):
		# get queryset
		queryset = self.get_queryset()
		
		# get queries
		query = request.query_params
		month = query.get("month", date.today().month)
		month = int(month)
		day = query.get("day", 1)
		day = int(day)
		
		queryset = queryset.filter(
			Q(due_date__month=month) &
			Q(due_date__day__gte=day),
			tailor=request.user.tailor,)
		
		serializer = BookingSerializer(queryset, many=True)
		return Response(serializer.data)
	

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_booking(request, id):
	try:
		booking = Booking.objects.get(id=id)
	except Booking.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	if booking.tailor.user != request.user:
		return Response({"error": "You do not have permission to modify this content"})
	
	if request.method == "POST":
		booking.accepted = True
		booking.declined = False
		booking.save()
		
		return Response({"status": "success"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def decline_booking(request, id):
	try:
		booking = Booking.objects.get(id=id)
	except Booking.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	if booking.tailor.user != request.user:
		return Response({"error": "You do not have permission to modify this content"})
	
	if request.method == "POST":
		booking.accepted = False
		booking.declined = True
		booking.save()
		
		return Response({"status": "success"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def withdrawal_notification(request):
	"""
	Gets the tailor's transaction details.
	:params:
		`wallet`:
			The type of wallet to be returned. Allowed values are credit, withdrawal, pending.
		`year`:
			This filters the notification by the given year passed to the query parameters.
		`month`:
			Filters it down to a specific month.
	If none of these parameters are provided, all the notifications are returned.
	"""
	query = request.query_params # get query parameters
	wallet = query.get("wallet", "")
	year = query.get("year", date.today().year)
	year = int(year)
	month = query.get("month", date.today().month)
	month = int(month)
	
	if request.method == "GET":
		try:
			tailor = request.user.tailor
			notifications = WalletNotification.objects.filter(
				Q(wallet__icontains=wallet),
				Q(date_created__year=year),
				Q(date_created__month=month),
				tailor=tailor).values()
			account = {
				"pending": tailor.pending_money,
				"withdrawn": tailor.money_earned,
				"balance": tailor.wallet_balance
			}
			return Response({
				"account": account,
				"notifications": notifications,
			})
			
		except User.tailor.RelatedObjectDoesNotExist:
			return Response({"error": "Not a valid tailor instance"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_view(request):
	"""
	Get all tasks related to the current logged in user which should be a tailor instance.
	:Params:
		completed:
			To query tasks that have been completed, pass the parameter `completed` and set the value to true.
		delivered:
			To query tasks that have been delivered, pass the parameter `delivered` and set the value to true.
	You don't necessarily need to pass the two parameters. Only pass the one you need.
	"""
	try:
		tailor = request.user.tailor
		
		query = request.query_params # get query parameters
		completed = query.get("completed", "false")
		completed = completed.lower() == "true"
		delivered = query.get("delivered", "false")
		delivered = delivered.lower() == "true"
		
		tasks = list(Task.objects.filter(
			tailor=tailor,
			completed=completed,
			delivered=delivered).values())
		
		# add more data to response
		for task in tasks:
			t = Task.objects.get(id=task["id"])
			task["deadline"] = t.deadline
			task["customer_name"] = t.username
			task["customer_phone"] = t.phone
			task["customer_address"] = t.address
			task["customer_measurement"] = t.measurement
		
		return Response({
			"tasks": tasks,
		})
		
	except User.tailor.RelatedObjectDoesNotExist:
		return Response({"error": "Not a valid tailor instance"})


class TaskCreateView(generics.CreateAPIView):
	"""
	Task Creation handler.
	"""
	serializer_class = TaskSerializer
	queryset = Task.objects.all()
	permission_classes = (IsAuthenticated,)
	
	def perform_create(self, serializer):
		serializer.save(tailor=self.request.user.tailor)

