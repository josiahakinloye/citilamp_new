from django.contrib import admin

from citilamp.models import (Beach, City, Continent, Country, StateProvince)
from citilamp.models import Contacts, GalleryPhoto

models_to_register = (Beach, Continent, Country, StateProvince)

class CitilampBaseAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class CityAdmin(admin.ModelAdmin):
    search_fields = ('name', 'country__name', 'country__iso_alpha_2_code', 'country__iso_alpha_3_code')


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date_created', 'date_updated',)
    search_fields = ('full_name', 'email',)


class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'date_created', 'date_updated',)
    raw_id_fields = ('city', 'country',)


for model in models_to_register:
    admin.site.register(model, admin_class=CitilampBaseAdmin)

admin.site.register(City, CityAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(GalleryPhoto, GalleryPhotoAdmin)
