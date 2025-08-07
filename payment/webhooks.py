import stripe
import json
import logging
import stripe.error
import stripe.webhook
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)
    
    print("Received event:", event['type'])

    # ✅ عندما يتم الدفع بنجاح
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("Session:", json.dumps(session, indent=2))

        if session.get('mode') == 'payment' and session.get('payment_status') == 'paid':
            
            try:
                order = Order.objects.get(id=session.get('client_reference_id'))
            except Order.DoesNotExist:
                logging.warning("Order not found")
                return HttpResponse(status=400)

            # 🧾 تسجيل كل منتج تم بيعه في SalesLog
            
            order.paid = True
            order.stripe_id = session.get('payment_intent')
            order.save()

    return HttpResponse(status=200)
