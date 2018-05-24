from django.conf.urls import url

from .views import HomePageView, GalleryView, ContactUsView


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^gallery/$', GalleryView.as_view(), name='gallery'),
    url(r'^contacts/$', ContactUsView.as_view(), name='contacts')
]
