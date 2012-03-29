from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

urlpatterns = patterns('base_test.views',
    url(r'^map/(?P<map_slug_name>[\w+(+-_)*]+)/$',
        'base_test',
        name="base_test"),
    url(r'^javascript/(?P<map_slug_name>[\w+(+-_)*]+)/$',
        'base_js',
        name="base_js"),    
        
        )
