from django.urls import path

from storage import views

app_name = 'storage'

urlpatterns = [
    path('my-rent/', views.my_rent, name='my_rent'),
    path('', views.storages, name='storages'),
    path('boxes/<int:box_id>/', views.my_rent, name='rent_box'),
    path('<int:storage_id>/', views.boxes, name='boxes'),
    path('faq/', views.faq, name='faq'),
]
