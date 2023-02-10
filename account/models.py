from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone

class User(AbstractUser):
	id = models.UUIDField(
		primary_key=True, default=uuid.uuid4)
	username = models.CharField(max_length=30)
	email = models.EmailField(unique=True)
	
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]
	
	def __str__(self):
		return self.email
		

class Otp(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=5)
	valid = models.BooleanField(default= True)
	date_created = models.DateTimeField(auto_now_add=True)
	
	@property
	def has_expired(self):
		delta = timezone.now() - self.date_created
		# token expires in one minute
		return delta.seconds > 99009877
	
	def __str__(self):
		return str(self.token)
		
	class Meta:
		ordering = ("-valid",)
	