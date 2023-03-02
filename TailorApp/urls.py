from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# documentation generator
schema_view = get_schema_view(
	openapi.Info(
		title="Snippets API",
		default_version='v1',
		description="Test description",
		terms_of_service="https://www.google.com/policies/terms/",
		contact=openapi.Contact(email="codewitgabi222@gmail.com"),
		license=openapi.License(name="BSD License"),
		),
	public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/api/", include("auth_api.urls")),
    path("shop/api/", include("shop_api.urls")),
    path("tailor/api/", include("tailor_api.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path("chat/api/", include("chat.urls")),
    path("api/doc/", include([
    	path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    	path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    	])
    ),
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
else:
	# to be used for production for the time being
	urlpatterns += re_path(r"^media/(?P<path>.*)$", serve, {
		"document_root": settings.MEDIA_ROOT})