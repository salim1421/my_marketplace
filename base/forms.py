from django import forms
from .models import Review
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'image',
            'body'
        ]

PAYMENT = [
    ('S', 'Stripe'),
    ('P', 'PayPal')
]


class CheckoutForm(forms.Form):
    address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '1234 Main Str'
        }),
    )
    zip_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder':'123-123'
            }
        )
    )
    country = CountryField(blank_label=('select country')).formfield(widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        })
    )
    save_info = forms.BooleanField(required=False)
    same_billing_info = forms.BooleanField(required=False)
    payment = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT
    )

