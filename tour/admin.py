from django.contrib import admin

from .models import Tour, TourProgram, TourPhotos, TourCategory, TourCity, TourBooking, BitpayIPN


class TourProgramInline(admin.TabularInline):
    model = TourProgram


class TourCityInline(admin.TabularInline):
    model = TourCity
    raw_id_fields = ('city',)


class TourPhotosInline(admin.TabularInline):
    model = TourPhotos


class TourAdmin(admin.ModelAdmin):
    inlines = [
        TourProgramInline, TourCityInline, TourPhotosInline
    ]


class TourBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour')
    raw_id_fields = ('user', 'tour', 'bitpay_ipn')


class BitpayIPNAdmin(admin.ModelAdmin):
    list_display = ('bitpay_id', 'status', 'price', 'date_updated', 'date_created')


admin.site.register(Tour, TourAdmin)
admin.site.register(TourCategory)
admin.site.register(TourBooking, TourBookingAdmin)
admin.site.register(BitpayIPN, BitpayIPNAdmin)
