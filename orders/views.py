from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import weasyprint
from django.core.exceptions import ValidationError

from .models import OrderItem, Order
from .form import OrderCreateForm
from shop.models import SaleRecord
from cart.cart import Cart
from django.contrib import messages


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # إنشاء الطلب وربط المستخدم به
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            

            # التعامل مع العناصر في السلة
            for item in cart:
                product = item['product']
                quantity = item['quantity']

                if product.stock < quantity:
                    raise ValidationError(f"الكمية غير كافية في المخزون للمنتج: {product.name}")

                product.stock -= quantity
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=quantity
                )

                SaleRecord.objects.create(
                    product=product,
                    quantity=quantity,
                    total_price=item['price'] * quantity,
                    buyer=request.user if request.user.is_authenticated else None,
                    buyer_name=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
                    buyer_email=form.cleaned_data['email'],
                    buyer_phone=form.cleaned_data['phone']
                )

            cart.clear()
            request.session['order_id'] = order.id
            # ✅ رسالة نجاح
            messages.success(request, "✅ تم إنشاء الطلب بنجاح! يرجى متابعة الدفع.")
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    )
    return response
