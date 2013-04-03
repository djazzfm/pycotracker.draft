from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
)


if settings.ROOT_URLCONF == 'pycotracker.urls':
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )
