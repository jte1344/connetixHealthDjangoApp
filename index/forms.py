from django import forms

# our new form
class LocalDrug(forms.Form):
    location = forms.CharField(required=True)
    medication = forms.CharField(required=True)

class InteractionForm(forms.Form):
    #might have to have user input data all in one string seperating meds by a comma
    medications = forms.CharField(required=True)
