from django.http import HttpResponse
from django.views.generic import TemplateView, FormView

from about.models import Testimonial
from CitilampSite.utils.news import get_headline_news
from CitilampSite.tripAdvisor.safety import prepare_recent_disaster_table
from tour.models import Tour
from .forms import ContactUsForm
from .models import GalleryPhoto






class HomePageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_approved=True, is_featured=True)
        context['tours'] = Tour.objects.filter(is_active=True, is_featured=True)
        context['news'] = list(get_headline_news())
        context['recent_disasters'] = prepare_recent_disaster_table()
        return context


class GalleryView(TemplateView):
    template_name = 'gallery.html'

    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)
        context['photos'] = GalleryPhoto.objects.all().order_by("-date_updated")
        return context


class ContactUsView(FormView):
    template_name = 'contact.html'
    form_class = ContactUsForm

    def form_valid(self, form):
        form.save()
        return HttpResponse("MF000")
