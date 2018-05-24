from social_django.models import UserSocialAuth

def check_social_user(request):
    context = {'is_social_user': False}
    if request.user.is_authenticated():
        try:
            UserSocialAuth.objects.get(user=request.user)
            context['is_social_user'] = True
        except UserSocialAuth.DoesNotExist:
            pass
    return context
