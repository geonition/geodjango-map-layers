from django.contrib import admin
from django.utils import simplejson as json
from maps.models import Map
from maps.models import Layer
from maps.models import Source
from urllib2 import urlopen

#class Admin(admin.OSMGeoAdmin):
#    projection = 'EPSG:3067'   


admin.site.register(Source)
admin.site.register(Layer)

class MapAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        
        for layer in form.cleaned_data['layers']:
            #check the right projection, tile_size
            if layer.protocol == 'ARCcache':
                li = json.loads(layer.layer_info)
                obj.projection = li['spatialReference']['wkid']
                tile_size = '%s,%s' % (li['tileInfo']['rows'], li['tileInfo']['cols'])
            elif layer.protocol == 'OSM':
                obj.projection = '900913'
        
        obj.save()
    
admin.site.register(Map, MapAdmin)