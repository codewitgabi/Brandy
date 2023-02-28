from django.urls import path
from . import views


app_name = "tailor"
urlpatterns = [
	path("list/",
		views.TailorListView.as_view(),
		name="list_tailors"),
	path("create/",
		views.TailorCreateView.as_view(),
		name="create_tailor"),
	path("detail/<uuid:id>/",
		views.TailorDetailView.as_view(),
		name="tailor_detail"),
	path("update/<uuid:id>/",
		views.TailorUpdateView.as_view(),
		name="update_tailor"),
	path("rating/",
		views.RatingCreateView.as_view(),
		name="create_rating"),
	path("rating/<uuid:id>/",
		views.customer_feedback_page),
	path("rating/update/<int:id>/",
		views.RatingUpdateView.as_view(),
		name="patch_rating"),
	path("rating/update/<uuid:id>/tailor/",
		views.ratingUpdateWithTailor,
		name="tailor_rating_update"),
	path("get-customers/",
		views.GetTailorCustomerList.as_view(),
		name="get_customers"),
	path("dashboard/<uuid:id>/",
		views.TailorDashboardView.as_view(),
		name="tailor-dashboard"),
	path("mybooking/",
		views.TailorBookingList.as_view()),
	path("book/",
		views.TailorBookingEvent.as_view(),
		name="tailor_booking"),
	path("booking/accept/<int:id>/",
		views.accept_booking,
		name="accept_booking"),
	path("booking/decline/<int:id>/",
		views.decline_booking,
		name="decline_booking"),
	path("wallet/notification/", views.withdrawal_notification),
]