from __future__ import unicode_literals

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from .utils import get_read_time
from .utils import unique_slug_generator

User = get_user_model()


class PostQuerySet(models.query.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now()).not_draft()


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        return self.get_queryset().published()


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    read_time = models.IntegerField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = CloudinaryField('image', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    objects = PostManager()

    def __str__(self):
        return self.title + ' by ' + str(self.author)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]


class Comment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    text = models.TextField()
    is_flagged = models.BooleanField(default=False, help_text="Set it true if comment is inapproriate.")

    def __str__(self):
        return self.post.title


#do this before saving an instance of  the model
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    read_time_var = get_read_time(html_string=instance.content)
    instance.read_time = read_time_var
    if instance.image:
        instance.image_url = "http://res.cloudinary.com/{cloud_name}/".format(cloud_name=settings.CLOUDNAME)+str(instance.image)


pre_save.connect(pre_save_post_receiver, sender=Post)
