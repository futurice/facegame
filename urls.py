"""urls for the facegame"""
from django.conf.urls.defaults import *
from django.conf import settings
from faceguessing.views import index, updatestats, jsonform, get_user_image
from stats.views import hall_of_fame
from nameguessing.views import nameguessing, get_thumbnail, check_hash, json_thumbnails

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

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
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    # {'document_root': settings.STATIC_ROOT}),

    (r'^admin/', include(admin.site.urls)),
)

# Development settings
# if settings.DEBUG:
#     urlpatterns = patterns('',
#         url(r'^facegame/$', index),
#         url(r'^facegame/updatestats/', updatestats),
#         url(r'^facegame/jsonform/', jsonform),
#         url(r'^facegame/image/current/thumb/', get_thumbnail),
#         url(r'^facegame/image/current/', get_user_image),
#         url(r'^facegame/hall_of_fame$', hall_of_fame),
#         url(r'^facegame/name/updatestats', check_hash),
#         url(r'^facegame/name/', nameguessing),
#         url(r'^facegame/json_thumbnails/', json_thumbnails),

        
#         (r'^facegame/static/(?P<path>.*)$', 'django.views.static.serve',
#             {'document_root': settings.STATIC_ROOT}),
#         #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
#         # {'document_root': settings.STATIC_ROOT}),

#         (r'^admin/', include(admin.site.urls)),
#     )

