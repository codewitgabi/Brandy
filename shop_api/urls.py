from django.urls import path
from . import views


app_name = "shop"
urlpatterns = [
	path("product/upload/", views.ClothUploadView.as_view()),
	path("product/store/", views.TailorStoreListView.as_view()),
	path("product/list/",
		views.ClothListView.as_view()),
	path("product/update/<uuid:id>/",
		views.ClothUpdateView.as_view()),
	path("product/add-to-fav/",
		views.AddToFavorite.as_view()),
	path("transactions/",
		views.GetTransactionNotificationView.as_view()),
]