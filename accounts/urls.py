from django.urls import path, include
from .views import loginpage,  logout_view


app_name = 'accounts'

urlpatterns = [


    path('login/', loginpage, name='login'),
    path('logout/', logout_view, name = 'logout'),

]


