from django.urls import path
from .views import *

app_name = "ecommerceApp"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("sobre", AboutView.as_view(), name="about"),
    path("contato", ContactView.as_view(), name="contact"),
    path("todos-produtos", AllProductsView.as_view(), name="all-products"),
    path("product/<slug:slug>", ProductDetailView.as_view(), name="productDetail"),
    path("addCart-<int:product_id>", AddCartView.as_view(), name="addCart" ),
    path("my-cart", MyCartView.as_view(), name="myCart"),
    path("menuCart/<int:cartProduct_id>", MenuCartView.as_view(), name="menuCart"),
    path("cleanCart", CleanCartView.as_view(), name="cleanCart"),
    path("checkout", CheckoutView.as_view(), name="checkout"),
    path("register", RegisterView.as_view(), name="register"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("login", LoginView.as_view(), name="login"),
    
]
