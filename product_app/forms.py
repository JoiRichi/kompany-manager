from django import forms
from django.forms import ModelForm, Select

from accounts.models import CustomUser
from .models import Order, Product, ProductSubType, Customer, SubOrder


class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", 'is_counter_staff', 'is_manager', 'password']


class OrderQueryForm(forms.Form):
    start_date = forms.DateTimeField(widget=forms.SelectDateWidget(), label="from")
    end_date = forms.DateTimeField(widget=forms.SelectDateWidget(), label="to")


class OrderQueryStaffForm(forms.Form):
    staff = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_counter_staff = True),  label="staff name")
    start_date = forms.DateTimeField(widget=forms.SelectDateWidget(), label="from")
    end_date = forms.DateTimeField(widget=forms.SelectDateWidget(), label="to")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer',)


class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('job_name', 'deposit', 'discount',)


class SubOrderForm(forms.ModelForm):
    class Meta:
        model = SubOrder
        fields = ('product_ordered', 'length', 'breadth', 'quantity',)
        widgets = {
            'product_ordered': Select(attrs={'required':True}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name',)


class ProductSubTypeForm(forms.ModelForm):
    class Meta:
        model = ProductSubType
        fields = ('sub_type_name', "price")


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ('created_by', 'date_created')
