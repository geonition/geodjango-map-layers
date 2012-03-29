# Create your views here.
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Map
from models import Layer

def map_test(request, map_slug_name = ''):
    map_data = Map.objects.get(slug_name = map_slug_name)
    layer_data = map_data.layers.all()
    return render_to_response('map.html',
                              {'map_data': map_data,
                               'layer_data': layer_data },
                              context_instance = RequestContext(request)) 

def map_js(request, map_slug_name = ''):
    map_data = Map.objects.get(slug_name = map_slug_name)
    layer_data = map_data.layers.all()
    return render_to_response('map.js',
                              {'map_data': map_data,
                               'layer_data': layer_data },
                              mimetype = "application/javascript",
                              context_instance = RequestContext(request)) 

    
