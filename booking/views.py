from pprint import pprint
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView

from .forms import FlightBookingForm
# Create your views here.
import logging
import requests

flight_booking_search = "https://api.sandbox.amadeus.com/v1.2/flights/affiliate-search"

def search(apikey, **kwargs):
    if  'origin' and 'destination' and 'departure_date' in  kwargs:
        parmaters = kwargs
        parmaters['apikey'] = apikey
        res = requests.get(flight_booking_search, params=parmaters).json()
        return  res
    else:
        logging.error('Ensure the following parameters origin,'
                      ' destination and departure_date were passed in.')
        raise Exception()

# lastthougths redircet to process flight then pass in form data use stackoverflow post  as guide


def book_flight(request):
    if request.GET.get('location') is not None:
        form = FlightBookingForm(request.GET)
        if form.is_valid():
            #todo pass to api then render content, test if api needs data in string or python datatype,
            #  also look up bootstrap cars
            pass
    else:
        form=FlightBookingForm()


    return render(request, 'book_flight.html', {'form': form})


def process_flight(request):
    print('processing flight')
    return render(request,'process_flight.html', {'post', request})