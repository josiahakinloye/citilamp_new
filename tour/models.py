import random
from django.contrib.auth.models import User
from django.db import models

from paypal.standard.ipn.models import PayPalIPN

from citilamp.models import City


class TourCategory(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Tour Categories'

    def __str__(self):
        return self.name


class Tour(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    headline = models.TextField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discounted_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    max_seats = models.IntegerField()
    cover_photo = models.ImageField(upload_to='pictures/tours')
    categories = models.ManyToManyField(TourCategory)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Tours'

    def __str__(self):
        return self.title

    def get_cities_list(self):
        return self.tourcity_set.all().values_list('city__name', flat=True)

    def get_showcase(self):
        photos = self.tourphotos_set.all()
        if photos:
            return photos[random.randint(0, len(photos) - 1)].photo.url

    def get_price(self):
        if self.discounted_price > 0.00:
            return self.discounted_price
        else:
            return self.price

    def get_remaining_seats(self):
        bookings = self.tourbooking_set.all()
        total_seats_booked = 0
        for booking in bookings:
            total_seats_booked += booking.seats
        return self.max_seats - total_seats_booked

    def get_tour_days(self):
        return (self.end_date - self.start_date).days + 1


class TourProgram(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tour = models.ForeignKey(Tour)
    day_start = models.IntegerField()
    day_end = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Tour Programs'

    def __str__(self):
        return self.title

class TourPhotos(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tour = models.ForeignKey(Tour)
    photo = models.ImageField(upload_to='pictures/tours')

    class Meta:
        verbose_name_plural = 'Tour Photos'


class TourCity(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tour = models.ForeignKey(Tour)
    city = models.ForeignKey(City)

    class Meta:
        verbose_name_plural = 'Tour Cities'


class BitpayIPN(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    bitpay_id = models.TextField()
    status = models.TextField(default=None, null=True, blank=True)
    price = models.FloatField(default=0.0)
    currency = models.CharField(max_length=3)
    buyer_email = models.EmailField(null=True, blank=True, default=None)
    post_data = models.TextField()


class TourBooking(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tour = models.ForeignKey(Tour)
    user = models.ForeignKey(User)
    seats = models.IntegerField(default=1)
    bitpay_ipn = models.ForeignKey(BitpayIPN, null=True, blank=True, default=None)
