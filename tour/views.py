import logging
import requests
import time
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Max, Count, Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView

from bitpay.client import Client
from paypal.standard.forms import PayPalPaymentsForm

from citilamp.models import StateProvince, Country
from CitilampSite.utils.distance import get_distance, get_location_by_ip, get_client_ip
from CitilampSite.utils.exchange import convert_currency
from CitilampSite.utils.timeComparison import time_details_comparison
from CitilampSite.utils.weather import get_weather_forecast
from CitilampSite.tripAdvisor.health import get_traveler_health_advice_for_country
from CitilampSite.tripAdvisor.safety import get_country_safety_stats
from .models import Tour, TourCategory


class TourGridView(TemplateView):
    template_name = 'tours_search.html'

    def get_context_data(self, **kwargs):
        context = super(TourGridView, self).get_context_data(**kwargs)
        categories = TourCategory.objects.all()
        for category in categories:
            category.count = category.tour_set.count()
        max_price = Tour.objects.all().aggregate(Max('price')).get('price__max', 10000)
        if not 'tour_view' in self.request.session:
            self.request.session['tour_view'] = 'list'
        if not 'tour_sort' in self.request.session:
            self.request.session['tour_sort'] = '2'

        # filters
        if self.request.session['tour_sort'] == '2':
            tours = Tour.objects.all().order_by('-date_updated')
        else:
            tours = Tour.objects.all().annotate(total_bookings=Count('tourbooking')).order_by('-total_bookings')
        if len(self.request.GET) > 0:
            if self.request.GET.get('type') == '1':
                destination = self.request.GET.get('destination')
                if destination:
                    states_list = StateProvince.objects.filter(name__icontains=destination)
                    countries_list = Country.objects.filter(name__icontains=destination)
                    tours = tours.filter(
                        Q(tourcity__city__name__icontains=destination) |
                        Q(tourcity__city__stateprovince__in=states_list) |
                        Q(tourcity__city__country__in=countries_list) |
                        Q(tourcity__city__country__iso_alpha_2_code__iexact=destination) |
                        Q(tourcity__city__country__iso_alpha_3_code__iexact=destination)
                    ).distinct()
                arrival = self.request.GET.get('arrival')
                if arrival:
                    tours = tours.filter(start_date__gte=arrival)
                departure = self.request.GET.get('departure')
                if departure:
                    tours = tours.filter(end_date__lte=departure)
            elif self.request.GET.get('type') == '2':
                category_filters = self.request.GET.getlist('category_filters')
                if category_filters:
                    tours = tours.filter(categories__in=category_filters).distinct()
                    context['filters'] = category_filters
                min_price_filter = self.request.GET.get('min_price')
                if min_price_filter:
                    tours = tours.filter(price__gte=min_price_filter)
                max_price_filter = self.request.GET.get('max_price')
                if max_price_filter:
                    tours = tours.filter(price__lte=max_price_filter)
                    context['max_price_filter'] = max_price_filter

        paginator = Paginator(tours, 15)
        page = self.request.GET.get('page', 1)
        try:
            tours_list = paginator.page(page)
        except PageNotAnInteger:
            tours_list = paginator.page(1)
        except EmptyPage:
            tours_list = paginator.page(paginator.num_pages)

        context.update({
            'tours': tours_list,
            'categories': categories,
            'max_price': max_price
        })
        return context

    def post(self, request):

        view_type = request.POST.get('view_type')
        if view_type == 'grid':
            request.session['tour_view'] = 'grid'
        elif view_type == 'list':
            request.session['tour_view'] = 'list'

        tour_sort = request.POST.get('tour_sort')
        if tour_sort == '2':
            self.request.session['tour_sort'] = '2'
        elif tour_sort == '3':
            self.request.session['tour_sort'] = '3'

        return HttpResponseRedirect('/tours/')


class TourDetailView(TemplateView):
    template_name = 'tour_details.html'

    def get_context_data(self, **kwargs):
        tour_id = kwargs.get('tour_id')
        if not tour_id:
            raise Http404
        try:
            tour = Tour.objects.get(id=tour_id)
        except:
            raise Http404
        context = super(TourDetailView, self).get_context_data(**kwargs)
        context['tour'] = tour
        context['programs'] = tour.tourprogram_set.all()
        context['photos'] = tour.tourphotos_set.all()
        city = tour.tourcity_set.first()
        if city:
            # get distance
            user_ip = get_client_ip(self.request)
            if user_ip == '127.0.0.1':
                user_ip = '39.45.244.96'
            location = {}
            try:
                location = get_location_by_ip(user_ip)
                if 'lat_lng' in location:
                    user_lat_lng = location['lat_lng']
                    dest_lat_lng = "{},{}".format(city.city.latitude, city.city.longitude)
                    context['distance'] = get_distance(user_lat_lng, dest_lat_lng)
            except Exception as ex:
                logging.error(ex)

            # get currency information
            if 'country_code' in location:
                try:
                    country = Country.objects.get(iso_alpha_2_code__iexact=location['country_code'])
                    current_rate = convert_currency(country.currency_code, city.city.country.currency_code, 1)
                    context['current_rate'] = current_rate
                    context['user_currency_code'] = country.currency_code
                    context['dest_currency_code'] = city.city.country.currency_code
                except Exception as ex:
                    print(ex)

            # get time diffrence
            if 'city' in location:
                try:
                    user_city = location['city']
                    dest_city = city.city.name
                    comparison = time_details_comparison([user_city, dest_city])
                    context['user_time'] = ', '.join(comparison[0][user_city])
                    context['dest_time'] = ', '.join(comparison[1][dest_city])
                except Exception as ex:
                    logging.error(ex)

            # get weather forcast
            weather_forcast = get_weather_forecast(city.city.name)
            if weather_forcast:
                context['weather_forcast'] = weather_forcast

            # get health advice
            try:
                health_advices = get_traveler_health_advice_for_country(city.city.country.name)
            except Exception as ex:
                health_advices = None
                logging.error(ex)
            context['health_advices'] = health_advices

            try:
                safety = get_country_safety_stats(city.city.country.name)
            except Exception as ex:
                logging.error(ex)
                safety = None
            context['safety'] = safety
        return context


