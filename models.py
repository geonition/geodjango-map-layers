from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site

class Layer(models.Model):

    LAYER_TYPES = (
        ('BL','Base Layer'),
        ('OL','Overlay'),
    )
        
    PROTOCOLS = (
        ('ARCACHE','ArcGISCache'),
        ('ARCGIS','ArcGIS93Rest'),
        ('WFS','WFS - Web Feature Service'),
        ('WMS','WMS - Web Map Service'),
        ('OP','OpenLayers Default'),
        ('OSM','Open Street Maps'),
    ) 
    name = models.CharField(max_length = 20)
    type = models.CharField(max_length = 5, choices = LAYER_TYPES)
    protocol = models.CharField(max_length = 10, choices = PROTOCOLS)
    source = models.URLField()
    layers = models.CharField(max_length = 300)
    
    def __unicode__(self):
        return self.layer_name
        

class Map(models.Model):
  
    name = models.CharField(max_length = 50)
    projection = models.CharField(max_length = 15)
    resolution = models.IntegerField()
    max_extent = models.CharField(max_length = 500)
    layers = models.ManyToManyField(Layer)     
    def __unicode__(self):
        return self.name
        
