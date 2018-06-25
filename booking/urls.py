from .views import FlightBookingView

from django.conf.urls import url


urlpatterns = [
    url('flight',FlightBookingView.as_view(), name='book_flight'),
    url('hotel', FlightBookingView.as_view(), name='book_hotel')
]