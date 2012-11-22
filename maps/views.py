from django.core import serializers
from django.shortcuts import render_to_response
from django.template import RequestContext
from maps.models import Map
from maps.models import Layer

def map_preview(request, map_slug_name = ''):
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

def layer_preview(request, layer_slug_name = ''):
    """
    This view is used for testing the layer
    """
    layer_data = Layer.objects.get(slug_name = layer_slug_name)
    
    return render_to_response('layer.html',
                              {'layer_data': layer_data,
                               'layer_slug': layer_slug_name},
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

def layer_js(request, layer_slug_name = ''):
    """
    This is the javascript that can be used to
    set up the defined map for viewing one layer.
    """
    layer_data = Layer.objects.get(slug_name = layer_slug_name)
    return render_to_response('layer.js',
                              {'layer_data': layer_data},
                              mimetype = "application/javascript",
                              context_instance = RequestContext(request))


    
