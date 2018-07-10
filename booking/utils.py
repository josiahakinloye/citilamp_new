import logging
import requests

flight_booking_search = "https://api.sandbox.amadeus.com/v1.2/flights/affiliate-search"

hotel_booking_search = "https://api.sandbox.amadeus.com/v1.2/hotels/search-airport"


def search_for_flights(apikey, **kwargs):
    """
    Search for flights using an api
    :param apikey: string defining apikey for the api
    :param kwargs: dict containing some specific options to add to api call
    :return: dict
    """

    flight_search_paramaters = kwargs
    flight_search_paramaters['apikey'] = apikey
    flight_search_paramaters['currency'] = "USD"  # since US Dollars is the most popular currency
    flight_search_response = requests.get(flight_booking_search, params=flight_search_paramaters).json()
    return flight_search_response



def search_for_hotels(apikey, **kwargs):
    """
    Search for hotel using an api
    :param apikey: string defining apikey for the api
    :param kwargs: dict containing some specific options to add to api call
    :return: dict
    """
    hotel_search_parameters = kwargs
    hotel_search_parameters['apikey'] = apikey
    hotel_search_parameters['currency'] = "USD"  # since US Dollars is the most popular currency
    hotel_api_response = requests.get(hotel_booking_search, params=hotel_search_parameters).json()
    return hotel_api_response



def serialize_flight_results(old_flight_dict, carriers_meta):
    """
    Represent data gotten from each flight in the api response
    :param old_flight_dict: dict one element of the list returned by the api response
    :param carriers_meta: dict containing meta information about the carrier of each flight
    :return:  dict
    """
    new_flight_dict = {}
    try:
        new_flight_dict['booking_link'] = old_flight_dict['deep_link']
        new_flight_dict['total_fare'] = old_flight_dict['fare']['total_price']
        new_flight_dict['airline'] = carriers_meta[old_flight_dict['airline']]['name']
        new_flight_dict['travel_class'] = old_flight_dict['travel_class']
        outbound_flight_info = old_flight_dict['outbound']['flights'][0]
        new_flight_dict['arrival_time'] = outbound_flight_info['arrives_at'][-5:]
        new_flight_dict['departure_time'] = outbound_flight_info['departs_at'][-5:]
    except KeyError:
        logging.error('Something went wrong, api provider might have changed some keys.')
    return new_flight_dict



def serialize_hotel_search_result(old_hotel_dict):
    """
    Process each element of the hotel dict gotten from the api call.
    :param old_hotel_dict: dict
    :return: dict
    """
    new_hotel_dict = {}
    try:
        new_hotel_dict['hotel_name'] = old_hotel_dict['property_name']
        old_address = old_hotel_dict['address']
        new_hotel_dict['address'] = old_address['line1']+', '+old_address['city']
        new_hotel_dict['amenities'] = serialize_hotel_amenities(old_hotel_dict['amenities'])
        new_hotel_dict['contacts'] = old_hotel_dict['contacts']
        new_hotel_dict['rooms'] = [serialize_hotel_room(room) for room in old_hotel_dict['rooms']]
    except KeyError:
        logging.warning('Could not determine info for hotels')
    return new_hotel_dict


def serialize_hotel_room(old_room):
    """
    Pick only the relevant information to display from the room
    :param old_room: dict containing info of room
    :return: dict
    """
    new_room = {}
    try:
        new_room['booking_code'] = old_room['booking_code']+''
        new_room['price'] = old_room['rates'][0]['price']
        old_room_info = old_room['room_type_info']
        new_room['description'] = old_room_info['room_type'] + ', '+ old_room_info['number_of_beds']+" "+ old_room_info['bed_type']+'bed(s)'
    except KeyError:
        logging.warning('Could not determine info for some rooms')
    return new_room


def serialize_hotel_amenities(old_amenities):
    """
    Bundle up all amenities into one string.
    :param old_amenities: dict containing amenities of hotel eg. car parking.
    :return: str
    """
    new_amentities = ""
    if old_amenities:
        for old_amenity in old_amenities:
            new_amentities = new_amentities + ', '+old_amenity['description']
        return new_amentities+"."
    else:
        return new_amentities