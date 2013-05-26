from django.conf.urls import patterns, include, url

urlpatterns = patterns('kickpassion.engine.views',

    url(r'^new/$','passion', name='new passion'),
    url(r'^(?P<passionID>\d+)/$', 'view_passion', name='view passion'),
    url(r'^join/(?P<passionID>\d+)/(?P<userID>\d+)/$','join_passion', name='join passion'),
    url(r'^meeting/new/(?P<passionID>\d+)/','create_meeting', name='create meeting'),
    url(r'^meeting/join/(?P<meetingID>\d+)/','join_meeting', name='join_meeting'),
	url(r'^(?P<profileName>\w+)/$', 'view_profile', name='view profile'),
	url(r'^(?P<profileName>\w+)/edit/$', 'edit_profile', name='edit profile'),
) 