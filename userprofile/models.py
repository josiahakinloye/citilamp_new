from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to='users', default='users/account_default.png')
    social_photo_url = models.URLField(null=True, blank=True, default=None)

    def get_photo_url(self):
        if self.social_photo_url:
            return self.social_photo_url
        else:
            return self.photo.url
