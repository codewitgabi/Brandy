from django.urls import path
from . import views


urlpatterns = [
	path("create/", views.CreateMessage.as_view()),
	path("get-messages/<uuid:id>/", views.get_messages),
]