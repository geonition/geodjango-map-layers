from django.contrib.gis import admin
from models import TestProject,LayerDetail

class GoogleAdmin(admin.GeoModelAdmin):
    '''
    default_lon = 394957.6809345
    default_lat = 6704606.1067195
    wms_url = 'http://108.166.110.152:8080/geoserver/cite/wms'
    wms_layer = 'cite:ilmapiiripositpoint'
    display_srid = True
    '''
    map_template = 'gis/admin/google.html'
    
admin.site.register(TestProject,GoogleAdmin)
admin.site.register(LayerDetail)
