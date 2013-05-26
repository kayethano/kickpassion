from django.conf.urls import patterns, include, url

urlpatterns = patterns('kickpassion.engine.views',

    url(r'^new/$','passion', name='new passion'),
    url(r'^(?P<passionID>\d+)/$', 'view_passion', name='view passion'),
 
) 