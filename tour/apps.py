from django.apps import AppConfig


class TourConfig(AppConfig):
    name = 'tour'

    def ready(self):
        from paypal.standard.ipn.signals import valid_ipn_received
        from .signals import show_me_the_money
        valid_ipn_received.connect(show_me_the_money)
