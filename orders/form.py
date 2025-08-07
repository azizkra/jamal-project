from django import forms
from .models import Order
from localflavor.us.forms import USZipCodeField
from django.core.validators import RegexValidator

class OrderCreateForm(forms.ModelForm):
    postal_code = forms.CharField(
        max_length=12,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\- ]{3,12}$',
                message="يرجى إدخال رمز بريدي صالح (3 إلى 12 حرفًا أو رقمًا)."
            )
        ]
    )
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone','address',
                  'postal_code', 'residence_place', 'city']