import json
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import get_template
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import BitpayIPN, Tour, TourBooking

User = get_user_model()


@csrf_exempt
def bitpay_webhook_handler(request):
    try:
        body = json.loads(request.body.decode())
        ipn = BitpayIPN(
            bitpay_id=body['id'],
            status=body['status'],
            price=body['price'],
            currency=body['currency'],
            buyer_email=body['buyerFields']['buyerEmail'],
            post_data=request.body.decode()
        )
        if 'buyerFields' in body:
            if 'buyerEmail' in body['buyerFields']:
                ipn.buyer_email = body['buyerFields']['buyerEmail']
        ipn.save()

        if ipn.status == 'paid':
            invoice_tokens = request.GET['order_id'].split('-')
            if len(invoice_tokens) != 3:
                logging.error('Wrong order id ' + body['orderId'])
                return HttpResponse('Wrong order id', status=500)
            user_id = invoice_tokens[0]
            tour_id = invoice_tokens[1]
            try:
                tour = Tour.objects.get(id=tour_id)
                user = User.objects.get(id=user_id)
            except Exception as ex:
                logging.error(ex)
                return HttpResponse(status=500)
            if tour.get_remaining_seats() > 0:
                TourBooking.objects.create(
                    user=user,
                    tour=tour,
                    bitpay_ipn=ipn
                )
                email_template = get_template('email/booking_success.txt')
                email_context = {'tour': tour, 'total_amount': body['price']}
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
    except Exception as ex:
        logging.error(ex)
        return HttpResponse('Unexpected response received', status=500)
    return HttpResponse('Success')
