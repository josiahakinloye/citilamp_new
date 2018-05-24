from django.views.generic import TemplateView

from .models import TeamMember, Career, Testimonial


class AboutUsView(TemplateView):
    template_name = 'about.html'


class OurTeamView(TemplateView):
    template_name = 'team.html'

    def get_context_data(self, **kwargs):
        context = super(OurTeamView, self).get_context_data(**kwargs)
        context['members'] = TeamMember.objects.all()
        return context


class CareersView(TemplateView):
    template_name = 'careers.html'

    def get_context_data(self, **kwargs):
        context = super(CareersView, self).get_context_data(**kwargs)
        context['jobs'] = Career.objects.filter(is_active=True)
        return context


class TestimonialsView(TemplateView):
    template_name = 'testimonials.html'

    def get_context_data(self, **kwargs):
        context = super(TestimonialsView, self).get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_approved=True).order_by("-date_updated")
        return context
