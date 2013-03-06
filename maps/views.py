from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
from django.conf import settings
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
    for layer in layer_data:
        if 'Google' in layer.protocol:
            map_data.google_key = getattr(settings, 'GOOGLE_API_KEY', '')
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
    if 'Google' in layer_data.protocol:
        layer_data.key = getattr(settings, 'GOOGLE_API_KEY', '')
    return render_to_response('layer.js',
                              {'layer_data': layer_data},
                              mimetype = "application/javascript",
                              context_instance = RequestContext(request))


def maps(request):
    """
    This function returns a list of maps in the following format:
    {
        name: <name of map>,
        javascript: <url to javascript file>,
        preview: <url to preview of map>
    }
    """
    maps = []
    for mapobj in Map.objects.all():
        maps.append({
            'name': mapobj.name,
            'javascript': reverse('map_js', kwargs={'map_slug_name': mapobj.slug_name}),
            'preview': reverse('map_preview', kwargs={'map_slug_name': mapobj.slug_name})
        })

    return HttpResponse(json.dumps(maps), mimetype="application/json")





