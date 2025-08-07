from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        slug = models.SlugField(max_length=200, unique=True),
    )
    image_1 = models.ImageField(upload_to='category/%Y/%m/%d', blank=True,null=True)
    
    class Meta:
        # ordering = ['name']
        # indexes = [
        #     models.Index(fields=['name']),
        # ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
    

class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        slug = models.SlugField(max_length=200),
        description = models.TextField(blank=True, null=True),
        brand = models.CharField(max_length=255,blank=True, null=True),
        style = models.CharField(max_length=255,blank=True, null=True),
        color = models.CharField(max_length=255,blank=True, null=True),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image_1 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True,null=True)
    image_2 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True,null=True)
    image_3 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True,null=True)
    image_4 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True,null=True)
    stock = models.PositiveIntegerField(default=0)
    price_customer = models.DecimalField(max_digits=10, decimal_places=2)
    price_vendor = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        # ordering = ['name']
        indexes = [
            # models.Index(fields=['id', 'slug']),
            # models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.safe_translation_getter('name', super().__str__())
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    


class SaleRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    buyer_name = models.CharField(max_length=100)
    buyer_phone = models.CharField(max_length=100)
    buyer_email = models.EmailField(blank=True)
    purchase_time = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'{self.product.name} - {self.quantity} pcs - {self.total_price}$'

    