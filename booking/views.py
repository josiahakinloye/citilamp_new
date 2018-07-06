from django.shortcuts import render
from django.conf import settings

import requests
import logging
from .forms import FlightBookingForm, HotelSearchForm

flight_booking_search = "https://api.sandbox.amadeus.com/v1.2/flights/affiliate-search"

hotel_booking_search = "https://api.sandbox.amadeus.com/v1.2/hotels/search-airport"

# TODO validate date inptiut is not more than today
def search_for_flights(apikey, **kwargs):
        flight_search_paramaters = kwargs
        flight_search_paramaters['apikey'] = apikey
        flight_search_paramaters['currency'] = "USD"  # since US Dollars is the most popular currency
        res = requests.get(flight_booking_search, params=flight_search_paramaters).json()
        return res

def search_for_hotels(apikey, **kwargs):
    hotel_search_parameters = kwargs
    hotel_search_parameters['apikey'] = apikey
    hotel_search_parameters['currency'] = "USD"  # since US Dollars is the most popular currency
    res = requests.get(hotel_booking_search, params=hotel_search_parameters).json()
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
            flights_response = search_for_flights(settings.AMADEUS_API_KEY, **flight_form_dict)
            try:
                carriers_dict = flights_response['meta']['carriers']
                flight_results = flights_response['results']
            except KeyError:
                logging.error('Could not generate results')
                return render(request, 'display_flight_bookings.html', {'results': []})
            #todo airline nt showing well and errors not showing on front, use the error fiels stuff in template
            data_to_display = [serialize_flight_results(result,carriers_dict) for result in flight_results]
            print(data_to_display)
            return render(request, 'display_flight_bookings.html', {'results': data_to_display})
    else:
        form = FlightBookingForm()
    return render(request, 'book_flight.html', {'form': form})


def hotel_search(request):
    if request.GET.get('location') is not None:
        form = HotelSearchForm(request.GET)
        if form.is_valid():
            # request.GET does not behave exactly like a dict, so it should not passed around in the application
            flight_form_dict = {}
            for k, v in request.GET.items():
                flight_form_dict[k] = v
            # # todo dont forget to use that empty tag
            flights_response = search_for_flights(settings.AMADEUS_API_KEY, **flight_form_dict)
            try:
                carriers_dict = flights_response['meta']['carriers']
                flight_results = flights_response['results']
            except KeyError:
                logging.error('Could not generate results')
                return render(request, 'process_flight.html', {'results': []})
            #todo airline nt showing well and errors not showing on front, use the error fiels stuff in template
            data_to_display = [serialize_flight_results(result,carriers_dict) for result in flight_results]
            print(data_to_display)
            return render(request, 'process_flight.html', {'results': data_to_display})
    else:
        form = HotelSearchForm()
    return render(request, 'hotel_search.html', {'form': form})


if __name__ == "__main__":
    data = {'location':'LOS', 'check_in': '2018-07-15', 'check_out':'2018-07-17'}
    print(search_for_hotels(settings.AMADEUS_API_KEY, **data))