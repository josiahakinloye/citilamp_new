from userprofile.models import Profile


def save_profile(backend, user, response, *args, **kwargs):
        try:
            profile = user.profile
        except:
            profile = Profile(user_id=user.id)
        image_url = None
        print(response)
        if backend.name == 'twitter':
            image_url = response.get('profile_image_url_https', '').replace('_normal','')
        elif backend.name == 'facebook':
            fb_id = response.get('id')
            if fb_id:
                image_url = 'https://graph.facebook.com/{}/picture?height=300&width=300'.format(fb_id)
        elif backend.name == 'google-oauth2':
            try:
                image_url = response['image']['url'].replace('sz=50', 'sz=300')
            except:
                pass
        if image_url:
            profile.social_photo_url = image_url
        profile.save()
