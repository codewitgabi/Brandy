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
		views.AddClothToFavorite.as_view()),
	path("product/remove-from-fav/<int:id>/",
		views.RemoveClothFromFavorite.as_view()),
	path("product/favorites/list/",
		views.ListFavorites.as_view()),
	path("product/comment/create/",
		views.ClothCommentCreateView.as_view()),
	path("product/<uuid:id>/comments/",
		views.RetrieveCommentView.as_view()),
	path("transactions/",
		views.GetTransactionNotificationView.as_view()),
]