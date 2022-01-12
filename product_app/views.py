from datetime import datetime
from .forms import UserForm, ProductForm, ProductSubTypeForm, CostumerForm, SubOrderForm
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from decorators import  manager_required, counter_staff_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import CustomUser,Profile
from .models import Product, ProductSubType, Costumer, Order, SubOrder
from .forms import OrderQueryForm, OrderForm, OrderEditForm
from django.template.defaulttags import register
from.models import get_product_details_based_on_date, get_orders_based_on_date
from .pdfs import render_to_pdf, render_pdf_view
from django.utils.dateparse import  parse_datetime

from .tests import affirm_order_balance


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)



@register.filter
def analyze_nested_list(the_list, num='0'):
    final_list = []
    for a, b in zip(the_list[0], the_list[1]):
        final_list.append("{} pieces at NGN{}".format(str(b), str(a)))

    return final_list




@register.filter
def get_value_and_relation(dictionary, key):
    s= dictionary.get(key)
    b= s.product
    return  b






@manager_required()
def print_report(request, start_date, end_date):
    orders = get_orders_based_on_date(parse_datetime(start_date), parse_datetime(end_date))
    sub_products_details = get_product_details_based_on_date(parse_datetime(start_date), parse_datetime(end_date))
    products = Product.objects.all()
    context ={'orders': orders, 'products': products,
             'sub_products_details': sub_products_details, 'date' : datetime.now()}
    return render_pdf_view(request, 'manager_components/manager_report.html', context,
                           "{}--{}-report".format(parse_datetime(start_date), parse_datetime(end_date)))


@manager_required()
def print_costumer_report(request, costumer_id):
    costumer = Costumer.objects.get(id = costumer_id)
    orders = Order.objects.filter(costumer=costumer).order_by("date_created")
    c_total_order_price = 0
    total_discount = 0
    total_funds_received = 0
    total_outstanding_funds = 0
    for order in orders:
        c_total_order_price += order.total_order_price
        total_funds_received += order.deposit
        total_discount += order.discount
        total_outstanding_funds += order.balance
    assert total_outstanding_funds + total_funds_received + total_discount == c_total_order_price
    outstanding_orders = orders.filter(paid_fully=False)
    printed_date = datetime.now()
    context = {'orders': orders, 'outstanding_orders': outstanding_orders,
               'printed_date':printed_date, 'costumer':costumer,
              'c_total_order_price':c_total_order_price,
               'total_discount': total_discount,
                'total_funds_received': total_funds_received,
                'total_outstanding_funds': total_outstanding_funds,
    }
    return render_pdf_view(request, 'manager_components/manager_costumer_report.html', context,
                           "{}-report".format(costumer))


@counter_staff_required()
def pay_debt(request, order_id):
    order = Order.objects.get(id = order_id)
    order.deposit = order.balance + order.deposit
    order.balance = 0
    order.paid_fully = True
    order.save()
    return redirect(reverse("product_app:manage_debtors"))





@counter_staff_required()
def create_suborder(request, order_id):
    order = Order.objects.get(id=order_id)
    form = SubOrderForm(request.POST or None)
    if form.is_valid():
        a= form.save(commit=False)
        a.order = order
        a.save()
        return render(request, 'counter_components/subtable.html', {'form':form, 'order':order})
    else:
        return render(request, 'counter_components/sub_order_form.html', {'form':form, 'order':order})


def delete_suborder(request, sub_order_id):
    sub_order = SubOrder.objects.get(id=sub_order_id)
    order = sub_order.order
    sub_order.delete()
    return render(request, 'counter_components/subtable.html', {'order': order})






@manager_required()
def manager_dashboard(request):
    return render(request, 'manager_base.html',{})


@manager_required()
def staff_creation_page(request):
    all_staff = CustomUser.objects.all()
    return render(request, 'manager_components/staff_manager.html', {'all_staff':all_staff})


@manager_required()
def product_management_page(request):
    products = Product.objects.all()
    products = [product.get_product_details() for product in products]

    return render(request, 'product_page.html', {"products":products})


@manager_required()
def costumer_management_page(request):
    costumers = Costumer.objects.all()

    return render(request, 'costumer_page.html', {"costumers":costumers})


@manager_required()
def get_orders_based_on_date_func(request):
    form = OrderQueryForm(request.POST or None)
    if form.is_valid():
        print('form is valid')
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        #orders = Order.objects.filter(date_created__range=[start_date, end_date]).filter(order_completed=True)
        orders = get_orders_based_on_date(start_date, end_date)
        sub_products_details = get_product_details_based_on_date(start_date, end_date)
        products = Product.objects.all()
        return render(request, 'transaction_page.html', {'orders':orders,
                                                         'products':products, 'sub_products_details': sub_products_details})
    print('form invalid')
    return render(request, 'transactions_page.html', {'form':form})

    #Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"])

@manager_required()
def suspend(request, staff_id):
    staff = CustomUser.objects.get(id=staff_id)
    staff.is_suspended = True
    staff.save()
    return redirect(reverse('product_app:staff_lazy_loader'))

@manager_required()
def pardon(request, staff_id):
    staff = CustomUser.objects.get(id=staff_id)
    staff.is_suspended = False
    staff.save()
    return redirect(reverse('product_app:staff_lazy_loader'))



