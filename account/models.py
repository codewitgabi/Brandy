from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone


class User(AbstractUser):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False)
	username = models.CharField(max_length=30)
	email = models.EmailField(unique=True)
	address = models.TextField(null=True, blank=True, default="")
	phone = models.CharField(max_length=14)
	followers = models.ManyToManyField(
		"self",
		blank=True,
		symmetrical=False)
	following = models.ManyToManyField(
		"self",
		blank=True,
		symmetrical=False,
		related_name="disciples")
	image = models.ImageField(upload_to= "profiile-picture/", default= "avatar.jpg")
	
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]
	
	def __str__(self):
		return self.email
		
	def save(self, *args, **kwargs):
		"""
		Add user instance to followers list
		"""
		for user in self.following.all():
			user.followers.add(self)
			
		"""
		Add user instance to related instance following list
		"""
		for user in self.followers.all():
			user.following.add(self)
			
		super().save(*args, **kwargs)
		

class Otp(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=5)
	valid = models.BooleanField(default= True)
	date_created = models.DateTimeField(auto_now_add=True)
	
	@property
	def has_expired(self):
		delta = timezone.now() - self.date_created
		# token expires in two minutes
		return delta.seconds > 120
	
	def __str__(self):
		return str(self.token)
		
	class Meta:
		ordering = ("-valid",)
	
	