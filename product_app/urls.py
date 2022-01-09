from django.urls import path
from . import views

app_name = 'product_app'



urlpatterns = [
    #path('manager/', views.manager_dashboard, name= "manager_dashboard"),
    path('manager/manage_staff/', views.staff_creation_page, name= "manage_staff"),
    path('manager/manage_staff/suspend/<int:staff_id>', views.suspend, name="suspend_staff"),
    path('manager/manage_staff/pardon/<int:staff_id>', views.pardon, name="pardon_staff"),


    path('manager/manage_product/', views.product_management_page, name= "manage_product"),
    path('manager/manage_costumer/', views.costumer_management_page, name="manage_costumer"),
    path('manager/', views.get_orders_based_on_date_func, name="manage_transactions"),
    #path('manager/manage_transactions/search', views.get_orders_based_on_date, name="submit_search"),
    path('manager/manage_transactions/print_report/<start_date>/<end_date>/', views.print_report, name="print_report"),
    path('manager/manage_transactions/print_costumer_report/<int:costumer_id>/', views.print_costumer_report, name="print_costumer_report"),







    path('counter_staff/', views.counter_dashboard, name="counter_dashboard"),
    path('counter_staff/manage_debtors-balances/', views.manage_debtors, name="manage_debtors"),
    path('counter_staff/manage_debtors-balances/pay_debt/<int:order_id>/', views.pay_debt,
             name="pay_debt"),
    path('counter_staff/create_costumers/', views.create_costumers, name="create_costumers"),
    path('counter_staff/', views.counter_dashboard, name="counter_dashboard"),






    path('staff/create-staff', views.staff_creation, name='create_staff'),
    path('staff/create_new_staff', views.new_staff_creation, name='staff_creation'),
    path('staff/all_staff', views.staff_lazy_page, name='staff_lazy_loader'),

    path('staff/<int:user_id>/fire-staff', views.staff_deletion, name='delete_staff'),
]