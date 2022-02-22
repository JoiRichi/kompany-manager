from datetime import datetime, timedelta

from django.db import models

from accounts.models import CustomUser
from . import tests


class Customer(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    company_name = models.CharField(max_length=300)
    customer_full_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=11, unique=True)
    date_created = models.DateTimeField(default=datetime.now())
    address = models.CharField(max_length=300)

    def __str__(self):
        return '{} {}'.format(self.company_name, self.customer_full_name)

    def get_details(self):
        details = {
            "full_name": "{} {}".format(self.customer_first_name.capitalize(), self.customer_last_name.capitalize()),
            "phone_number": self.phone_number,
            "created_by": self.created_by,
            "date_created": self.date_created,

            "transaction_history": self.get_transaction_history(),
            }
        return details

    def get_transaction_history(self):
        details = {
            "all_orders": Order.objects.filter(customer=self).order_by("date_created"),
            'outstanding_orders': Order.objects.filter(customer=self, order_completed=True, paid_fully=False).order_by(
                "date_created"),

        }
        return details


class Product(models.Model):
    product_name = models.CharField(max_length=300)
    date_created = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.product_name

    def get_product_details(self):
        details = {
            'product_name': self.product_name,
            'product_id': self.id,
            'date_created': self.date_created,
            'product_sub_types': ProductSubType.objects.filter(product=self),

        }
        return details

    def product_sub_type_details(self):
        details = {
            'product_sub_types': ProductSubType.objects.filter(product=self),

        }


class ProductSubType(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    sub_type_name = models.CharField(max_length=300)
    price = models.FloatField(default=0)
    last_price_changed_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_type_name

PAYMENT_MODE = (
    ("cash", "cash"),
    ("pos", "POS"),
    ("transfer", "transfer"),

)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    counter_staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name= 'counter_staff')
    job_name = models.CharField(default="", max_length=50)
    total_order_price = models.FloatField(default=0)
    date_created = models.DateTimeField(default=datetime.now())
    order_completed = models.BooleanField(default=False)
    paid_fully = models.BooleanField(default=False)
    deposit = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    discount_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    payment_mode = models.CharField(max_length=30,choices=PAYMENT_MODE, default='cash')
    balance = models.FloatField(default=0)

    # balance is debt!
    def save_order(self):
        self.balance = self.total_order_price - self.deposit + self.discount
        if self.total_order_price == self.discount + self.deposit - self.balance:
            self.paid_fully = True
            self.save()
            tests.affirm_order_balance(self)
        self.save()
        tests.affirm_order_balance(self)
        return self

    def paid_balance(self):
        self.deposit = self.discount + self.balance
        self.balance = 0
        self.save()
        tests.affirm_order_balance(self)
        return self

    def __str__(self):
        return "Order ID: {}, Order Total: {}".format(self.id, str(self.total_order_price))

    def get_order_details(self):
        total_payment_made = self.total_order_price - self.discount - self.balance
        total_debt = self.total_order_price - self.discount - self.deposit
        # assert total_debt+total_payment_made+self.discount == self.total_order_price
        return {
            'customer': self.customer,
            'total_payment_made': total_payment_made,
            'total_debt': total_debt,
            'sub_order_details': self.get_sub_order_details()
        }

    def get_sub_order_details(self):
        sub_orders = SubOrder.objects.filter(order=self)

        return sub_orders


class SubOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product_ordered = models.ForeignKey(ProductSubType, on_delete=models.CASCADE, blank=True, null=True)
    length =  models.FloatField(default=1)
    breadth = models.FloatField(default=1)
    quantity = models.FloatField(default=0)
    buy_price = models.FloatField(default=0)
    sub_order_total = models.FloatField(default=0)

    def __str__(self):
        return '{} {} at NGN {} ({} by {})'.format(self.product_ordered.sub_type_name, self.quantity, self.buy_price,
                                                   self.length,
                                                   self.breadth)


def get_total_financial_record():
    pass




def get_orders_based_on_date_and_staff(start_date, end_date, staff_id):
    staff = CustomUser.objects.get(id=staff_id)
    orders = Order.objects.filter(date_created__range=[start_date, end_date + timedelta(days=1)]).filter(
        order_completed=True, counter_staff = staff)
    c_total_order_price = 0
    total_discount = 0
    total_funds_received = 0
    total_outstanding_funds = 0
    for order in orders:
        c_total_order_price += order.total_order_price
        total_funds_received += order.deposit
        total_discount += order.discount
        total_outstanding_funds += order.balance
    try:
        assert total_outstanding_funds + total_funds_received + total_discount == c_total_order_price
        return {

            'start_date': start_date,
            'end_date': end_date,
            'total_discount': total_discount,
            'c_total_order_price': c_total_order_price,
            'total_funds_received': total_funds_received,
            'total_outstanding_funds': total_outstanding_funds,

        }
    except AssertionError:
        return {'error': "An embezzlement is happening"}