@manager_required()
def staff_lazy_page(request):
    all_staff = CustomUser.objects.all().exclude(is_superuser=True)
    return render(request, 'manager_components/staff_lazy_loader.html', {'all_staff':all_staff})

@manager_required()
def new_staff_creation(request):
    form1 = UserForm(request.POST or None)
    if form1.is_valid():
        form1.save()

    return render(request, 'manager_components/staff_creation.html', {'form1':form1})



@manager_required()
def product_edit_page(request, product_id):
    product = Product.objects.get(id = product_id)
    form = ProductForm(request.POST or None,instance=product)
    if form.is_valid():
        form.save()
        return redirect(reverse('product_app:manage_product'))
    else:
        return render(request, 'manager_components/product_edit_page.html', {'form': form, 'product':product})


@manager_required()
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('product_app:manage_product'))
    else:
        return render(request, 'manager_components/create_product.html', {'form': form})




@manager_required()
def sub_product_edit_page(request, sub_product_id):
    sub_product = ProductSubType.objects.get(id = sub_product_id)
    form = ProductSubTypeForm(request.POST or None,instance=sub_product)
    if form.is_valid():
        form.save()
        return redirect(reverse('product_app:manage_product'))
    else:
        return render(request, 'manager_components/sub_product_edit_page.html', {'form': form, 'sub_product':sub_product})

@manager_required()
def create_sub_product(request, product_id):
    product = Product.objects.get(id = product_id)
    form = ProductSubTypeForm(request.POST or None)
    if form.is_valid():
        a= form.save(commit=False)
        a.product = product
        a.save()
        return redirect(reverse('product_app:manage_product'))
    else:
        return render(request, 'manager_components/sub_product_create_page.html', {'form': form, 'product':product})




def complete_order(request, order_id):
    form = OrderEditForm(request.POST or None, instance= Order.objects.get(id=order_id))
    if form.is_valid():
        a=form.save(commit=False)
        a.counter_staff = request.user
        a.order_completed = True
        a.balance = a.total_order_price - (a.deposit + a.discount)
        if not a.balance:
            a.fully_paid = True
        affirm_order_balance(a)
        a.save()
        form = OrderForm(request.POST or None)
        return render(request, 'create_order.html', {'form':form, 'order':a})
    return redirect(reverse('product_app:counter_dashboard'))



def print_order_receipt(request, order_id):
    order = Order.objects.get(id=order_id)
    return render_pdf_view(request, 'counter_components/order_receipt.html',
                           {'order': order, 'date': datetime.now()}, '{}-{}'.format(order.costumer, datetime.now()))






@counter_staff_required()
def counter_dashboard(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save()
        form = OrderEditForm(request.POST or None, instance=order)

        return (render(request, 'counter_components/add_suborders.html', {'form':form, 'order':order}))
    else:

        return render(request, 'create_order.html', {'form':form})


@counter_staff_required()
def manage_debtors(request):
    outstanding_orders = Order.objects.filter(paid_fully=False, order_completed =True)
    debtors = []
    for outstanding_order in outstanding_orders:
        if not outstanding_order.costumer in debtors:
            debtors.append(outstanding_order.costumer)
    return render(request, 'counter_debtors.html', {"debtors": debtors, 'outstanding_orders': outstanding_orders})


@counter_staff_required()
def create_costumers(request):
    form = CostumerForm(request.POST or None)
    if form.is_valid():
        a = form.save(commit=False)
        a.created_by = request.user
        a.save()
        messages.success(request, "Costumer created successfully!")
        messages.success(request, "Kindly proceed to complete your order or you can create another costumer below")
        return render(request, 'create_costumer.html', {'form':form})
    return render(request, 'create_costumer.html', {'form':form})







@manager_required()
def staff_creation(request):
    try:
        user = CustomUser.objects.get(email=request.POST.get('email'))
        messages.error(request, "This email already exist, try again!")
        return redirect(reverse('product_app:staff_lazy_loader'))

    except ObjectDoesNotExist:
        new_user = CustomUser.objects.create_user(request.POST.get('email'), request.POST.get('password'))

        if request.POST.get('staff_type') == 'is_counter_staff':
            new_user.is_counter_staff = True
            new_user.save()
        elif request.POST.get('staff_type') == 'is_manager_staff':
            new_user.is_manager = True
            new_user.is_staff = True
            new_user.is_admin = True
            new_user.save()

        try:
            profile = Profile.objects.get(user=new_user)
        except ObjectDoesNotExist:
            new_profile = Profile.objects.create(first_name=request.POST.get('first_name'),
                                                 user=new_user,
                                                 last_name= request.POST.get('last_name'),
                                                 address=request.POST.get('address'),
                                                 phone_number= request.POST.get('phone_number'))


        all_staff = CustomUser.objects.all()
        user = request.user
        user_name = user.profile.first_name
        context = {
            'all_staff': all_staff,
            'user': user,
            'username': user_name,

        }
        return redirect(reverse('product_app:staff_lazy_loader'))

        #return redirect(reverse("product_app:manage_staff"))


@manager_required()
def staff_deletion(request, user_id):
    staff = CustomUser.objects.get(id=user_id)
    try:
        profile = staff.profile
        profile.delete()
    except ObjectDoesNotExist:
        pass
    staff.delete()

    return redirect('/staff')