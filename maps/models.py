from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from urllib2 import urlopen
from django.utils import simplejson as json

class Layer(models.Model):
    LAYER_TYPES = (
        ('BL','Base Layer'),
        ('OL','Overlay'),
    )
    
    PROTOCOLS = (
        ('ArcGISCache','ArcGIS Cache'),
        ('ARCREST','ArcGISRest'),
        ('WFS','WFS - Web Feature Service'),
        ('WMS','WMS - Web Map Service'),
        ('OSM','Open Street Maps'),
        ('WMTS','Web Map Tile Service'),
        ('TMS','Tile Map Service'),
    )
    
    slug_name = models.SlugField(max_length = 50,
                                 primary_key = True,
                                 editable = False)
    name = models.CharField(max_length = 20)
    layer_type = models.CharField(max_length = 5,
                                  choices = LAYER_TYPES)
    protocol = models.CharField(max_length = 20,
                                choices = PROTOCOLS)
    source = models.URLField(blank = True)
    layer_info = models.TextField(editable = True,
                                  blank = True)
    layers = models.CharField(max_length = 300,
                              blank = True)
    
    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(Layer, self).save(*args, **kwargs)
        
        
    def get_absolute_url(self):
        return reverse('layer_preview', kwargs={'layer_slug_name': self.slug_name})
        
    def __unicode__(self):
        return self.name

class Source(models.Model):
    """
    This model represents a source for services.
    
    Supports at the moment ArcGISServer
    """
    SERVICE_TYPES = (
        ('ArcGISServer', 'ArcGISServer'),
    )
    
    service_type = models.CharField(
        max_length = 100,
        choices = SERVICE_TYPES
    )
    source = models.URLField(verify_exists = True)
    
    def save(self, *args, **kwargs):
        
        if self.service_type == 'ArcGISServer':
            
            service_info = json.loads(urlopen(self.source + '?f=json').read())
            print service_info
            #create layers that you can retreive from this source
            
            
            #ArcGIS cache layer
            if service_info['singleFusedMapCache']:
                arcgiscache = Layer(name = service_info['documentInfo']['Title'],
                                    layer_type = 'BL',
                                    protocol = 'ArcGISCache',
                                    source = self.source,
                                    layer_info = json.dumps({
                                        'tileInfo': service_info['tileInfo'],
                                        'fullExtent': service_info['fullExtent'],
                                        'spatialReference': service_info['spatialReference'],
                                        'units': service_info['units'],
                                        'initialExtent': service_info['initialExtent']
                                    }))
                arcgiscache.save()
        
        super(Source, self).save(*args, **kwargs)
        
        
"""
Map which is a collection of layers (that fit together)
"""
class Map(models.Model):
    slug_name = models.SlugField(max_length = 50,
                                 primary_key = True,
                                 editable = False)
    name = models.CharField(max_length = 50)
    projection = models.CharField(max_length = 15,
                                  default = getattr(settings,
                                                    'SPATIAL_REFERENCE_SYSTEM_ID',
                                                    4326))
    max_resolution = models.IntegerField(default = 50,
                                         blank = True,
                                         null = True)
    max_extent = models.CharField(max_length = 750,
                                  blank = True)
    zoom_level = models.IntegerField(default = 10,
                                     blank = True)
    tile_size = models.CharField(max_length = 15,
                                 default = '256,256')
    layers = models.ManyToManyField(Layer)
    
    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(Map, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('map_preview', kwargs={'map_slug_name': self.slug_name})
        
    def __unicode__(self):
        return self.name

