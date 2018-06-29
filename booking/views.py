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
    # if this is a POST request we need to process the form data
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = FlightBookingForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         # return redirect('process_flight_booking', form=form)
    #         print(form.location)
    #         print('\n')
    #         print(form.cleaned_data)
    # # if a GET (or any other method) we'll create a blank form
    # #todo submit form via get request check if dta has been filled

    if request.GET.get('location') is not None:
        form = FlightBookingForm(request.GET)
        if form.is_valid():
            pass
    else:
        form=FlightBookingForm()


    return render(request, 'book_flight.html', {'form': form})


def process_flight(request):
    print('processing flight')
    return render(request,'process_flight.html', {'post', request})