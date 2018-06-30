from django import forms

class FlightBookingForm(forms.Form):
    origin = forms.CharField(widget=forms.TextInput(attrs={'value':'LON'}))
    destination = forms.CharField(widget=forms.TextInput(attrs={'value':'DUB'}))
    departure_date = forms.DateField(input_formats=['%Y-%m-%d'],widget=forms.TextInput(
        attrs={'value': "2018-12-24"}))
    #for round trips
    arrival_date = forms.DateField(required=False, input_formats=['%d/%m/%Y',],widget=forms.TextInput(
        attrs={'placeholder': "24/12/2018"}))
    no_of_adults = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'value':1}),min_value=1)
    no_of_children =  forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'value':0}),min_value=0)
