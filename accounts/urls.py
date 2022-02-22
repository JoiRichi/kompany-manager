from django.contrib.auth.views import PasswordChangeView
from django.urls import path, reverse
from django.shortcuts import redirect
from .views import loginpage, logout_view



def check_user(request):
    user = request.get.user
    if user.is_authenticated:
        if user.is_manager:
            return redirect(reverse('product_App:manager_dashboard'))
        elif user.is_counter_staff():
            return redirect(reverse('product_App:counter_dashboard'))
    return redirect('login/')




app_name = 'accounts'

urlpatterns = [

    path('login/', loginpage, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/check_user/',check_user, name='check_user'),
    path('change-password/', PasswordChangeView.as_view(template_name='change_password.html', success_url = 'check_user/'
        ), name='change_password'),
]



