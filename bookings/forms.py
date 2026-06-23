from django import forms
from django.utils import timezone
from .models import Booking

class BookingWebForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        now = timezone.now()

        if start_date:
            if start_date < now - timezone.timedelta(minutes=1):
                raise forms.ValidationError("Дата початку не може бути в минулому.")

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("Дата завершення має бути пізніше дати початку.")

        return cleaned_data