from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DateDetailView, TemplateView, FormView, DetailView
from django.utils.html import mark_safe
from django.core.urlresolvers import reverse

from braces.views import MessageMixin, FormValidMessageMixin
from taggit.models import Tag
from haystack.generic_views import SearchView as HaystackSearchView

from categories.models import Category

from .models import Post
from .forms import ContactForm


class IndexView(ListView):
    paginate_by = 10
    model = Post
    template_name = "blog/index.html"


class PostDetailView(DateDetailView):
    model = Post
    date_field = "pub_date"
    month_format = '%m'
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response


class InCategoryView(MessageMixin, ListView):
    paginate_by = 10
    model = Post
    template_name = "blog/index.html"

    def get_queryset(self):
        c = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        posts = Post.published.filter(category=c)
        self.messages.info(
            mark_safe("分类 <strong>{0}</strong>，{1} 篇文章".format(c.name, posts.count())))
        return posts


class InTagView(MessageMixin, ListView):
    paginate_by = 10
    model = Post
    template_name = "blog/index.html"

    def get_queryset(self):
        t = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        posts = Post.published.filter(tags=t)
        self.messages.info(
            mark_safe("标签 <strong>{0}</strong>，{1} 篇文章".format(t.name, posts.count())))
        return posts


# class MessageBoardView(ListView):
#     model = Announcement
#     template_name = 'blog/messages_board.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs = super(MessageBoardView, self).get_context_data(**kwargs)
#         try:
#             announcement = Announcement.objects.latest()
#         except Announcement.DoesNotExist:
#             announcement = None
#         kwargs.update({'announcement': announcement})
#         return kwargs
#
#
# class AnnouncementDetailView(DetailView):
#     model = Announcement
#     template_name = 'blog/messages_board.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs = super(AnnouncementDetailView, self).get_context_data(**kwargs)
#         announcement_list = Announcement.objects.all()
#         kwargs.update({'announcement_list': announcement_list})
#         return kwargs


class ContactView(FormValidMessageMixin, FormView):
    form_valid_message = 'Thank you for you message'
    form_class = ContactForm
    template_name = 'blog/contact.html'

    def form_valid(self, form):
        form.send()
        return super(ContactView, self).form_valid(form)

    def get_success_url(self):
        self.success_url = reverse('blog:contact')
        return super().get_success_url()


class SearchView(MessageMixin, HaystackSearchView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if self.queryset:
            self.messages.success(
                mark_safe(
                    'There are {0} post found in keyword <strong>{1}</strong>'
                        .format(self.queryset.count(), response.context_data['form'].cleaned_data.get('q'))
                )
            )
        return response
