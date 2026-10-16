from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Driver, Customer,CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'image']

class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['image','username', 'email', 'first_name', 'last_name', 'phone_number', 'password']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['image','username', 'email', 'first_name', 'last_name', 'phone_number', 'password']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser  
        fields = ['username', 'password']
