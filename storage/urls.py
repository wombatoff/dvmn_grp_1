from django.urls import path

from storage import views

app_name = 'storage'

urlpatterns = [
    path('my-rent/', views.my_rent, name='my_rent'),
    path('boxes/', views.storages, name='storages'),
    #path('boxes/<int:box_id>/', views.rent_box, name='rent_box'),
    path('storages/<int:storage_id>/', views.boxes, name='boxes'),
    path('faq/', views.faq, name='faq'),
]
