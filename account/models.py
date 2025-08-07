from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    tax_number = models.CharField(max_length=50, blank=True, null=True)
    purchased_products = models.ManyToManyField('shop.product', related_name='buyers_purchased', blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )
