from django.urls import path
from . import views


app_name = "tailor"
urlpatterns = [
	path("list/",
		views.TailorListView.as_view(),
		name="list_tailors"),
	path("create/",
		views.TailorCreateView.as_view(),
		name="create_tailors"),
]