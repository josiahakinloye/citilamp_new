from django.shortcuts import render
from django.conf import settings

import requests

from .forms import FlightBookingForm

flight_booking_search = "https://api.sandbox.amadeus.com/v1.2/flights/affiliate-search"


def search_for_flights(apikey, **kwargs):
        parmaters = kwargs
        parmaters['apikey'] = apikey
        parmaters['currency'] = "USD"  # since US Dollars is the most popular currency
        res = requests.get(flight_booking_search, params=parmaters).json()
        return res


def book_flight(request):
    if request.GET.get('origin') is not None:
        form = FlightBookingForm(request.GET)
        if form.is_valid():
            # todo  look up bootstrap cars
            # request.GET does not behave exactly like a dict, so it should not passed around in the application
            flight_form_dict = {}
            for k, v in request.GET.items():
                flight_form_dict[k] = v
            # todo prepare function that serializes  info, dont forget to use that empty tag
            flight_results = search_for_flights(settings.AMADEUS_API_KEY, **flight_form_dict)
            # return redirect('show_flights_search_results', b=json.dumps(flight_results))
            return render(request, 'process_flight.html', {'results': flight_results})
    else:
        form = FlightBookingForm()
    return render(request, 'book_flight.html', {'form': form})
