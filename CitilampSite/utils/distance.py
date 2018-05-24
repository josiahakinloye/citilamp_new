"""
This module contains every thing that has to deal with distance
"""
import googlemaps
import json
import requests
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location_by_ip(ip):
    url = 'http://api.ipstack.com/{}?access_key={}&format=1'.format(ip, settings.IPSTACK_API_KEY)
    response = requests.get(url).content
    location = json.loads(response.decode())
    try:
        data = {}
        data['lat_lng'] = "{},{}".format(location['latitude'], location['longitude'])
        data['country_code'] = location['country_code']
        data['city'] = location['city']
    except KeyError:
        raise Exception("Error while reading the response of IPStack API response")
    return data


def get_distance(origin, destination):
    """
    Get the distance from origin to destination

    :param origin: One location and/or latitude/longitude values,
        from which to calculate distance.
    :type origin: a single location

    :param destination: One address or lat/lng values, to
        which to calculate distance.
    :type destination: a single location

    :return: dict containing distance details
    """
    result = gmaps.distance_matrix(origin, destination)
    try:
        distance_details = result['rows'][0]['elements'][0]['distance']
    except Exception as ex:
        print(ex)
        raise Exception("Could not get distance details, were origin and destination of the same type ie where they both cities or countries")
    return  distance_details

if __name__ =="__main__":
    print (get_distance('nigeria','germany'))