"""
This module contains everything that has to do with weather
"""
from datetime import datetime
from django.conf import settings
from apixu.client import ApixuClient #weather api

weather_client = ApixuClient(settings.WEATHER_API_KEY)


def get_weather_forecast(city):
    try:
        forecast = weather_client.getForecastWeather(q=city, days=7)['forecast']['forecastday']
        return list(map(get_weather_info, forecast))
    except:
        return None


def get_weather_forecast_comparison(user_city="lagos", explored_city="london", days=7):
    """
    Compares the weather forecast of two cities passed in
    :param user_city: String The city the author in browsing from , this is to be obtained on the front end with the Html
    :param explored_city: String The city the author is exploring ie the city the author is viewing on the website
    :param days: Int Number of days you want to compare weather forecast for
    :return: Zip object containing info of weather comparision
    """
    user_city_forecast = weather_client.getForecastWeather(q=user_city, days=days)['forecast']['forecastday']
    explored_city_forecast = weather_client.getForecastWeather(q=explored_city, days=days)['forecast']['forecastday']
    weather_forecast_comparison = zip(map(get_weather_info, user_city_forecast), map(get_weather_info, explored_city_forecast))
    return weather_forecast_comparison



def get_weather_info(forecast):
    """
    This returns a dictionary of relevant weather info
    :param forecast: List of weather info for a particular day
    :return: Dict of  relevant info to be displayed
    """
    day_forecast = {}
    day_forecast['condition_text'] = forecast['day']['condition']['text']
    #this icon is a url to an image that describes the weather condition
    day_forecast['condition_icon'] = forecast['day']['condition']['icon']
    day_forecast['max_temp'] = forecast['day']['maxtemp_c']
    day_forecast['min_temp'] = forecast['day']['mintemp_c']
    day_forecast['avg_temp'] = forecast['day']['avgtemp_c']
    date = datetime.strptime(forecast['date'], "%Y-%m-%d").strftime("%b %d:%a")
    date_format = date.split(':')
    day_forecast['day'] = date_format[0]
    day_forecast['weekday'] = date_format[1]
    return day_forecast


if __name__ == "__main__":
    weather_comparison = get_weather_forecast_comparison()
    for comparison in weather_comparison:
        print (comparison)
