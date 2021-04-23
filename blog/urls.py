from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<slug>.+)/$',
        views.PostDetailView.as_view(), name="detail"),
    url(r'^category/(?P<slug>.+)/$', views.InCategoryView.as_view(), name='in_category'),
    url(r'^tag/(?P<slug>.+)/$', views.InTagView.as_view(), name='in_tag'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^archive/(?P<year>[0-9]{4})/$', views.PostYearArchiveView.as_view(), name='archive_year'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$', views.PostMonthArchiveView.as_view(),
        name="archive_month"),
    # url(r'^messages/$', views.MessageBoardView.as_view(), name='message_board'),
    # url(r'^messages/(?P<slug>.+)/$', views.AnnouncementDetailView.as_view(), name='announcement'),
    # url(r'^contact/$', views.ContactView.as_view(), name='contact'),
]
