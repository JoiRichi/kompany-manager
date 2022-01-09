from django.contrib import admin
from .models import Costumer, Product, ProductSubType, Order, SubOrder
# Register your models here.
admin.site.register(Costumer)
admin.site.register(Product)
admin.site.register(ProductSubType)
admin.site.register(Order)
admin.site.register(SubOrder)