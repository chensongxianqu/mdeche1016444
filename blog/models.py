from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.conf import settings

from model_utils import Choices
from model_utils.fields import SplitField, MonitorField
from model_utils.models import TimeStampedModel, StatusModel, TimeFramedModel, SoftDeletableModel
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from markdownx.utils import markdownify
from mptt.models import MPTTModel

from comments.models import MyComment


class Post(StatusModel, TimeStampedModel, TimeFramedModel):
    """
    fields in parent classes:

    'status'
    'status_changed'
    'created'
    'modified'
    'start'
    'end'
    """

    STATUS = Choices(
        ('draft', _('draft')),
        ('published', _('published')),
        ('hidden', _('hidden')),
    )

    title = models.CharField(_('title'), max_length=255)
    body = SplitField(_('body'))
    pub_date = MonitorField(_('published date/time'), monitor='status', when=['published'])
    slug = AutoSlugField(populate_from='title', max_length=255, allow_unicode=True, unique_for_date='pub_date')
    featured = models.BooleanField(_('featured'), default=False)
    views = models.PositiveIntegerField(_('views'), default=0)
    lead = models.TextField(_('lead'), blank=True)
    comment_enabled = models.BooleanField(_('comments enabled'), default=True)

    cover = models.ForeignKey('covers.Cover', verbose_name=_('cover'), blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'))
    category = models.ForeignKey('categories.Category', verbose_name='category')

    tags = TaggableManager(blank=True)
    comments = GenericRelation(MyComment, object_id_field='object_pk', content_type_field='content_type')

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.cover:
        #     if self.category.cover:
        #         self.cover = self.category.cover
        self.cover = self.cover or self.category.cover
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={
            'pk': self.pk,
            'year': self.pub_date.year,
            'month': self.pub_date.month,
            'day': self.pub_date.day,
            'slug': self.slug,
        })

    @property
    def body_html(self):
        return mark_safe(markdownify(self.body.content))

    @property
    def excerpt_html(self):
        return mark_safe(markdownify(self.body.excerpt))

    @property
    def lead_html(self):
        return mark_safe(markdownify(self.lead))

    def root_comments(self):
        return self.comments.filter(parent__isnull=True)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

# class Announcement(TimeStampedModel, TimeFramedModel, SoftDeletableModel):
#     title = models.CharField(_('title'), max_length=255)
#     body = models.TextField(_('body'))
#     slug = AutoSlugField(_('slug'), populate_from='title', unique=True, allow_unicode=True)
#     issuer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='issuer')
#     messages = GenericRelation(MyComment, object_id_field='object_pk', content_type_field='content_type')
#
#     class Meta:
#         verbose_name = _('Announcement')
#         verbose_name_plural = _('Announcements')
#         get_latest_by = 'modified'
#         ordering = ['-modified', 'title']
#
#     def __str__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return reverse('blog:announcement', kwargs={'slug': self.slug})
#
#     def directed_messages(self):
#         return self.messages.filter(parent__isnull=True).order_by('submit_date')
