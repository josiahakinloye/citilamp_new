import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template

from paypal.standard.models import ST_PP_COMPLETED

from .models import Tour, TourBooking


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        invoice_tokens = ipn_obj.invoice.split('-')
        if len(invoice_tokens) != 3:
            logging.error('Wrong invoice number')
            return
        user_id = invoice_tokens[0]
        tour_id = invoice_tokens[1]
        if ipn_obj.receiver_email == settings.PAYPAL_BUSINESS_EMAIL:
            try:
                user = User.objects.get(id=user_id)
                tour = Tour.objects.get(id=tour_id)
            except User.DoesNotExist:
                logging.error('Invoice is currupted')
                return
            if tour.get_remaining_seats() > 0:
                TourBooking.objects.create(
                    user=user,
                    tour=tour,
                    ipn_object=ipn_obj
                )
                email_template = get_template('email/booking_success.txt')
                email_context = {'tour': tour, 'total_amount': ipn_obj.mc_gross}
                try:
                    send_mail(
                        'Booking Confirmation - ' + tour.title,
                        email_template.render(email_context),
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False
                    )
                except Exception as ex:
                    logging.error(ex)
            else:
                print("Booking not possible, seats are full.")
        else:
            print('Wrong business email')
    else:
        print('Status is not Complete')
        print(ipn_obj)
