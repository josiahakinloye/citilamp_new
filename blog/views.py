from urllib.parse import quote_plus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, FormView

from .forms import PostCommentForm
from .models import Post, Comment


def searched_posts(parameter_to_query_with):
    """
    Returns searched posts querying with the parameter passed in
    :param parameter_to_query_with:
    :return:
    """
    return Post.objects.active().filter(
        Q(title__icontains=parameter_to_query_with) |
        Q(content__icontains=parameter_to_query_with) |
        Q(author__first_name__icontains=parameter_to_query_with) |
        Q(author__last_name__icontains=parameter_to_query_with)
    ).distinct()


class PostListView(TemplateView):
    template_name = 'blog_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        queryset_list = Post.objects.active().order_by("-timestamp")
        query = self.request.GET.get("q")
        if query:
            queryset_list = searched_posts(query)
        paginator = Paginator(queryset_list, 12)
        page = self.request.GET.get("page", 1)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)
        context['queryset'] = queryset
        return context


class PostDetailView(DetailView):
    template_name = 'blog_details.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        instance = get_object_or_404(Post, slug=slug)
        return instance

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        instance = context['object']
        context['comments'] = instance.comment_set.all()
        context['share_string'] = quote_plus(instance.content)
        return context


class PostCommentView(LoginRequiredMixin, FormView):
    form_class = PostCommentForm

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404
        Comment.objects.create(
            post=post,
            user=self.request.user,
            text=form.cleaned_data['comment']
        )
        return redirect(reverse("blog:detail", kwargs={'slug':slug}))
