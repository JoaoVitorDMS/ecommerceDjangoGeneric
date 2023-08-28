from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    alt = models.CharField(max_length=600, null=True)
    price_market = models.PositiveBigIntegerField()
    price_sale = models.PositiveBigIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    refund = models.CharField(max_length=300, null=True, blank=True)
    views = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveBigIntegerField(default=0)
    date_sale = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id) # type: ignore

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.PositiveBigIntegerField()
    amount = models.PositiveBigIntegerField()
    subtotal = models.PositiveBigIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + "CartProduct: " + str(self.id) # type: ignore

ORDER_STATUS=(
    ("Order received successfully", "Order received successfully"),
    ("Please wait, the order is being processed", "Please wait, the order is being processed"),
    ("Order is on its way", "Order is on its way"),
    ("Wonderful, the order is complete", "Wonderful, the order is complete"),
    ("Unfortunately, the order was canceled", "Unfortunately, the order was canceled"),
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)

    order_by = models.CharField(max_length=200)

    address_shipping = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveBigIntegerField()
    discount = models.PositiveBigIntegerField()
    total = models.PositiveBigIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: " + str(self.id) # type: ignore
