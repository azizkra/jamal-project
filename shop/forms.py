from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="name", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Write Your Name'
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Write Your E-mail'
    }))
    subject = forms.CharField(label="Subject", max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Write Your Subject'
    }))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Write Your Message', 'rows': 5
    }))