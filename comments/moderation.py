from django import VERSION
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.template import Context, loader
from django.contrib.sites.shortcuts import get_current_site

from django_comments.moderation import CommentModerator as DjangoCommentModerator


class CommentModerator(DjangoCommentModerator):
    email_notification = True

    def email(self, comment, content_object, request):
        if not self.email_notification:
            return
        recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
        if comment.parent:
            recipient_list.extend([comment.parent.email, comment.get_root().email])
        t = loader.get_template('comments/comment_notification_email.txt')
        c = {
            'comment': comment,
            'content_object': content_object,
            'site': get_current_site(request).domain,
            'protocol': 'http'
        }
        subject = _('你在 [%(site)s] 的评论有了新回复') % {
            'site': get_current_site(request).name,
        }
        message = t.render(Context(c) if VERSION < (1, 8) else c)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, set(recipient_list), fail_silently=True)
