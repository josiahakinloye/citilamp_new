from .views import  book_flight

from django.conf.urls import url


urlpatterns = [
    url('flight', book_flight, name='book_flight'),
    url('hotel', book_flight, name='book_hotel'),
]