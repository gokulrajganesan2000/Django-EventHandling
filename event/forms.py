from django import forms
from django.forms import ModelForm
from .models import Events

class DateInput(forms.DateInput):
    input_type='date'

class TimeInput(forms.TimeInput):
    input_type='time'

class EmailInput(forms.EmailInput):
    input_type='email'

class NumberInput(forms.NumberInput):
    input_type='number'

class URLInput(forms.URLInput):
    input_type='url'


class EventPostForm(ModelForm):
    class Meta:
        model=Events
        widgets={'event_date':DateInput(),'requested_time':TimeInput(),'email':EmailInput,'phone':NumberInput,'url':URLInput}
        fields=['title','description','organizer','event_date','email','phone','url','poster','requested_time','purpose','department']
