from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

from account.compat import is_authenticated
from account.forms import LoginEmailForm
from account.views import SignupView, LoginView, LogoutView, ChangePasswordView

from about.models import Testimonial
from tour.models import TourBooking
from .forms import SignupForm, UpdateProfileForm, FeedbackForm
from .models import Profile


class CustomSignupView(SignupView):
    form_class = SignupForm

    def generate_username(self, form):
        return form.cleaned_data.get('email')

    def after_signup(self, form):
        Profile.objects.create(user=self.created_user)
        return super(CustomSignupView, self).after_signup(form)


class CustomLoginView(LoginView):
    form_class = LoginEmailForm


class CustomLogoutView(LogoutView):
    def get(self, *args, **kwargs):
        if is_authenticated(self.request.user):
            auth.logout(self.request)
        return redirect(self.get_redirect_url())


class AccountDetails(LoginRequiredMixin, TemplateView):
    template_name = 'account/details.html'


class UpdateProfileView(LoginRequiredMixin, FormView):
    form_class = UpdateProfileForm
    template_name = 'account/update.html'

    def get(self, request, *args, **kwargs):
        self.initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        }
        return super(UpdateProfileView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        photo = form.cleaned_data['photo']
        if photo:
            try:
                profile = self.request.user.profile
            except:
                profile = Profile(user=self.request.user)
            profile.photo = photo
            profile.save()
        return redirect(reverse('account_details'))


class CustomChangePasswordView(ChangePasswordView):
    def get_success_url(self, fallback_url=None, **kwargs):
        return super(CustomChangePasswordView, self).get_success_url(reverse('account_details'))


class MyBookingsView(LoginRequiredMixin, TemplateView):
    template_name = 'bookings.html'

    def get_context_data(self, **kwargs):
        context = super(MyBookingsView, self).get_context_data(**kwargs)
        bookings = TourBooking.objects.filter(user=self.request.user).order_by("-date_updated")
        for booking in bookings:
            if Testimonial.objects.filter(booking=booking, user=self.request.user).count():
                booking.is_feedback_submitted = True
            else:
                booking.is_feedback_submitted = False
        context['bookings'] = bookings
        return context


class FeedbackView(LoginRequiredMixin, FormView):
    template_name = 'feedback_form.html'
    form_class = FeedbackForm

    def get_context_data(self, **kwargs):
        context = super(FeedbackView, self).get_context_data(**kwargs)
        try:
            booking = TourBooking.objects.get(id=self.kwargs.get('booking_id'), user=self.request.user)
            if Testimonial.objects.filter(booking=booking, user=self.request.user).count():
                raise Http404
        except TourBooking.DoesNotExist:
            raise Http404
        context['booking'] = booking
        return context

    def post(self, request, *args, **kwargs):
        try:
            self.booking = TourBooking.objects.get(id=self.kwargs.get('booking_id'), user=request.user)
        except TourBooking.DoesNotExist:
            raise Http404
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        Testimonial.objects.create(
            user=self.request.user,
            booking=self.booking,
            text=form.cleaned_data['message']
        )
        return redirect(reverse('account_bookings'))
