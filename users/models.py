# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    ip_joined = models.GenericIPAddressField(_('IP joined'), unpack_ipv4=True, null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(_('last login IP'), unpack_ipv4=True, null=True, blank=True)

    def __str__(self):
        return self.username
