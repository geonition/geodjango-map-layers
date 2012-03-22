from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

urlpatterns = patterns('base_test.views',
    url(r'^(?P<map_slug_name>[\w+(+-_)*]+)/$',
        'base_test',
        name="base_test"))
