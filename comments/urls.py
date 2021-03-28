from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^reply/(?P<pid>[0-9]+)$',
        view=views.CommentReplyView.as_view(),
        name='reply'
    ),
    url(r'^success/$',
        views.CommentSuccess.as_view(),
        name='comment_success'),
]
