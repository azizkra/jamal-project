from django.shortcuts import render, redirect, reverse, get_object_or_404
from decimal import Decimal
import stripe
from django.conf import settings
from orders.models import Order
# Create your views here.

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # add order items to the Stripe checkout session
        for item in order.items.all():
            # ✅ حساب السعر الإجمالي للوحدة الواحدة شامل الضريبة
            # (سعر الوحدة * (1 + نسبة الضريبة))
            unit_price_with_tax = item.price * (Decimal('1.0') + item.get_tax_rate())
            session_data['line_items'].append({
                'price_data': {
                    # ✅ Stripe إرسال السعر الجديد إلى
                    'unit_amount': int(unit_price_with_tax * Decimal('100')),
                    'currency': 'usd',
                    'product_data':{
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })
        
        # إنشاء جلسة الدفع
        session = stripe.checkout.Session.create(**session_data)

        # التحويل لصفحة الدفع
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())



def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')