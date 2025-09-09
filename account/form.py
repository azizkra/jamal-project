from django import forms
from .models import CustomUser
from django_countries.fields import CountryField
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class CustomUserRegistrainForm(UserCreationForm):
    is_vendor = forms.BooleanField(required=False, label=_('Are you a merchant?'))
    tax_number = forms.CharField(required=False, label=_('Tax number'))
    # ✅ الخطوة 1: إضافة حقل البلد
    # نستخدم CountryField الذي يأتي من مكتبة django-countries
    # to_field_name='code' سيضمن حفظ رمز البلد (مثل 'BE') في قاعدة البيانات
    country = CountryField(blank_label=_('Select country')).formfield(
        label=_('Country'),
        widget=forms.Select(attrs={'class': 'form-select'}) # استخدام form-select ليتناسب مع Bootstrap
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_vendor', 'tax_number','country', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تعديل الكلاسات لـ Bootstrap
        for field_name, field in self.fields.items():
            # تخطي حقل البلد لأننا قمنا بتعيين الكلاس الخاص به بالفعل
            if field_name == 'country':
                continue
            
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                # إضافة form-control إلى الحقول الأخرى
                current_class = field.widget.attrs.get('class', '')
                if 'form-control' not in current_class:
                    field.widget.attrs['class'] = f'{current_class} form-control'.strip()

    def clean(self):
        cleaned_data = super().clean()
        is_vendor = cleaned_data.get('is_vendor')
        tax_number = cleaned_data.get('tax_number')

        if is_vendor and not tax_number:
            self.add_error('tax_number', _('Merchant tax number must be entered'))

        if not is_vendor and tax_number:
            self.add_error('is_vendor', _('You must specify that you are a merchant if you enter your tax number.'))