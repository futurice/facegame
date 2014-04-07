from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.template import add_to_builtins
from django.contrib import admin
admin.autodiscover()

from faceguessing.views import index, updatestats, jsonform, get_user_image
from stats.views import hall_of_fame
from nameguessing.views import nameguessing, get_thumbnail, check_hash, json_thumbnails

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^updatestats/', updatestats),
    url(r'^jsonform/', jsonform),
    url(r'^image/current/thumb/', get_thumbnail),
    url(r'^image/current/', get_user_image),
    url(r'^hall_of_fame$', hall_of_fame),
    url(r'^name/updatestats', check_hash),
    url(r'^name/', nameguessing),
    url(r'^json_thumbnails/', json_thumbnails),

	
    (r'^facegame/static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

    (r'^admin/', include(admin.site.urls)),
)
