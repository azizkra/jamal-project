from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    tax_number = models.CharField(max_length=50, blank=True, null=True)
    country = CountryField(blank=True, null=True)
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
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    theme_preference = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='light',
        blank=True,
        null=True
    )
