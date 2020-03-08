from django import forms

# our new form
class UserForm(forms.Form):
    location = forms.CharField(required=True)
    medication = forms.CharField(required=True)
