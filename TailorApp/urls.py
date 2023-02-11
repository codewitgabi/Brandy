from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
    url(r'^auth/', include('drf_social_oauth2.urls', namespace='drf'))
]
