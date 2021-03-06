from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import logout

from kickpassion.engine.views import search, autocomp

admin.autodiscover()


urlpatterns = patterns('django.views.generic.simple',

	url(r'^$', 'direct_to_template', {'template':'home.html'}),

	url(r'^passion/', include('kickpassion.engine.urls')),
	url(r'^facebook/', include('django_facebook.urls')),
	url(r'^accounts/', include('django_facebook.auth_urls')),

    url(r'^logout/$', logout, {'next_page' : '/'}),

    url(r'^search/$', search, name='search service'),
    url(r'^search/autocomplete/$',autocomp, name ="autocomp"),



) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
