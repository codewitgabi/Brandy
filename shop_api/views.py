""" Django imports """
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse

""" Custom imports """
from .serializers import (
	ClothUploadSerializer,
	TransactionNotificationSerializer,
	ClothSerializer,
	FavoriteSerializer,
	CommentSerializer,
	RetrieveCommentSerializer,
	ClothRatingSerializer,
	ClothLikeSerializer, CardSerializer, AmountSerializer)
from .models import *
from auth_api.permissions import IsTailor

""" third-party imports """
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


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
		# cloth filters
		query = request.query_params
		category = query.get("q", "")
		sub_category = query.get("category", "")
		color = query.get("color", "")
		size = query.get("size", "")
		length = query.get("length", "")
		price_range = query.get("price", "999999999999")
		price_range = float(price_range)
		material = query.get("material", "")
		
		# sort queries
		default_order = ["?"]
		ordering = query.getlist("order", default_order)
		
		# get cloths by queries
		queryset = self.get_queryset()
		queryset = queryset.filter(
			Q(category__icontains=category) &
			Q(sub_category__icontains=sub_category) &
			Q(available_colors__icontains=color) &
			Q(size__icontains=size) &
			Q(length__icontains=length) &
			Q(price__lte=price_range) &
			Q(material__icontains=material)
		).order_by(*ordering)
		
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
		
		
class AddClothToFavorite(generics.CreateAPIView):
	serializer_class = FavoriteSerializer
	permission_classes = (IsAuthenticated, )
	queryset = Favorite.objects.all()


class RemoveClothFromFavorite(generics.DestroyAPIView):
	serializer_class = FavoriteSerializer
	permission_classes = (IsAuthenticated, )
	queryset = Favorite.objects.all()
	lookup_field = "id"
	
	
class ListFavorites(generics.ListAPIView):
	serializer_class = FavoriteSerializer
	permission_classes = (IsAuthenticated,)
	queryset = Favorite.objects.all()
	
	def list(self, request):
		queryset = self.get_queryset()
		queryset = queryset.filter(user=request.user)
		serializer = FavoriteSerializer(queryset, many=True)
		return Response(serializer.data)


class ClothCommentCreateView(generics.CreateAPIView):
	serializer_class = CommentSerializer
	permission_classes = (IsAuthenticated,)
	queryset = Comment.objects.all()


class RetrieveCommentView(generics.RetrieveAPIView):
	serializer_class = RetrieveCommentSerializer
	permission_classes = (IsAuthenticated,)
	queryset = Cloth.objects.all()
	lookup_field = "id"


class ClothRatingCreateView(generics.CreateAPIView):
	serializer_class = ClothRatingSerializer
	permission_classes = (IsAuthenticated,)
	queryset = ClothRating.objects.all()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_cloth_rating_image(request, cloth_id):
	images = request.data
	try:
		rating = ClothRating.objects.get(user=request.user, cloth_id=cloth_id)
		print(images)
		for img in images:
			ClothRatingImage.objects.create(rating=rating, image=images[img])
		return Response({"status": "success"})
	except:
		return Response({"status": "failed"})


class ClothLikeView(generics.CreateAPIView):
	serializer_class = ClothLikeSerializer
	permission_classes = (IsAuthenticated,)
	queryset = ClothLike.objects.all()


class ClothUnlikeView(generics.DestroyAPIView):
	serializer_class = ClothLikeSerializer
	permission_classes = (IsAuthenticated,)
	queryset = ClothLike.objects.all()
	lookup_field = "id"


