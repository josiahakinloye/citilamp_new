from django.conf.urls import url

from .views import PostListView, PostDetailView, PostCommentView

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/comment/$', PostCommentView.as_view(), name='comment'),
]
