
from django.forms import ModelForm
from .models import Order,Customer
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
      #  fields = ['username','email','password1','password2','profile_picture']
        fields = '__all__'
        exclude =['user']#  dont not update user

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('customer','product','status')

class CreateUserForm(UserCreationForm):
     class Meta:
          model =User
          fields=['username','email','password1','password2']