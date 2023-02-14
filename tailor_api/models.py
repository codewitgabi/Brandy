from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
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
	wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	money_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	pending_money = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
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
			avg += float(rating.rating)
			
		try:
			return avg / ratings.count()
		except ZeroDivisionError:
			return avg
		
		
	@property
	def total_ratings(self):
		return self.rating_set.all().count()
		
	@property
	def profile_picture(self):
		return self.user.image.url
		
	@property
	def followers_count(self):
		return str(self.user.followers.all().count())
		
	@property
	def following_count(self):
		return str(self.user.following.all().count())
		
	@property
	def task_list(self):
		data = []
		tasks = self.task_set.all()
		for task in tasks:
			data.append(task.customer.image.url)
		return data
		
	@property
	def reminders(self):
		data = []
		r = self.taskreminder_set.all()
		for i in r:
			data.append(i.message)
		return data
		

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


class Task(models.Model):
	tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE)
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	time_created = models.TimeField(auto_now_add=True)
	due_date = models.DateField()
	charge = models.DecimalField(max_digits=12, decimal_places=2)
	delivered = models.BooleanField(default=False)
	
	def __str__(self):
		return self.customer.username
		
	@property
	def phone(self):
		return self.customer.phone
		
	@property
	def address(self):
		return self.customer.address
		
	@property
	def image(self):
		return self.customer.image.url
		
	@property
	def username(self):
		return self.customer.username
		
	@property
	def measurement(self):
		m = self.customer.measurement
		return {
			"crotch_length": m.crotch_length,
			"center_length": m.center_length,
			"out_seam": m.out_seam,
			"waist": m.waist,
			"In_seam": m.In_seam,
			"hip": m.hip,
			"ankle": m.ankle,
			"bust": m.bust,
			"height": m.height,
			"hight_bust": m.hight_bust
		}
		
		
class TaskReminder(models.Model):
	message = models.TextField()
	tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.message
		
		
class Measurement(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	crotch_length = models.IntegerField(default=1)
	center_length = models.IntegerField(default=1)
	out_seam = models.IntegerField(default=1)
	waist = models.IntegerField(default=1)
	In_seam = models.IntegerField(default=1)
	hip = models.IntegerField(default=1)
	ankle = models.IntegerField(default=1)
	bust = models.IntegerField(default=1)
	height = models.IntegerField(default=1)
	hight_bust = models.IntegerField(default=1)
	
	def __str__(self):
		return self.user.username
		
	def clean(self):
		if Tailor.objects.filter(user= self.user).exists():
			raise ValidationError("Tailor instances cannot have measurements!")
		super(Measurement, self).clean()
		

# availability