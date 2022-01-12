from django import  forms
from django.forms import ModelForm
from datetime import datetime
from accounts.models import CustomUser, Profile
from .models import Order, Product, ProductSubType, Costumer, SubOrder

from django.contrib.auth.forms import UserCreationForm



class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields =["email", 'is_counter_staff', 'is_manager', 'password']



class OrderQueryForm(forms.Form):
    start_date = forms.DateTimeField(widget=forms.SelectDateWidget(), label ="from")
    end_date = forms.DateTimeField(widget=forms.SelectDateWidget(), label ="to")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('costumer', )



class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('deposit', 'discount', 'order_description')



class SubOrderForm(forms.ModelForm):
    class Meta:
        model = SubOrder
        fields = ('product_ordered', 'quantity',)





class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name',)




class ProductSubTypeForm(forms.ModelForm):
    class Meta:
        model = ProductSubType
        fields = ('sub_type_name', "price")


class CostumerForm(forms.ModelForm):
    class Meta:
        model = Costumer
        exclude = ('created_by', 'date_created')
