from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """
            Initialize the cart.
        """
        self.session = request.session
        self.user = request.user # تخزين المستخدم المسجل
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        # اختر السعر المناسب حسب نوع المستخدم
        if self.user.is_authenticated and hasattr(self.user, 'is_vendor'):
            price = product.price_vendor if self.user.is_vendor else product.price_customer
        else:
            price = product.price_customer

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity':0,
                'price': str(price)}
            
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
            Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """
            Iterate over the items in the cart and get the products
            from the database.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
        
    def __len__(self):
        """
         Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def get_subtotal_price(self):
        """
        حساب السعر الإجمالي الأساسي (بدون ضرائب).
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_tax(self):
        """
        حساب إجمالي قيمة الضريبة لجميع المنتجات في السلة (فقط للتجار في بلجيكا).
        """
        total_tax = Decimal('0.00')
        
        # لا يتم حساب الضريبة إلا إذا كان المستخدم تاجرًا في بلجيكا
        if not (self.user.is_authenticated and self.user.is_vendor and hasattr(self.user, 'country') and self.user.country == 'BE'):
            return total_tax

        # إذا كان تاجرًا في بلجيكا، استمر في الحساب
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        product_map = {str(p.id): p for p in products}

        for product_id, item in cart.items():
            product = product_map.get(product_id)
            if product:
                tax_rate = Decimal('0.00')
                if product.tax_type == 'food':
                    tax_rate = Decimal('0.06')
                elif product.tax_type == 'home':
                    tax_rate = Decimal('0.21')
                
                base_price = Decimal(item['price']) * item['quantity']
                total_tax += base_price * tax_rate
                
        return total_tax


    def get_total_price_with_tax(self):
        """
        حساب السعر النهائي شامل الضريبة.
        """
        return self.get_subtotal_price() + self.get_total_tax()
