from django.shortcuts import render
from django.conf import settings

import logging

from .forms import FlightBookingForm, HotelSearchForm
from .utils import search_for_flights, search_for_hotels, serialize_flight_results, serialize_hotel_search_result

def book_flight(request):
    if request.GET.get('origin') is not None:
        form = FlightBookingForm(request.GET)
        if form.is_valid():
            # request.GET does not behave exactly like a dict, so it should not passed around in the application
            flight_form_dict = {}
            for k, v in request.GET.items():
                flight_form_dict[k] = v
            # # todo dont forget to use that empty tag
            print(flight_form_dict)
            flights_response = search_for_flights(settings.AMADEUS_API_KEY, **flight_form_dict)
            print(flights_response)
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

