from django.contrib import admin
from maps.forms import ArcGISCacheForm
from maps.models import Map
from maps.models import Layer
from maps.models import OpenStreetMapLayer
from maps.models import ArcGISCacheLayer
from urllib2 import urlopen

#class Admin(admin.OSMGeoAdmin):
#    projection = 'EPSG:3067'   
    
admin.site.register(Map)
admin.site.register(Layer)

class ArcGISCacheLayerAdmin(admin.ModelAdmin):
    
    form = ArcGISCacheForm
    
    def queryset(self, request):
        return self.model.objects.filter(protocol = 'ARCcache')
    
    def save_model(self, request, obj, form, change):
        layer_info = urlopen(obj.source + '?f=json').read()
        obj.layer_info = layer_info
        obj.save()

admin.site.register(ArcGISCacheLayer, ArcGISCacheLayerAdmin)
