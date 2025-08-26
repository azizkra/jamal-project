from django import forms
from django.utils.translation import gettext_lazy as _



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label=_('Quantity'),
        widget=forms.NumberInput(attrs={
            "class": "form-control quantity-input",
            "value": 1
        })
        )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    def __init__(self, *args, stock=1000, **kwargs):
        super().__init__(*args, **kwargs)

        max_quantity = stock if stock > 0 else 1

        self.fields['quantity'].widget.attrs["max"] = max_quantity


