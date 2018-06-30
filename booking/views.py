from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.conf import settings
# Create your views here.
import logging
import requests

from .forms import FlightBookingForm

flight_booking_search = "https://api.sandbox.amadeus.com/v1.2/flights/affiliate-search"


def search_for_flights(apikey, **kwargs):
        parmaters = kwargs
        parmaters['apikey'] = apikey
        print(parmaters)
        res = requests.get(flight_booking_search, params=parmaters).json()
        print(res)
        return  res

def book_flight(request):
    if request.GET.get('origin') is not None:
        form = FlightBookingForm(request.GET)
        if form.is_valid():
            #todo pass to api then get apikey then render content, test if api needs data in string or python datatype,
            # also look up bootstrap cars
            flight_form_dict = {}
            for k,v in request.GET.items():
                flight_form_dict[k] = v
            print(flight_form_dict)
            search_for_flights(settings.AMADEUS_API_KEY, **flight_form_dict)
    else:
        form=FlightBookingForm()
    return render(request, 'book_flight.html', {'form': form})


def process_flight(request):
    print('processing flight')
    return render(request,'process_flight.html', {'post', request})