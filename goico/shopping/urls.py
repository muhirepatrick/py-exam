
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # default homepage
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('products/', views.product_list, name='products'),
    path('services/', views.service_list, name='services'),
    path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('checkout/', views.checkout_order, name='checkout_order'),
    path('my-orders/', views.my_orders, name='my_orders'),

]