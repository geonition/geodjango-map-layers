from django.contrib import admin
from models import Map,Layer

#class Admin(admin.OSMGeoAdmin):
#    projection = 'EPSG:3067'   
    
admin.site.register(Map)
admin.site.register(Layer)
