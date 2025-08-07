from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from django.contrib import messages
from .form import CartAddProductForm

# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])

        # ✅ عرض رسالة
        if cd['override']:
            messages.success(request, f"✅ تم تحديث الكمية لـ {product.name}.")
        else:
            messages.success(request, f"✅ تم إضافة {product.name} إلى العربة.")
    else:
        messages.error(request, "❌ لم يتمكن من إضافة المنتج، تحقق من النموذج.")
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    # ✅ عرض رسالة
    messages.success(request, f"🗑 تم إزالة {product.name} من العربة.")
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        product = item['product']
        item['update_quantity_form'] = CartAddProductForm(
            stock=product.stock,
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )
    return render(request, 'cart/detail.html', {'cart': cart})