class CardCreateEvent(generics.CreateAPIView):
	serializer_class = CardSerializer
	permission_classes = (IsAuthenticated,)
	queryset = Card.objects.all()
	
	def perform_create(self, serializer):
		try:
			serializer.save(user=self.request.user)
		except:
			return Response({"error": "Seems you already have a card"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cartEvent(request, action, cloth_id):
	if request.method == "POST":
		cart, _ = Cart.objects.get_or_create(user=request.user, paid=False)
		
		cart_item, _ = cart.cartitem_set.get_or_create(cloth_id=cloth_id)
		
		if action == "add":
			cart_item.quantity += 1
			cart_item.save()
		
		if action == "sub":
			cart_item.quantity -= 1
			cart_item.save()
			
		if cart_item.quantity <= 0:
			cart_item.delete()
			
		return Response({"status": "success"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCartItems(request):
	if request.method == "GET":
		cart, _ = Cart.objects.get_or_create(user=request.user, paid=False)
		
		cart_items = cart.cartitem_set.all().values()
		data = []
		
		for item in cart_items:
			json = {}
			cloth = Cloth.objects.get(id=item.get("cloth_id"))
			c_item = CartItem.objects.get(id=item.get("id"))
			
			# adjust data to be returned
			json["cloth_img"] = cloth.image.url
			json["quantity"] = item.get("quantity")
			json["total_price"] = c_item.price
			
			# add json data to list
			data.append(json)
		
		return Response({
			"cart_total": cart.total_cloths,
			"price_total": cart.price_total,
			"data": data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_cart_payment(request):
	if request.method == "POST":
		serializer = AmountSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		cart = get_object_or_404(Cart, user=request.user, paid=False)
		data = serializer.data
		
		# checks that a user paid the correct amount
		if str(cart.price_total) == data.get("amount_paid", "0.00"):		
			cart.paid = True
			cart.save()
			return Response({"status": "success"}, status=status.HTTP_200_OK)
		else:
			return Response({"status": "The amount of the cart uas been tampered with"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cloth_feedback_page(request, cloth_id):
	cloth = get_object_or_404(Cloth, id=cloth_id)
	
	rating_grouping = []
	rating_grouping.append({"5": cloth.clothrating_set.filter(rating=5).count()})
	rating_grouping.append({"4": cloth.clothrating_set.filter(rating=4).count()})
	rating_grouping.append({"3": cloth.clothrating_set.filter(rating=3).count()})
	rating_grouping.append({"2": cloth.clothrating_set.filter(rating=2).count()})
	rating_grouping.append({"1": cloth.clothrating_set.filter(rating=1).count()})
	
	# Get all related ratings/feedbacks
	feedbacks =  list(cloth.clothrating_set.all().order_by("-date_created").values())
	for d in feedbacks:
		d["user_name"] = User.objects.get(id=d["user_id"]).username
		d["rating"] = float(d["rating"])
		d["images"] = ClothRating.objects.get(user_id=d["user_id"], cloth_id=d["cloth_id"]).images
	
	return Response({
		"avg_rating": cloth.rating,
		"rating_grouping": rating_grouping,
		"feedbacks": feedbacks})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_orders(request):
	"""
	Returns all order for the current logged in tailor.
	query_params:
		sent: takes true or false as value.
		/?sent=true returns all orders that have been sent.
		/?sent=false returns all unsent order. This query param can be ignored as it is the default
	"""
	try:
		tailor = request.user.tailor
		sent = request.query_params.get("sent", "false")
		sent = sent.lower() == "true"
		data = []
		
		orders = list(Order.objects.filter(tailor=tailor, delivered=sent).values())
		
		for order in orders:
			d = {}
			cloth = CartItem.objects.get(id=order["cart_item_id"]).cloth
			cart_owner = CartItem.objects.get(id=order["cart_item_id"]).cart.user
			
			d["name"] = cloth.sub_category
			d["material"] = cloth.material
			d["color"] = cloth.available_colors
			d["length"] = cloth.length
			d["size"] = cloth.size
			d["address"] = cart_owner.address
			d["phone"] = cart_owner.phone
			d["image"] = cloth.image.url
			
			data.append(d)
		print(data)
		return Response({"status": "success", "orders": data})
		
	except User.tailor.RelatedObjectDoesNotExist:
		return Response({"error": "User is not a valid tailor instance"})