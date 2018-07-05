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

def serialize_flight_results(old_dict, carriers_meta):
    new_dict = {}
    try:
        new_dict['booking_link'] = old_dict['deep_link']
        new_dict['total_fare'] = old_dict['fare']['total_price']
        new_dict['airline'] = carriers_meta[old_dict['airline']]['name']
        new_dict['travel_class'] = old_dict['travel_class']
        outbound_flight_info = old_dict['outbound']['flights'][0]
        new_dict['arrival_time'] = outbound_flight_info['arrives_at'][-5:]
        new_dict['departure_time'] = outbound_flight_info['departs_at'][-5:]
    except KeyError:
        #todo tigger 404 page but enter production environ first
        raise Exception('Something went wrong')
    return new_dict


def book_flight(request):
    if request.GET.get('origin') is not None:
        form = FlightBookingForm(request.GET)
        if form.is_valid():
            # request.GET does not behave exactly like a dict, so it should not passed around in the application
            flight_form_dict = {}
            for k, v in request.GET.items():
                flight_form_dict[k] = v
            # # todo dont forget to use that empty tag
            flight_results = search_for_flights(settings.AMADEUS_API_KEY, **flight_form_dict)
            carriers_dict = flight_results['meta']['carriers']
            #todo airline nt showing well and errors not showing on front, use the error fiels stuff in template
            data_to_display = [serialize_flight_results(result,carriers_dict) for result in flight_results['results']]
            print(data_to_display)
            return render(request, 'process_flight.html', {'results': data_to_display})
    else:
        form = FlightBookingForm()
    return render(request, 'book_flight.html', {'form': form})
