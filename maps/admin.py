from django.contrib import admin
from django.utils import simplejson as json
from maps.forms import ArcGISCacheForm
from maps.models import Map
from maps.models import Layer
from maps.models import OpenStreetMapLayer
from maps.models import ArcGISCacheLayer
from urllib2 import urlopen

#class Admin(admin.OSMGeoAdmin):
#    projection = 'EPSG:3067'   
    
admin.site.register(Layer)

class ArcGISCacheLayerAdmin(admin.ModelAdmin):
    fields = ('name', 'source', 'layer_info')
    form = ArcGISCacheForm
    
    def queryset(self, request):
        return self.model.objects.filter(protocol = 'ARCcache')
    
    def save_model(self, request, obj, form, change):
        layer_info = urlopen(form.cleaned_data['source'] + '?f=json').read()
        obj.layer_info = layer_info
        obj.layer_type = 'BL'
        obj.protocol = 'ARCcache'
        obj.save()

admin.site.register(ArcGISCacheLayer, ArcGISCacheLayerAdmin)

class MapAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        
        for layer in form.cleaned_data['layers']:
            print layer
            #check the right projection, tile_size
            if layer.protocol == 'ARCcache':
                li = json.loads(layer.layer_info)
                obj.projection = li['spatialReference']['wkid']
                tile_size = '%s,%s' % (li['tileInfo']['rows'], li['tileInfo']['cols'])
            elif layer.protocol == 'OSM':
                obj.projection = '900913'
        
        obj.save()
    
admin.site.register(Map, MapAdmin)