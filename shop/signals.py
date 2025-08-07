from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Product
from account.models import CustomUser
@receiver(post_save, sender=Product)
def notify_users_on_new_product(sender, instance, created, **kwargs):
    if created:
        subject = f"منتج جديد: {instance.name}"
        message = f"تمت إضافة منتج جديد: {instance.name}\n\nالوصف: {instance.description}\n"
        recipient_list = list(CustomUser.objects.exclude(email='').values_list('email', flat=True))

        if recipient_list:
            send_mail(subject, message, None, recipient_list, fail_silently=True)