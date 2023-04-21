from django.contrib import admin
from django.urls import path
from storage import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('boxes/', views.storages, name='storages'),
    path('boxes/<int:storage_id>/', views.boxes, name='boxes')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)