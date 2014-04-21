from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from sormento.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name="home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^add_memento/$', add_memento, name='add_any_memento'),
    url(r'^add_memento/(?P<source>[-\w]+)/$', add_memento, name='add_memento'),
    url(r'^edit_memento/(?P<pk>\d+)/$', edit_memento, name='edit_memento'),
    url(r'^mementos/(?P<pk>\d+)/$', memento_detail, name='memento_detail'),
)

urlpatterns += patterns('',
    # url(r'add_source_type/$', add_source_type, name='add_source_type'),
    url(r'mementos/(?P<pk>\d+)/$', MementoDetail.as_view(), name='memento_detail'),
    # url(r'sources/(?P<root>[-\w]+)/(?P<node>[-\w]+)/$', SourceDetail.as_view(), name='node_detail'),
    url(r'sources/(?P<root_slug>[-\w]+)/$', root_detail, name='root_detail'),
    url(r'sources/(?P<root_slug>[-\w]+)/(?P<source_slug>[-\w]+)/$', source_detail, name='source_detail'),
    url(r'^goto/$', track_url, name='track_url'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)