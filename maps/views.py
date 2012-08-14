from django.shortcuts import render_to_response
from django.template import RequestContext
from maps.models import Map

def map_test(request, map_slug_name = ''):
    """
    This view is used for testing the map, and viewing the
    layers.
    """
    map_data = Map.objects.get(slug_name = map_slug_name)
    layer_data = map_data.layers.all()
    return render_to_response('map.html',
                              {'map_data': map_data,
                               'layer_data': layer_data,
                               'map_slug': map_slug_name},
                              context_instance = RequestContext(request)) 

def map_js(request, map_slug_name = ''):
    """
    This is the javascript that can be used to
    set up the defined map.
    """
    map_data = Map.objects.get(slug_name = map_slug_name)
    layer_data = map_data.layers.all()
    return render_to_response('map.js',
                              {'map_data': map_data,
                               'layer_data': layer_data },
                              mimetype = "application/javascript",
                              context_instance = RequestContext(request))
    
