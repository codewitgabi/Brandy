from django.urls import path
from . import views


app_name = "shop"
urlpatterns = [
	path("orders/", views.get_orders),
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
	path("product/rating/",
		views.ClothRatingCreateView.as_view()),
	path("product/rating-image/<uuid:cloth_id>/", views.create_cloth_rating_image),
	path("product/like/",
		views.ClothLikeView.as_view()),
	path("product/unlike/<int:id>/",
		views.ClothUnlikeView.as_view()),
	path("transactions/",
		views.GetTransactionNotificationView.as_view()),
	path("card/create/",
		views.CardCreateEvent.as_view()),
	path("cart/<str:action>/<uuid:cloth_id>/", views.cartEvent),
	path("cart/display/", views.getCartItems),
	path("cart/complete/", views.complete_cart_payment),
	path("product/<uuid:cloth_id>/feedbacks/", views.cloth_feedback_page),
]