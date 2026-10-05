from django import forms
from django.utils import timezone
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests']
        widgets = {
            'check_in': DateInput(attrs={'class': 'form-control'}),
            'check_out': DateInput(attrs={'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        guests = cleaned.get('guests')

        if not self.room:
            raise forms.ValidationError('Room is required.')

        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError('Check-out must be after check-in.')
            if check_in < timezone.localdate():
                raise forms.ValidationError('Check-in cannot be in the past.')

            # منع تداخل الحجز لنفس الغرفة
            overlap = Booking.objects.filter(
                room=self.room,
                check_in__lt=check_out,
                check_out__gt=check_in,
            ).exists()
            if overlap:
                raise forms.ValidationError('Selected dates are not available for this room.')

        if guests and guests > self.room.capacity:
            raise forms.ValidationError(f'Max guests for this room is {self.room.capacity}.')

        return cleaned

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
