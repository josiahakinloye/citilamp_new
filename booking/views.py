from pprint import pprint
from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import FlightBookingForm
# Create your views here.
import requests

flight_booking_search = "https://api.sandbox.amadeus.com/v1.2/flights/affiliate-search"

def search(apikey, origin, destination, departure_date, **kwargs):
    parmaters = kwargs
    parmaters['apikey'] = apikey
    parmaters['origin'] = origin
    parmaters['destination'] = destination
    parmaters['departure_date'] = departure_date
    res = requests.get(flight_booking_search, params=parmaters).json()
    return  res


class FlightBookingView(FormView):
    template_name = 'book_flight.html'
    form_class =  FlightBookingForm
    #redirect to a template
    # success_url = '/'

    def form_valid(self, form):
        print("form got submitted")
        self.location = form.cleaned_data['location']
        self.departure_date = form.cleaned_data['departure_date']
        # for round fields
        self.arrival_date = form.cleaned_data['arrival_date']
        # todo put in template that is defulted to 1
        self.no_of_adults = form.cleaned_data['no_of_adults']
        self.no_of_children = form.cleaned_data['no_of_children']
        return super().form_valid(form)

    def get_success_url(self, form):
        #lastthoughts how can data be passed from form to another view in django
        pass

