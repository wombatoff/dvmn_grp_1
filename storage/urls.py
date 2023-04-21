from django.urls import path

from storage import views

app_name = 'storage'

urlpatterns = [
    path('my-rent/', views.my_rent, name='my_rent'),
    path('boxes/', views.boxes, name='boxes'),
    path('faq/', views.faq, name='faq'),
]
