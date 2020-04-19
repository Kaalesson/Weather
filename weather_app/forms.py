from django import forms


class Cityform(forms.Form):
    city_name = forms.CharField(label="Населённый пункт", max_length=100)