from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from.models import SubOrder, Order, Product
from django.shortcuts import HttpResponse
from . import tests




@receiver(post_save, sender=SubOrder)
def update_order(sender, instance, created, **kwargs):
    sub_orders = SubOrder.objects.filter(order= instance.order)
    total_order_price = 0
    for sub_order in sub_orders:
        qt = sub_order.quantity * sub_order.buy_price
        total_order_price += qt
    order = instance.order
    order.total_order_price = total_order_price
    order.save()

    if created:
        a= instance.product_ordered.price
        instance.buy_price = a
        instance.save()


@receiver(post_delete, sender=SubOrder)
def update_order_on_delete(sender, instance, **kwargs):
    try:
        sub_orders = SubOrder.objects.filter(order= instance.order)
        total_order_price = 0
        for sub_order in sub_orders:
            qt = sub_order.quantity * sub_order.buy_price
            total_order_price += qt
        order = instance.order
        order.total_order_price = total_order_price
        order.save()
    except ObjectDoesNotExist:
        pass









