from django.contrib import admin

from .models import TeamMember, Testimonial, Career


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'designation', 'is_featured', 'date_created', 'date_updated',)
    search_fields = ('full_name', 'designation',)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'is_approved', 'is_featured', 'date_created', 'date_updated',)
    raw_id_fields = ('user', 'booking',)


class CareerAdmin(admin.ModelAdmin):
    list_display = ('designation', 'positions', 'city', 'is_active', 'date_created', 'date_updated',)
    raw_id_fields = ('city', 'country',)
    search_fields = ('designation',)


admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Career, CareerAdmin)
