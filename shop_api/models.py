from django.db import models
from django.contrib.auth import get_user_model
import uuid
from tailor_api.models import Tailor
from django.core.exceptions import ValidationError

# current user model
User = get_user_model()


class Cloth(models.Model):
	SIZE_CHOICES = [
		("S", "S"),
		("M", "M"),
		("L", "L"),
		("XL", "XL"),
		("XXL", "XXL"),
		("XXXL", "XXXL")
	]
	
	CLOTH_CATEGORIES = [
		("Men", "Men"),
		("Women", "Women"),
		("Babies", "Babies"),
		("Teenagers", "Teenagers")
	]
	
	LENGTH_CHOICES = [
		("Short", "Short"),
		("Half", "Half"),
		("Long", "Long"),
		("Sleeveless", "Sleeveless")
	]
	
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False)
	description = models.CharField(max_length=50)
	category = models.CharField(max_length=9, choices= CLOTH_CATEGORIES, default= "Men")
	sub_category = models.CharField(max_length=30)
	price = models.DecimalField(
		max_digits=8, decimal_places=2, default=0.00)
	discount = models.IntegerField(default=0)
	uploader = models.ForeignKey(
		Tailor, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="cloth/")
	size = models.CharField(
		max_length=4, choices= SIZE_CHOICES, default="L")
	available_colors = models.CharField(max_length=30)
	length = models.CharField(
		max_length=10, choices=LENGTH_CHOICES, default="Short")
	material = models.CharField(max_length=30)
	date_created = models.DateTimeField(auto_now_add=True)
	
	def save(self, *args, **kwargs):
		self.material = self.material.title()
		super().save(*args, **kwargs)
	
	@property
	def new_price(self):
		return self.price - ((self.price * self.discount) / 100)
		
	@property
	def rating(self):
		ratings = self.clothrating_set.all()
		avg = 0
		for r in ratings:
			avg += float(r.rating)
			
		try:
			return avg / ratings.count()
		except ZeroDivisionError:
			return avg
		
	@property
	def likes(self):
		return self.clothlike_set.all().count()
		
	@property
	def comments(self):
		queryset = self.comment_set.all().values()
		data = []
		
		for i in queryset:
			d = {}
			d["user"] = User.objects.get(id=i.get("user_id")).username
			d["comment"] = i.get("comment")
			data.append(d)
		
		return data
		
	def __str__(self):
		return str(self.id)


class TransactionNotification(models.Model):
	tailor = models.ForeignKey(
		Tailor, on_delete=models.CASCADE)
	message = models.TextField()
	cloth = models.ForeignKey(Cloth, on_delete=models.DO_NOTHING)
	
	def __str__(self):
		return self.message
		
	@property
	def pay(self):
		return self.cloth.price
		

class Cart(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	paid = models.BooleanField(default=False)
	
	@property
	def total_cloths(self):
		total = 0
		for item in self.cartitem_set.all():
			total += item.quantity
		return total
		
	@property
	def price_total(self):
		total = 0
		for item in self.cartitem_set.all():
			total = item.cloth.new_price * item.quantity + total
		return total
	
	def __str__(self):
		return str(self.user.username)
		
		
class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
	quantity = models.IntegerField(default= 0)
	
	@property
	def price(self):
		return self.cloth.new_price * self.quantity
	
	def __str__(self):
		return str(self.cloth.id)
		

class ClothRating(models.Model):
	""" Allowed tailor rating """
	RATING =  [
		("0.5", "0.5"),
		("1.0", "1.0"),
		("1.5", "1.5"),
		("2.0", "2.0"),
		("2.5", "2.5"),
		("3.0", "3.0"),
		("3.5", "3.5"),
		("4.0", "4.0"),
		("4.5", "4.5"),
		("5.0", "5.0")
	]
	
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
	rating = models.CharField(max_length= 3, default="0.0", choices= RATING)
	
	def __str__(self):
		return self.rating
		
		
class ClothLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.user.username
		
		
class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	comment = models.TextField()
	cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.comment[:30]
	
	class Meta:
		ordering = ["-date_created"]
		

class FAQ(models.Model):
	question = models.TextField()
	answer = models.TextField()
	
	def __str__(self):
		return self.question[:30]
		
		
class Favorite(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.user.username
	
	@property
	def image(self):
		return self.cloth.image.url


class Card(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	card_number = models.CharField(max_length=16)
	expiry_date = models.CharField(max_length=7)
	cvv = models.CharField(max_length=3)
	
	@property
	def owner(self):
		return self.user.username
	
	def __str__(self):
		return self.user.username

