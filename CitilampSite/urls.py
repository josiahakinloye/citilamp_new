from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from graphene_django.views import GraphQLView

from CitilampSite.schema import schema

urlpatterns = [
    url(r'^graphiql', include('django_graphiql.urls')),
    url(r'^graphql', GraphQLView.as_view(graphiql=True,schema=schema)),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'',include('userprofile.urls')),
    url(r"^account/", include("account.urls")),
    url(r'',include('citilamp.urls')),
    url(r'',include('AdsSystem.urls')),
    url(r'tours/',include('tour.urls')),
    url(r'blog/',include('blog.urls', namespace='blog')),
    url(r"^about/", include("about.urls")),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'CitilampSite.views.custom_404_handler'
