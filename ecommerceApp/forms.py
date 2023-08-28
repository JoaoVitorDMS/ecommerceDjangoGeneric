from django import forms
from .models import Order, Client
from django.forms import ModelForm, PasswordInput, TextInput, EmailInput
from django.contrib.auth.models import User



class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = [
      "order_by",
      "address_shipping",
      "phone",
      "email",  
    ]
    widgets = {
      'order_by': TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: 300px',
        'placeholder': 'order_by'
      }),
      'address_shipping': TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: 300px',
        'placeholder': 'Shipping address'
      }),
      'phone': TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: 300px',
        'placeholder': 'Your phone number'
      }),
      'email': EmailInput(attrs={
        'class': "form-control",
        'style': 'max-width: 300px',
        'placeholder': 'Your e-mail address'
      })
    }

class RegisterForm(forms.ModelForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'User', 'class': "form-control", 'style': 'max-width: 300px; display: flex;'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter A Password', 'class': "form-control", 'style': 'max-width: 300px; display: flex;'}))
  email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Your E-mail Address', 'class': "form-control", 'style': 'max-width: 300px; display: flex;'}))
  class Meta:
    model = Client
    fields = ["username","full_name","email","address","password",]
    widgets = {
      'full_name': TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: 300px',
        'placeholder': 'Full name'
      }),

      'address': TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: 300px',
        'placeholder': 'Your address'
      }),

    }

  def clean_username(self):
      uname = self.cleaned_data.get("username")
      if User.objects.filter(username=uname).exists():
        raise forms.ValidationError("This user already exists")
      return uname

class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'User', 'class': "form-control", 'style': 'max-width: 300px; display: flex;'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter A Password', 'class': "form-control", 'style': 'max-width: 300px; display: flex;'}))
