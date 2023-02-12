from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@receiver(reset_password_token_created)
def password_reset_token_created(
	sender, instance, reset_password_token, *args, **kwargs):
		
	token = reset_password_token.key
	
	subject = "Password Reset"
	html_content = render_to_string("password_reset.html", {"token": token})
	
	mail = EmailMessage(
		subject,
		html_content,
		to=[reset_password_token.user.email]
	)
	
	mail.content_subtype = "html"
	mail.fail_silently = False
	mail.send()
	
	