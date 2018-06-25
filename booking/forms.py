from django import forms

class FlightBookingForm(forms.Form):
    location = forms.CharField(label='Location')
    departure_date = forms.DateField()
    #for round fields
    arrival_date = forms.DateField(required=False)
    # todo put in template that is defulted to 1
    no_of_adults = forms.IntegerField(required=False)
    no_of_children =  forms.IntegerField(required=False)
