from pprint import pprint
from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import FlightBookingForm
# Create your views here.

class FlightBookingView(FormView):
    template_name = 'book_flight.html'
    form_class =  FlightBookingForm
    # success_url = '/thanks'

    def form_valid(self, form):
        pprint(form)
        return super().form_valid(form)