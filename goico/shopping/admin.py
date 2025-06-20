from django.contrib import admin

from .models import Product, Service, CartItem

admin.site.register(Product)
admin.site.register(Service)
admin.site.register(CartItem)