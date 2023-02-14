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
	path("rating/update/<int:id>/",
		views.RatingUpdateView.as_view(),
		name="patch_rating"),
	path("rating/update/<uuid:id>/tailor/",
		views.ratingUpdateWithTailor,
		name="tailor_rating_update"),
	path("get-customers/",
		views.GetCustomerDetail.as_view(),
		name="get_customers"),
	path("dashboard/",
		views.TailorDashboardView.as_view(),
		name="tailor-dashboard"),
]