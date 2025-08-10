from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserRegistrainForm(UserCreationForm):
    is_vendor = forms.BooleanField(required=False, label=_('Are you a merchant?'))
    tax_number = forms.CharField(required=False, label=_('Tax number'))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_vendor', 'tax_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إضافة كلاس bootstrap لكل الحقول
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                # لجعل checkbox يظهر بشكل صحيح، يمكننا التعامل معه بشكل منفصل
                if isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = 'form-check-input'
                else:
                    field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        is_vendor = cleaned_data.get('is_vendor')
        tax_number = cleaned_data.get('tax_number')

        if is_vendor and not tax_number:
            self.add_error('tax_number', _('Merchant tax number must be entered'))

        if not is_vendor and tax_number:
            self.add_error('is_vendor', _('You must specify that you are a merchant if you enter your tax number.'))