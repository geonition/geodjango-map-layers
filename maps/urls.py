from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

urlpatterns = patterns('maps.views',
    url(r'^map/(?P<map_slug_name>[\w+(+-_)*]+)/$',
        'map_test',
        name="map_test"),
    url(r'^javascript/(?P<map_slug_name>[\w+(+-_)*]+)/$',
        'map_js',
        name="map_js"),    
        
        )
