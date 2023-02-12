from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import uuid

User = get_user_model()


class Tailor(models.Model):
	SKILL = [
		("Tailor", "Tailor"),
		("Fashion Designer", "Fashion Designer"),
		("Tailor and Designer", "Both")
	]
	
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False)
	user = models.OneToOneField(
		User, on_delete=models.CASCADE)
	skill = models.CharField(
		max_length=19,
		choices=SKILL,
		default="Tailor")
	business_name = models.CharField(max_length=100)
	phone = models.CharField(max_length=14)
	experience = models.IntegerField(
		default=1, validators=[MinValueValidator(0)])
	business_address = models.TextField()
	bank = models.CharField(max_length=20)
	account_number = models.CharField(max_length=10)
	
	def __str__(self):
		return self.user.username
		
	@property
	def avg_rating(self):
		ratings = self.rating_set.all()
		avg = 0
		for rating in ratings:
			avg += float(rating)
		
		return avg
		

class Rating(models.Model):
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
	
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	rating = models.CharField(
		max_length=3,
		choices=RATING,
		default="5.0")
	tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.rating
		
		