from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/api/", include("auth_api.urls")),
    path("shop/api/", include("shop_api.urls")),
    path("tailor/api/", include("tailor_api.urls")),
    path('api-auth/', include('rest_framework.urls')),
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
