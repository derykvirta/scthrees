from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from frontend import views
from frontend import api

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^api/stats', api.stats),
    #url(r'^db', hello.views.db, name='db'),
    #url(r'^admin/', include(admin.site.urls)),
)
