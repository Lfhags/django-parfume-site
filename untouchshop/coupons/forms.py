from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg rounded-start-4 border-brown',
            'placeholder': 'Введіть купон'
        })
    )