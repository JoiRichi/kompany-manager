from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, HttpResponse

from .forms import LoginForm


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))



def handle404(request, exception):
    messages.warning(request, "The page you just tried to access does not exist, please login again")
    return redirect('accounts:login')



def loginpage(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_manager or user.is_director:
                return redirect(reverse('product_app:manage_transactions'))
            elif user.is_counter_staff:
                return redirect(reverse('product_app:counter_dashboard'))
            else:
                return redirect(reverse('accounts:login'))

        else:
            context = {'form': form,
                       'error': 'incorrect details!'
                       }
            return render(request, 'login.html', context)

    else:
        context = {'form': form}
        return render(request, 'login.html', context)
