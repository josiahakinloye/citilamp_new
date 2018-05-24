from django.contrib.auth.models import User
from django.db import models

from citilamp.models import City, Country
from tour.models import Tour, TourBooking


class TeamMember(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=60)
    designation = models.CharField(max_length=50)
    summary = models.CharField(max_length=255)
    facebook_url = models.TextField(blank=True)
    twitter_url = models.TextField(blank=True)
    youtube_url = models.TextField(blank=True)
    linkedin_url = models.TextField(blank=True)
    photo = models.ImageField()
    is_featured = models.BooleanField(default=False, help_text='If true, the member will be shown on Homepage.')

    def __str__(self):
        return self.full_name


class Testimonial(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    booking = models.ForeignKey(TourBooking)
    text = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False, help_text='If true, it will be shown on Homepage.')


class Career(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, help_text='If True, it will be shown on Careers page.')
    designation = models.CharField(max_length=50)
    description = models.TextField()
    positions = models.IntegerField(default=1)
    city = models.ForeignKey(City)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.designation
