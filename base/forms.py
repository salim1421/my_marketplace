from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'image',
            'body'
        ]


class CheckoutForm(forms.Form):
    pass
