from django.conf.urls.defaults import *
from django.conf import settings
from faceguessing.views import index, updatestats, jsonform

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('fumapi.urls', namespace='fumapi')),
    url(r'^$', index),
    url(r'^updatestats/', updatestats),
    url(r'^jsonform/', jsonform),
	
	(r'^facegame/static/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': settings.STATIC_ROOT}),
	#(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
	#	{'document_root': settings.STATIC_ROOT}),


    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
