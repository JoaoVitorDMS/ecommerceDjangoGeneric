from django.contrib import admin
from .models import *

admin.site.register([Client, Category, Product, Cart, CartProduct, Order])
