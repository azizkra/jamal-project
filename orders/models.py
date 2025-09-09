from django.utils.translation import gettext_lazy as _
from django.db import models
from shop.models import Product
from django.conf import settings
from decimal import Decimal
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(_('first name'),max_length=50)
    last_name = models.CharField(_('last name'),max_length=50)
    email = models.EmailField(_('e-mail'))
    phone = models.CharField(_('phone'), max_length=20) 
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal_code'), max_length=20)
    city = models.CharField(_('city'), max_length=100)
    residence_place = models.CharField(_('residence_place'), max_length=100)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    paid = models.BooleanField(_('paid'), default=False)
    is_delivired = models.BooleanField(_('is_delivired'), default=False, null=True, blank=True)
    stripe_id = models.CharField(_('stripe_id'), max_length=250, blank=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    # We can also include a link to each payment ID to see the payment details in the Stripe dashboard
    def get_stripe_url(self):
        if not self.stripe_id:
            # no payment associated
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Stripe path for test payments
            path = '/test/'
        else:
            # Stripe path for real payments
            path = '/'
        return  f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
    
    # ✅ا: حساب الإجمالي بدون ضريبة
    def get_total_cost_without_tax(self):
        # تستدعي دالة get_base_cost() من كل OrderItem
        return sum(item.get_base_cost() for item in self.items.all())
    
     #✅ ا حساب إجمالي الضريبة فقط
    def get_total_tax(self):
        # تحسب الفرق بين الإجمالي مع الضريبة والإجمالي بدونها
        return self.get_total_cost() - self.get_total_cost_without_tax()

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_tax_rate(self):
        """
        تحديد نسبة الضريبة بناءً على بلد المستخدم ونوع المنتج.
        """
        user = self.order.user
        # تحقق من أن المستخدم مسجل وله بلد محدد
        if user and user.is_authenticated and user.is_vendor and hasattr(user, 'country') and user.country == "BE":  # مستخدم داخل بلجيكا
            if self.product.tax_type == 'food':
                return Decimal('0.06')  # 6% للمواد الغذائية
            elif self.product.tax_type == 'home':
                return Decimal('0.21')  # 21% للأدوات المنزلية
        
        # إذا كان المستخدم خارج بلجيكا أو غير مسجل، لا توجد ضريبة
        return Decimal('0.00')

    def get_cost(self):
        """
        حساب التكلفة الإجمالية للمنتج شاملة الضريبة.
        """
        base_cost = self.price * self.quantity
        tax_rate = self.get_tax_rate()
        tax = base_cost * tax_rate
        return base_cost + tax

    def get_base_cost(self):
        """
        حساب التكلفة الأساسية للمنتج (بدون ضريبة).
        """
        return self.price * self.quantity


class SalesLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales_as_vendor')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales_as_customer')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    sold_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} x{self.quantity} sold to {self.customer} at {self.sold_at}"

