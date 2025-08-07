from django import forms
from django.utils.translation import gettext_lazy as _



class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(coerce=int, label=_('Quantity'))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    def __init__(self, *args, stock=1000, **kwargs):
        super().__init__(*args, **kwargs)

        max_quantity = stock if stock > 0 else 1

        self.fields['quantity'].choices = [(i, str(i)) for i in range(1, max_quantity + 1)]


