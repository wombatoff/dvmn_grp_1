from django.urls import path

from storage import views

app_name = 'storage'

urlpatterns = [
    path('my-rent/', views.my_orders, name='my_orders'),
    path('', views.storage, name='current_storage'),
    path('box/<int:box_id>/', views.rent_box, name='rent_box'),
    path('<int:storage_id>/', views.storage, name='storage_detail'),
    path('order_success/', views.order_success, name='order_success'),
    path('faq/', views.faq, name='faq'),
]
