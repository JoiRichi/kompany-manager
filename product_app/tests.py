from django.test import TestCase


def affirm_order_balance(obj):
    total_payment_made = obj.total_order_price - obj.discount - obj.balance
    total_debt = obj.total_order_price - obj.discount - obj.deposit
    assert total_debt + total_payment_made + obj.discount == obj.total_order_price


def affirm_accuracy_of_total(total:int, list_of_list_of_values:list):
    try:
        result = sum([a*b for a, b in zip(list_of_list_of_values[0], list_of_list_of_values[1])])
        assert total == result

    except AssertionError:
        raise ArithmeticError()
