from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe

from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from markdownx.utils import markdownify


class MyCommentManager(TreeManager, CommentManager):
    pass


class MyComment(MPTTModel, CommentAbstractModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('parent comment'))
    follow = models.BooleanField(_('follow up'), default=True)

    objects = MyCommentManager()

    class Meta(CommentAbstractModel.Meta):
        pass

    class MPTTMeta:
        order_insertion_by = ['-submit_date']

    def get_descendants_by_time(self):
        return self.get_descendants().order_by('submit_date')

    @property
    def comment_html(self):
        return mark_safe(markdownify(self.comment))
