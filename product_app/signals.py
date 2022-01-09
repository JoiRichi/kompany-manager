from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from.models import SubOrder, Order, Product
from django.shortcuts import HttpResponse
from . import tests




@receiver(post_save, sender=SubOrder)
def update_order(sender, instance, created, **kwargs):
    sub_orders = SubOrder.objects.filter(order= instance.order)
    products_subtypes = [subtypes.product_ordered for subtypes in sub_orders]
    total_order_price = 0
    for sub_order in sub_orders:
        for products_subtype in products_subtypes:
            qt = sub_order.quantity*products_subtype.price
            total_order_price+=qt
    order= instance.order
    order.total_order_price = total_order_price
    order.save()
    if created:
        a= instance.product_ordered.price
        instance.buy_price = a
        instance.save()









