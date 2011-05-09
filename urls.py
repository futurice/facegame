from django.conf.urls.defaults import *
from django.conf import settings
from faceguessing.views import index, updatestats, jsonform, get_user_image
from stats.views import hall_of_fame

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('fumapi.urls', namespace='fumapi')),
    url(r'^$', index),
    url(r'^updatestats/', updatestats),
    url(r'^jsonform/', jsonform),
    url(r'^image/current/', get_user_image),
    url(r'^hall_of_fame$', hall_of_fame),

	
    (r'^facegame/static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    # {'document_root': settings.STATIC_ROOT}),

    (r'^admin/', include(admin.site.urls)),
)
