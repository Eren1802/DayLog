from django import forms

class DailyLogForm(forms.Form):
    done = forms.CharField(required=True)
    pending = forms.CharField(required=False)
    mood = forms.CharField(required=False)