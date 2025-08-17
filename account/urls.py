from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

app_name = 'account'

urlpatterns = [
    path('register/', views.register , name='register'),
    path('login/', views.CustomLoginView, name='login'),
    path('account/logout/', LogoutView.as_view(), name='account_logout'),
    path('vendor/profile/', views.vendor_profile, name='vendor_profile'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),

    path('set-theme/', views.set_theme, name='set_theme'),
]