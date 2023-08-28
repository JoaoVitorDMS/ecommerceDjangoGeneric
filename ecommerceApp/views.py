from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView, CreateView, FormView
from django.urls import reverse_lazy
from .forms import OrderForm, RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import *

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all().order_by("-id")
        return context

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html"

class AllProductsView(TemplateView):
    template_name = "allproducts.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allCategory'] = Category.objects.all()
        return context

class ProductDetailView(TemplateView):
    template_name = "productDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.views += 1
        product.save()
        context['products'] = product
        return context

class AddCartView(TemplateView):
    template_name = "addCart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['product_id']
        product_obj = Product.objects.get(id=product_id)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

            if product_in_cart.exists():
                cartProduct = product_in_cart.last()
                cartProduct.amount += 1
                cartProduct.subtotal += product_obj.price_sale
                cartProduct.save()
                cart_obj.total += product_obj.price_sale
                cart_obj.save()

            else:
                cartProduct = CartProduct.objects.create(
                cart = cart_obj,
                product = product_obj,
                review = product_obj.price_sale,
                amount = 1,
                subtotal = product_obj.price_sale,
                )
                cart_obj.total += product_obj.price_sale
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartProduct = CartProduct.objects.create(cart = cart_obj,
                product = product_obj,
                review = product_obj.price_sale,
                amount = 1,
                subtotal = product_obj.price_sale,
                )
            cart_obj.total += product_obj.price_sale
            cart_obj.save()
            
        return context
    
class MyCartView(TemplateView):
    template_name = "myCart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

class MenuCartView(View):
     def get(self,request,*args,**kwargs):
       cartProduct_id = self.kwargs["cartProduct_id"]
       action = request.GET.get("action")
       cartProduct_obj = CartProduct.objects.get(id=cartProduct_id)
       cart_obj = cartProduct_obj.cart
       
       if action == "increment":
           cartProduct_obj.amount += 1
           cartProduct_obj.subtotal += cartProduct_obj.review
           cartProduct_obj.save()
           cart_obj.total += cartProduct_obj.review
           cart_obj.save()
           
       elif action == "decrement":
           cartProduct_obj.amount -= 1
           cartProduct_obj.subtotal -= cartProduct_obj.review
           cartProduct_obj.save()
           cart_obj.total -= cartProduct_obj.review
           cart_obj.save()
           if cartProduct_obj.amount == 0:
               cartProduct_obj.delete()

       elif action == "delete":
           cart_obj.total -= cartProduct_obj.subtotal
           cart_obj.save()
           cartProduct_obj.delete()
       else:
           pass
       return redirect("ecommerceApp:myCart")
     
class CleanCartView(View):
    def get(self,request,*args,**kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecommerceApp:myCart")

class CheckoutView(CreateView):
    template_name = "checkout.html"
    form_class = OrderForm
    success_url = reverse_lazy("ecommerceApp:index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order received successfully"
            del self.request.session['cart_id']
        else:
            return redirect("ecommerceApp:index")
        
        return super().form_valid(form)


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("ecommerceApp:index")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("ecommerceApp:index")
    
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password2 = form.cleaned_data.get("password")
        userPassword = authenticate(username=username, password=password2)
        if userPassword is not None and userPassword.client:
            login(self.request, userPassword)
        else:
            return render(self.request, self.template_name, {"form":self.form_class, "error":"Credentials not found"})
        return super().form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecommerceApp:login")
        