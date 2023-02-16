from django.urls import path
from . import views


app_name = "shop"
urlpatterns = [
	path("product/upload/", views.ClothUploadView.as_view()),
]