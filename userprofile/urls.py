from django.conf.urls import url

from .views import CustomSignupView, CustomLoginView, CustomLogoutView, AccountDetails, UpdateProfileView, CustomChangePasswordView, MyBookingsView, FeedbackView


urlpatterns = [
    url(r'^account/signup/$', CustomSignupView.as_view(), name='custom_signup'),
    url(r'^account/login/$', CustomLoginView.as_view(), name='custom_login'),
    url(r'^account/logout/$', CustomLogoutView.as_view(), name='custom_logout'),
    url(r'^account/details/$', AccountDetails.as_view(), name='account_details'),
    url(r'^account/update/$', UpdateProfileView.as_view(), name='account_update'),
    url(r'^account/password/$', CustomChangePasswordView.as_view(), name='custom_account_password'),
    url(r'^account/bookings/$', MyBookingsView.as_view(), name='account_bookings'),
    url(r'^account/booking/(?P<booking_id>\d+)/feedback/$', FeedbackView.as_view(), name='booking_feedback'),
]
