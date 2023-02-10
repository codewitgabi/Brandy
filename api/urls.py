from django.urls import path, re_path
from . import views
from knox import views as knox_views

app_name = "api"
urlpatterns = [
	path("register/", views.RegisterView.as_view(), name="register"),
	path("register/verify-otp/<int:otp>/",
		views.verify_OTP, name="register_verify_otp"),
	path("register/resend-otp/", views.ResendOtpView.as_view(), name="resend_otp"),
	path("login/", views.AppLoginView.as_view(), name="login"),
	path("logout/", knox_views.LogoutView.as_view(), name="logout"),
	path("logout-all/", knox_views.LogoutAllView.as_view(), name="logout_all"),
	
	# reset and change password
	path("change-password/", views.ChangePassword.as_view(), name="change_password"),
]