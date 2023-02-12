from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = "auth_api"
urlpatterns = [
	path("users/list/", views.UserListView.as_view(), name="list_users"),
	path("users/detail/<uuid:id>/", views.UserDetailView.as_view(), name="retrieve_user"),
	path("register/", views.RegisterView.as_view(), name="register"),
	path("register/verify-otp/<int:otp>/",
		views.verify_OTP, name="register_verify_otp"),
	path("register/resend-otp/", views.ResendOtpView.as_view(), name="resend_otp"),
	path("login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path("login/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
	path("logout/", views.LogoutView.as_view(), name="logout"),
	# reset and change password
	path("change-password/", views.ChangePassword.as_view(), name="change_password"),
	path("password-reset/",
		include("django_rest_passwordreset.urls", 
			namespace="password_reset")),
]