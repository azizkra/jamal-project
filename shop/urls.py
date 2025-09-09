from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # --- صفحات ثابتة ---
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('trems-of-service/', views.trems, name='trems'),
    path('about-us/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),


    # --- البحث ---
    path('search/', views.search_view, name='product_search'),

    # --- تقارير ---
    path('sales-report/', views.sales_report, name='sales_report'),

    # --- المنتجات والفئات ---
    path('categories/', views.category_list, name='category_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # --- الرئيسية: قائمة المنتجات ---
    # path('', views.product_list, name='product_list'),
    path('', cache_page(60 * 15)(views.product_list), name='product_list'),
]
