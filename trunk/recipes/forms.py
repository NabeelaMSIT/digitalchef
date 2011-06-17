from django import forms
from tagging import models

class SearchForm(forms.Form):
    ingred1 = forms.ModelChoiceField(queryset=models.objects.all(), empty_label="Select Ingredient")
    ingred2 = forms.ModelChoiceField(queryset=models.objects.all(), empty_label="Select Ingredient")
    ingred3 = forms.ModelChoiceField(queryset=models.objects.all(), empty_label="Select Ingredient")

