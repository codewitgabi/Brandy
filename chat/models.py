from django.db import models
from django.contrib.auth import get_user_model

# user object
User = get_user_model()

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	receiver = models.ForeignKey(User, related_name="getter", on_delete=models.DO_NOTHING)
	message = models.TextField()
	date_sent = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.message[:30] + "..."

