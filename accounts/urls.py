from django.urls import path, include
from .views import loginpage, homepage, teacher_dashboard, logout_view


app_name = 'accounts'

urlpatterns = [


    path('login/', loginpage, name='login'),
    path('', homepage, name = 'home_page'),
    path('logout/', logout_view, name = 'logout'),

]


