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


def serialize_flight_results(old_flight_dict, carriers_meta):
    new_dict = {}
    try:
        new_dict['booking_link'] = old_flight_dict['deep_link']
        new_dict['total_fare'] = old_flight_dict['fare']['total_price']
        new_dict['airline'] = carriers_meta[old_flight_dict['airline']]['name']
        new_dict['travel_class'] = old_flight_dict['travel_class']
        outbound_flight_info = old_flight_dict['outbound']['flights'][0]
        new_dict['arrival_time'] = outbound_flight_info['arrives_at'][-5:]
        new_dict['departure_time'] = outbound_flight_info['departs_at'][-5:]
    except KeyError:
        #todo tigger 404 page but enter production environ first
        raise Exception('Something went wrong')
    return new_dict

def serialize_hotel_search_result(old_hotel_dict):
    new_hotel_dict = {}
    try:
        new_hotel_dict['hotel_name'] = old_hotel_dict['property_name']
        old_address = old_hotel_dict['address']
        new_hotel_dict['address'] = old_address['line1']+', '+old_address['city']
        new_hotel_dict['amenities'] = serialize_hotel_amentities(old_hotel_dict['amenities'])
        new_hotel_dict['contacts'] = serialize_hotel_contacts(old_hotel_dict['contacts'])
        new_hotel_dict['rooms'] = [serialize_hotel_room(room) for room in old_hotel_dict['rooms']]
    except KeyError:
        logging.warning('Could not determine info for hotels')
    return new_hotel_dict
def serialize_hotel_room(old_room):
    new_room = {}
    try:
        new_room['booking_code'] = old_room['booking_code']
        new_room['price'] = old_room['rates'][0]['price']
        old_room_info = old_room['room_type_info']
        new_room['description'] = old_room_info['room_type'] + ', '+ old_room_info['number_of_beds']+" "+ old_room_info['bed_type']+'bed(s)'
    except KeyError:
        logging.warning('Could not determine info for some rooms')
    return new_room

def serialize_hotel_amentities(old_amenities):
    new_amentities = ""
    if old_amenities:
        for old_amenity in old_amenities:
            new_amentities = new_amentities + ', '+old_amenity['description']
    return new_amentities

def serialize_hotel_contacts(old_contacts):
    new_contacts = ""
    if old_contacts:
        for old_contact in old_contacts:
            new_contacts = new_contacts + ', ' + old_contact['type']+ ": " + old_contact['detail']

    return new_contacts
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
                logging.error('Could not get flight results')
                return render(request, 'display_flight_bookings.html', {'results': []})
            #todo airline nt showing well and errors not showing on front, use the error fiels stuff in template
            data_to_display = [serialize_flight_results(result,carriers_dict) for result in flight_results]
            return render(request, 'display_flight_bookings.html', {'results': data_to_display})
    else:
        form = FlightBookingForm()
    return render(request, 'book_flight.html', {'form': form})


def hotel_search(request):
    if request.GET.get('location') is not None:
        form = HotelSearchForm(request.GET)
        if form.is_valid():
            # request.GET does not behave exactly like a dict, so it should not passed around in the application
            hotel_search_form_dict = {}
            for k, v in request.GET.items():
                hotel_search_form_dict[k] = v
            # # todo dont forget to use that empty tag

            hotel_search_response = search_for_hotels(settings.AMADEUS_API_KEY, **hotel_search_form_dict)
            try:
                hotel_search_results = hotel_search_response['results']
            except KeyError:
                logging.error('Could not get hotel results')
                return render(request, 'display_hotel_search_results.html', {'results': []})
            # data_to_display = [serialize_flight_results(result,carriers_dict) for result in flight_results]
            # print(data_to_display)
            print(hotel_search_response)
            hotels_data_to_display = [serialize_hotel_search_result(hotel) for hotel in hotel_search_results ]
            return render(request, 'display_hotel_search_results.html', {'results': hotels_data_to_display})
    else:
        form = HotelSearchForm()
    return render(request, 'hotel_search.html', {'form': form})


if __name__ == "__main__":
    data = {'location':'LOS', 'check_in': '2018-07-15', 'check_out':'2018-07-17'}
    print(search_for_hotels(settings.AMADEUS_API_KEY, **data))