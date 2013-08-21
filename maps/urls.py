from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('maps.views',
    url(r'^map/(?P<map_slug_name>[\w+(+-_)*]+)/$',
        'map_preview',
        name="map_preview"),
    url(r'^layer/(?P<layer_slug_name>[\w+(+-_)*]+)/$',
        'layer_preview',
        name="layer_preview"),
    url(r'^mapjs/(?P<map_slug_name>[\w+(+-_)*]+).js$',
        'map_js',
        name="map_js"),
    url(r'^layerjs/(?P<layer_slug_name>[\w+(+-_)*]+).js$',
        'layer_js',
        name="layer_js"),
    url(r'^maps.json$',
        'maps',
        name="maps"),
        )
