from django.urls import path
from . import views
from knox import views as knox_views


urlpatterns = [
	path("register/", views.RegisterView.as_view(), name="register"),
	path("login/", views.AppLoginView.as_view(), name="login"),
	path("logout/", knox_views.LogoutView.as_view(), name="logout"),
	path("logout-all/", knox_views.LogoutAllView.as_view(), name="logout_all"),
	
	# reset and change password
	path("change-password/", views.ChangePassword.as_view(), name="change_password"),
]