from django.contrib import admin
from django.urls import include, path

from storage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('storage/', include('storage.urls', namespace='storage')),
    path('', views.index, name='home'),

]
