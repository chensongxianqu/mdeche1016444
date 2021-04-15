from django.template import Library
from django.db.models.aggregates import Count

from taggit.models import Tag

from categories.models import Category
from comments.models import MyComment

from ..models import Post

register = Library()


@register.simple_tag
def get_recent_posts(number=5):
    return Post.published.all()[:number]


@register.simple_tag
def get_categories():
    categories = Category.objects.all().annotate(
        num_categories=Count('post')).filter(num_categories__gt=0)
    return categories


@register.simple_tag
def get_tags():
    return Tag.objects.all()


@register.simple_tag
def get_archive():
    return Post.objects.archive()

# @register.inclusion_tag('blog/recent_comments.html')
# def get_recent_comments(number=5):
#     comments = MyComment.objects.all()[:number]
#     return {'recent_comments': comments}
#
#
# @register.inclusion_tag('blog/archive.html')
# def get_archive():
#     dates = Post.objects.datetimes('pub_date', 'month', order='DESC')
#     return {'dates': dates}
