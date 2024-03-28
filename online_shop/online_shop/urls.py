
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import index, registration_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/register/" ,registration_view, name='register'),
    path('accounts/', include("django.contrib.auth.urls")),
    path("", index, name="index"),
    path('shop/', include("shop.urls"))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
