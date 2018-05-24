from django.conf.urls import url

from .views import AboutUsView, OurTeamView, CareersView, TestimonialsView


urlpatterns = [
    url(r'^$', AboutUsView.as_view(), name='about_us'),
    url(r'^team/$', OurTeamView.as_view(), name='our_team'),
    url(r'^careers/$', CareersView.as_view(), name='careers'),
    url(r'^testimonials/$', TestimonialsView.as_view(), name='testimonials'),
]
