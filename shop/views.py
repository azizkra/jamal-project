from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import get_language
from parler.utils.context import switch_language
from datetime import timedelta
from django.utils import timezone
from cart.form import CartAddProductForm
from .forms import ContactForm
from .models import Product, Category, SaleRecord

# --- صفحات ثابتة ---
def privacy_policy(request):
    return render(request, 'others/privacy_policy.html')

def trems(request):
    return render(request, 'others/terms.html')

def about(request):
    return render(request, 'others/about.html')

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"رسالة من: {name} ({email})\n\n{message}"

            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False
            )
            return redirect('shop:contact_success')
    else:
        form = ContactForm()  # في حالة GET

    # هذا السطر يوضع خارج if-else ليعمل في كل الحالات
    return render(request, 'others/contact.html', {'form': form})


def contact_success(request):
    return render(request, 'others/contact_success.html')      

# --- البحث ---
def search_view(request):
    query = request.GET.get('q', '').strip()
    lang = get_language()

    if not query:
        results = Product.objects.active_translations(lang).all()
    else:
        results = Product.objects.filter(
            Q(translations__language_code=lang) &
            (
                Q(translations__name__icontains=query) |
                Q(translations__description__icontains=query) |
                Q(category__translations__language_code=lang,
                  category__translations__name__icontains=query)
            )
        ).distinct()

    return render(request, 'others/search_results.html', {
        'results': results,
        'query': query
    })

# --- تقرير المبيعات (للموظفين فقط) ---
@staff_member_required
def sales_report(request):
    sales = SaleRecord.objects.all().order_by('-purchase_time')
    return render(request, 'shop/sales/sales_report.html', {'sales': sales})

# --- عرض الفئات ---
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/product/categories.html', {'categories': categories})

# --- قائمة المنتجات (حسب الفئة) ---
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    language = get_language()

    # استخراج فئة New Arrivals
    try:
        new_arrivals_category = Category.objects.get(translations__language_code=language,
                                                     translations__slug='new-arrivals')
        # المنتجات الجديدة من خلال الفئة
        new_arrivals = Product.objects.filter(category=new_arrivals_category, stock__gt=0)
        new_arrival_ids = new_arrivals.values_list('id', flat=True)
    except Category.DoesNotExist:
        new_arrivals = Product.objects.none()
        new_arrival_ids = []
        
    # المنتجات المعروضة (باستثناء الجديدة)
    products = Product.objects.filter(stock__gt=0).exclude(id__in=new_arrival_ids).order_by('-created')  # فقط المنتجات المتوفرة

    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug
        )
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'new_arrivals': new_arrivals,
    })

# --- تفاصيل المنتج ---
def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True,
                                stock__gt=0
    )
    cart_product_form = CartAddProductForm(stock=product.stock)

    # منتجات مشابهة من نفس الفئة
    similar_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'similar_products': similar_products,
    })