def get_orders_based_on_date(start_date, end_date):
    orders = Order.objects.filter(date_created__range=[start_date, end_date + timedelta(days=1)]).filter(
        order_completed=True)
    c_total_order_price = 0
    total_discount = 0
    total_funds_received = 0
    total_outstanding_funds = 0
    for order in orders:
        c_total_order_price += order.total_order_price
        total_funds_received += order.deposit
        total_discount += order.discount
        total_outstanding_funds += order.balance
    try:
        assert total_outstanding_funds + total_funds_received + total_discount == c_total_order_price
        return {
            'start_date': start_date,
            'end_date': end_date,
            'total_discount': total_discount,
            'c_total_order_price': c_total_order_price,
            'total_funds_received': total_funds_received,
            'total_outstanding_funds': total_outstanding_funds,

        }
    except AssertionError:
        return {'error': "An embezzlement is happening"}


def get_product_details_based_on_date(start_date, end_date):
    orders = Order.objects.filter(date_created__range=[start_date, end_date + timedelta(days=1)]).filter(
        order_completed=True)
    final_list = []
    all_sub_orders = []
    for each_order in orders:
        sub_orders = each_order.suborder_set.all()  # list of sub orders associated with a single order
        for each_sub_order in sub_orders:
            all_sub_orders.append(each_sub_order)

    for sub_product in ProductSubType.objects.all():
        sub_product_details = {'sub_product': sub_product,
                               'total_piece_ordered': 0,
                               'total_expected_income': 0,

                               }

        total_piece_ordered = 0
        list_of_prices = []
        list_of_quantities = []
        total_expected_income = 0
        for each_sub_order in all_sub_orders:
            if sub_product == each_sub_order.product_ordered:
                total_expected_income += each_sub_order.buy_price * each_sub_order.quantity
                total_piece_ordered += each_sub_order.quantity
                if each_sub_order.buy_price not in list_of_prices:
                    list_of_prices.append(each_sub_order.buy_price)
        for each_price in list_of_prices:
            quantity_at_that_price = 0
            for each_sub_order in all_sub_orders:
                if each_sub_order.buy_price == each_price:
                    quantity_at_that_price += each_sub_order.quantity
            list_of_quantities.append(quantity_at_that_price)
        sub_product_details.update({'total_piece_ordered': total_piece_ordered})
        sub_product_details.update({'total_expected_income': total_expected_income})
        sub_product_details.update({'price_list': [list_of_prices, list_of_quantities]})
        tests.affirm_accuracy_of_total(total_expected_income, [list_of_prices, list_of_quantities])
        final_list.append(sub_product_details)
    return final_list


def get_product_details_based_on_date_and_staff(start_date, end_date, staff_id):
    staff = CustomUser.objects.get(id=staff_id)
    orders = Order.objects.filter(date_created__range=[start_date, end_date + timedelta(days=1)]).filter(
        order_completed=True, counter_staff = staff )
    final_list = []
    all_sub_orders = []
    for each_order in orders:
        sub_orders = each_order.suborder_set.all()  # list of sub orders associated with a single order
        for each_sub_order in sub_orders:
            all_sub_orders.append(each_sub_order)

    for sub_product in ProductSubType.objects.all():
        sub_product_details = {'sub_product': sub_product,
                               'total_piece_ordered': 0,
                               'total_expected_income': 0,

                               }

        total_piece_ordered = 0
        list_of_prices = []
        list_of_quantities = []
        total_expected_income = 0
        for each_sub_order in all_sub_orders:
            if sub_product == each_sub_order.product_ordered:
                total_expected_income += each_sub_order.buy_price * each_sub_order.quantity
                total_piece_ordered += each_sub_order.quantity
                if each_sub_order.buy_price not in list_of_prices:
                    list_of_prices.append(each_sub_order.buy_price)
        for each_price in list_of_prices:
            quantity_at_that_price = 0
            for each_sub_order in all_sub_orders:
                if each_sub_order.buy_price == each_price:
                    quantity_at_that_price += each_sub_order.quantity
            list_of_quantities.append(quantity_at_that_price)
        sub_product_details.update({'total_piece_ordered': total_piece_ordered})
        sub_product_details.update({'total_expected_income': total_expected_income})
        sub_product_details.update({'price_list': [list_of_prices, list_of_quantities]})
        tests.affirm_accuracy_of_total(total_expected_income, [list_of_prices, list_of_quantities])
        final_list.append(sub_product_details)
    return final_list
