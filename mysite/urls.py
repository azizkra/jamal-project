from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.views.i18n import set_language

from payment import webhooks  # Webhook Stripe

# --- i18n PATTERNS (توجيهات تدعم الترجمة) ---
urlpatterns = i18n_patterns(
    # لوحة التحكم
    path('admin/', admin.site.urls),

    # التطبيقات الداخلية (مرتبة حسب الوظيفة)
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('orders/'), include('orders.urls', namespace='orders')),
    path(_('payment/'), include('payment.urls', namespace='payment')),
    path(_('account/'), include('account.urls', namespace='account')),

    # الترجمة (Rosetta)
    path(_('rosetta/'), include('rosetta.urls')),

    # المتجر (الرئيسية)
    path('', include('shop.urls', namespace='shop')),
)

# --- روابط إضافية ---
urlpatterns += [
    # Stripe Webhook
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),

    # تغيير اللغة
    path('i18n/setlang/', set_language, name='set_language'),
]

# --- ملفات Static و Media أثناء التطوير ---
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
