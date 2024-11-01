from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static
from core import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('libros.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
