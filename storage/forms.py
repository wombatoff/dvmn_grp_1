from django import forms
from django.forms import TextInput
from phonenumber_field.formfields import PhoneNumberField


class RentBoxForm(forms.Form):
    rental_period_months = forms.IntegerField(
        min_value=1,
        label='Срок аренды, месяцев',
        widget=TextInput(attrs={
            'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Введите срок аренды, месяцев',
            'required': True
        })
    )
    phone = PhoneNumberField(
        required=False,
        label='Телефон',
        widget=TextInput(attrs={
            'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Укажите ваш телефон',
        })
    )
