from django.conf.urls import url

from .views import TourGridView, TourDetailView, BookingView, BookingSuccessView
from .webhooks import bitpay_webhook_handler


urlpatterns = [
    url(r'^$', TourGridView.as_view(), name='tours_all'),
    url(r'^(?P<tour_id>\d+)$', TourDetailView.as_view(), name='tour_details'),
    url(r'^(?P<tour_id>\d+)/booking/$', BookingView.as_view(), name='tour_booking'),
    url(r'^(?P<tour_id>\d+)/booking/success/$', BookingSuccessView.as_view(), name='tour_success'),
    url(r'^bitpay/ipn/$', bitpay_webhook_handler, name='bitpay-ipn')
]
