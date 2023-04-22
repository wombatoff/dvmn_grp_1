from datetime import date, timedelta
from django import forms
from django.forms.widgets import SelectDateWidget
from django.core.validators import MinValueValidator

from .models import Rental


class RentalForm(forms.ModelForm):
    min_end_date = date.today() + timedelta(days=30)
    start_date = forms.DateField(
        label='Дата начала аренды',
        widget=SelectDateWidget(),
        initial=date.today,
        validators=[MinValueValidator(limit_value=date.today)]
    )
    end_date = forms.DateField(
        label='Дата окончания аренды',
        widget=SelectDateWidget(),
        initial=min_end_date,
        validators=[MinValueValidator(limit_value=min_end_date)]
    )

    class Meta:
        model = Rental
        fields = ['start_date', 'end_date']
