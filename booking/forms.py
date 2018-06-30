from django import forms

class FlightBookingForm(forms.Form):
    location = forms.CharField(label='Location')
    destination = forms.CharField()
    departure_date = forms.DateField(input_formats=['%Y-%m-%d'],widget=forms.TextInput(
        attrs={'placeholder': "24/12/2018"}))
    #for round fields
    arrival_date = forms.DateField(required=False, input_formats=['%d/%m/%Y',],widget=forms.TextInput(
        attrs={'placeholder': "24/12/2018"}))
    # todo put in template that is defulted to 1
    no_of_adults = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'value':1}),min_value=1)
    no_of_children =  forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'value':0}),min_value=0)
