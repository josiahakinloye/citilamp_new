from .views import  book_flight, hotel_search

from django.conf.urls import url


urlpatterns = [
    url('flight', book_flight, name='book_flight'),
    url('hotel', hotel_search, name='hotel_search'),
]