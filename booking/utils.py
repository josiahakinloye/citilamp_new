import logging
import requests

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
        new_hotel_dict['contacts'] = old_hotel_dict['contacts']
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
    return new_amentities+"."

