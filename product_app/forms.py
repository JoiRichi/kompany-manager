from django import  forms
from django.forms import ModelForm
from datetime import datetime
from accounts.models import CustomUser, Profile
from .models import Order, Product, ProductSubType

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
        fields = ('costumer', 'total_order_price', 'deposit', 'discount', 'order_description')


'''costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE, blank=True, null=True)
    counter_staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    order_description = models.TextField()
    total_order_price = models.FloatField(default=0)
    date_created = models.DateTimeField(default=datetime.now())
    order_completed = models.BooleanField(default=False)
    paid_fully = models.BooleanField(default=False)
    deposit = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    balance = models.FloatField(default=0)'''


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name',)




class ProductSubTypeForm(forms.ModelForm):
    class Meta:
        model = ProductSubType
        fields = ('sub_type_name', "price")