class BookingView(LoginRequiredMixin, TemplateView):
    template_name = 'booking.html'

    def get_context_data(self, **kwargs):
        tour_id = kwargs.get('tour_id')
        if not tour_id:
            raise Http404
        try:
            tour = Tour.objects.get(id=tour_id)
            if tour.get_remaining_seats() == 0:
                raise Http404
        except:
            raise Http404

        context = super(BookingView, self).get_context_data(**kwargs)
        context['tour'] = tour
        return context

    def post(self, request, **kwargs):
        tour_id = self.kwargs.get('tour_id')
        try:
            tour = Tour.objects.get(id=tour_id)
            if tour.get_remaining_seats() == 0:
                raise Http404
        except:
            raise Http404
        if hasattr(settings, 'NGROK_URL'):
            ipn_url = settings.NGROK_URL + reverse('bitpay-ipn')
        else:
            ipn_url = self.request.build_absolute_uri(reverse('bitpay-ipn'))
        try:
            f = open(settings.BITPAY_API_KEY_FILE, 'r')
            pem = f.read()
        except Exception as ex:
            logging.error(ex)
            return HttpResponse(status=500)
        if settings.BITPAY_TEST is True:
            client = Client('https://test.bitpay.com', False, pem, tokens={'merchant': settings.BITPAY_API_TOKEN})
        else:
            client = Client('https://bitpay.com', False, pem, tokens={'merchant': settings.BITPAY_API_TOKEN})
        order_id = "{}-{}-{}".format(self.request.user.id, tour.id, int(time.time()))
        bitpay_invoice_payload = {
            "price": str(tour.get_price()),
            "currency": "USD",
            "transactionSpeed": "medium",
            "fullNotifications": "true",
            "notificationURL": ipn_url + '?order_id=' + order_id,
            "redirectURL": self.request.build_absolute_uri(reverse('tour_success', kwargs={'tour_id': tour_id})),
            "orderId": order_id,
            "token": client.tokens['merchant']
        }
        if self.request.user.email:
            bitpay_invoice_payload['buyer'] = {
                'email': self.request.user.email
            }
        try:
            response = client.create_invoice(bitpay_invoice_payload)
            return HttpResponseRedirect(response['url'])
        except Exception as ex:
            logging.error(ex)
            return HttpResponse(status=500)

    # Paypal payment
    def paypal_payment(self, request, **kwargs):
        tour_id = self.kwargs.get('tour_id')
        try:
            tour = Tour.objects.get(id=tour_id)
            if tour.get_remaining_seats() == 0:
                raise Http404
        except:
            raise Http404
        if hasattr(settings, 'NGROK_URL'):
            notify_url = settings.NGROK_URL + reverse('paypal-ipn')
        else:
            notify_url = self.request.build_absolute_uri(reverse('paypal-ipn'))
        paypal_dict = {
            "business": settings.PAYPAL_BUSINESS_EMAIL,
            "amount": tour.get_price(),
            "item_name": tour.title,
            "invoice": "{}-{}-{}".format(self.request.user.id, tour.id, int(time.time())),
            "notify_url": notify_url,
            "return": self.request.build_absolute_uri(reverse('tour_success', kwargs={'tour_id': tour_id})),
            "cancel_return": self.request.build_absolute_uri(reverse('tour_details', kwargs={'tour_id': tour_id})),
            "cmd": "_xclick",
            "charset": "utf-8",
            "currency_code": "USD",
            "no_shipping": "1",
        }
        response = requests.post("https://www.sandbox.paypal.com/cgi-bin/webscr", paypal_dict)
        return HttpResponseRedirect(response.url)


class BookingSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'booking_success.html'

    def get_context_data(self, **kwargs):
        tour_id = kwargs.get('tour_id')
        if not tour_id:
            raise Http404
        try:
            tour = Tour.objects.get(id=tour_id)
        except:
            raise Http404
        context = super(BookingSuccessView, self).get_context_data(**kwargs)
        context['tour'] = tour
        return context
