from django.contrib import messages
from orders.models import OrderItem
from .form import CustomUserRegistrainForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrainForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Account created and login successful.'))
            if user.is_vendor:
                return redirect('account:vendor_profile') # اسم الصفحة الخاصة بالتاجر
            else:
                return redirect('account:customer_profile') # اسم الصفحة الخاصة بالزبون
        else:
            messages.error(request, _('An error occurred while creating your account. Please check your data.'))
    else:
        form = CustomUserRegistrainForm()
    return render(request, 'account/register.html', {'form':form})


def CustomLoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _('You have successfully logged in.'))
            if user.is_vendor:
                return redirect('account:vendor_profile') # اسم الصفحة الخاصة بالتاجر
            else:
                return redirect('account:customer_profile') # اسم الصفحة الخاصة بالتاجر
        else:
            messages.error(request, _('Incorrect username or password'))
    return render(request, 'account/login.html')



@login_required
def vendor_profile(request):
    if not request.user.is_vendor:
        return redirect('account:customer_profile')
    
    # purchased_products = request.user.purchased_products.all()
    purchased_products = OrderItem.objects.filter(order__user=request.user).select_related('product')
    return render(request, 'account/vendor_profile.html', {'purchased_products': purchased_products})



@login_required
def customer_profile(request):
    if request.user.is_vendor:
        return redirect('account:vendor_profile')
    
    purchased_products = OrderItem.objects.filter(order__user=request.user).select_related('product')
    # purchased_products = request.user.purchased_products.all()
    return render(request, 'account/customer_profile.html', {'purchased_products': purchased_products})

