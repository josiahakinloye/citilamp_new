import requests

flight_booking_search = "https://api.sandbox.amadeus.com/v1.2/flights/affiliate-search"

def search(apikey, origin, destination, departure_date, **kwargs):
    parmaters = kwargs
    parmaters['apikey'] = apikey
    parmaters['origin'] = origin
    parmaters['destination'] = destination
    parmaters['departure_date'] = departure_date
    res = requests.get(flight_booking_search, params=parmaters).json()
    return  res

if __name__ == "__main__":
    other_params = {
        'adults':2
    }
    c = search(apikey="upLiGgUIJEpboZQW5R1yztAPoSNrea5V",
               origin='LON',destination='DUB', departure_date='2018-06-25',)
    print(c)