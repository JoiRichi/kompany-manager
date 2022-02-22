from django.contrib.auth.views import PasswordChangeView
from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render



app_name = 'product_app'

urlpatterns = [
    path('manager/manage_staff/history/', views.staff_history_page, name= "manage_staff_history"),
    path('manager/manage_staff/history/loader/<start_date>/<end_date>/<int:staff_id>/', views.staff_history_page_lazy, name="staff_report_loader"),

    path('manager/manage_staff/history/report/', views.get_orders_based_on_date_and_staff_func, name="manage_staff_transactions"),

    path('manager/manage_staff/', views.staff_creation_page, name="manage_staff"),
    path('manager/manage_staff/suspend/<int:staff_id>/', views.suspend, name="suspend_staff"),
    path('manager/manage_staff/pardon/<int:staff_id>/', views.pardon, name="pardon_staff"),

    path('manager/manage_product/', views.product_management_page, name="manage_product"),
    path('manager/manage_product/create_product/', views.create_product, name="create_product"),

    path('manager/manage_product/edit_product_page/<int:product_id>/', views.product_edit_page, name="edit_product"),

    path('manager/manage_product/edit_sub_product_page/<int:sub_product_id>/', views.sub_product_edit_page,
         name="edit_sub_product"),

    path('manager/manage_product/create_sub_product_page/<int:product_id>/', views.create_sub_product,
         name="create_sub_product"),

    path('manager/manage_customer/', views.customer_management_page, name="manage_customer"),
    path('manager/', views.get_orders_based_on_date_func, name="manage_transactions"),
    # path('manager/manage_transactions/search', views.get_orders_based_on_date, name="submit_search"),
    path('manager/manage_transactions/print_report/<start_date>/<end_date>/', views.print_report, name="print_report"),
    path('manager/manage_transactions/print_customer_report/<int:customer_id>/', views.print_customer_report,
         name="print_customer_report"),

    path('counter_staff/', views.counter_dashboard, name="counter_dashboard"),
    path('counter_staff/manage_debtors-balances/', views.manage_debtors, name="manage_debtors"),
    path('counter_staff/manage_debtors-balances/pay_debt/<int:order_id>/', views.pay_debt,
         name="pay_debt"),
    path('counter_staff/create_customers/', views.create_customers, name="create_customers"),
    path('counter_staff/', views.counter_dashboard, name="counter_dashboard"),
    path('counter_staff/create_sub_order/<int:order_id>/', views.create_suborder, name="create_sub_order"),
    path('counter_staff/delete_sub_order/<int:sub_order_id>/', views.delete_suborder, name="delete_sub_order"),
    path('counter_staff/complete_order/<int:order_id>', views.complete_order, name="complete_order"),
    path('counter_staff/complete_order/print_receipt/<int:order_id>', views.print_order_receipt,
         name="print_order_receipt"),

    path('staff/create-staff', views.staff_creation, name='create_staff'),
    path('staff/create_new_staff', views.new_staff_creation, name='staff_creation'),
    path('staff/all_staff', views.staff_lazy_page, name='staff_lazy_loader'),

    path('staff/<int:user_id>/fire-staff', views.staff_deletion, name='delete_staff'),

]
