from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from storage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('storage/', include('storage.urls', namespace='storage')),
    path('', views.index, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
