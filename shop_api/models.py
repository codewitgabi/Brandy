from django.db import models
from django.contrib.auth import get_user_model
import uuid

# current user model
User = get_user_model()


class Category(models.Model):
		
	CLOTH_CATEGORIES = [
		("Men", "Men"),
		("Women", "Women"),
		("Babies", "Babies"),
		("Teenagers", "Teenagers")
	]
	
	name = models.CharField(
		max_length=9,
		default="Men",
		choices= CLOTH_CATEGORIES)
		
	class Meta:
		verbose_name_plural = "Categories"
		
	def __str__(self):
		return self.name


class SubCategory(models.Model):
	name = models.CharField(max_length=10)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	
	class Meta:
		verbose_name_plural = "Sub-Categories"
	
	def __str__(self):
		return self.name


class Color(models.Model):
	name = models.CharField(max_length=20)
	
	def __str__(self):
		return self.name
		
		
class Length(models.Model):
	size = models.CharField(max_length=20)
	
	def __str__(self):
		return self.size


class Material(models.Model):
	name = models.CharField(max_length=30)
	
	def __str__(self):
		return self.name 


class Cloth(models.Model):
	SIZE_CHOICES = [
		("S", "S"),
		("M", "M"),
		("L", "L"),
		("XL", "XL"),
		("XXL", "XXL"),
		("XXXL", "XXXL")
	]
	
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False)
	description = models.CharField(max_length=50)
	price = models.DecimalField(
		max_digits=8, decimal_places=2, default=0.00)
	discount = models.IntegerField(default=0)
	image = models.ImageField(upload_to="cloth/")
	uploader = models.ForeignKey(
		User, on_delete=models.CASCADE)
	available_sizes = models.CharField(
		max_length=4, choices= SIZE_CHOICES, default="L")
	available_colors = models.ForeignKey(
		Color, on_delete=models.DO_NOTHING)
	length = models.ManyToManyField(Length, symmetrical=False)
	material_type = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	
	@property
	def new_price(self):
		pass
		
	def __str__(self):
		return


class Cart(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	paid = models.BooleanField(default=False)
	
	def __str__(self):
		return str(self.paid)
		
		
class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
	quantity = models.IntegerField(default= 1)
	
	def __str__(self):
		return self.product
		

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
		
		
class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.user.username
		
		
class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	comment = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.comment[:30]
		

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

