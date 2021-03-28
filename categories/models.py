from django.db import models
from django.db.models.manager import Manager
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import AutoCreatedField
from autoslug import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('parent category'),
                            on_delete=models.SET_NULL)
    name = models.CharField(_('name'), max_length=255, unique=True)
    cover = models.OneToOneField('covers.Cover', verbose_name=_('cover'), blank=True, null=True,
                                 on_delete=models.SET_NULL)
    slug = AutoSlugField(populate_from='name', max_length=255, allow_unicode=True, unique=True)
    description = models.TextField(_('description'), blank=True)
    created = AutoCreatedField(_('created date/time'))

    objects = Manager()
    tree = TreeManager()

    class Meta:
        ordering = ('name', 'created')
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
