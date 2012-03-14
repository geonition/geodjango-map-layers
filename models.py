from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site

class TestProject(models.Model):
  
    name = models.CharField(max_length = 50)
    area = geomodels.PolygonField()
    site = models.ForeignKey(Site)
    on_site = CurrentSiteManager()
    
    def __unicode__(self):
        return self.name

class LayerDetail(models.Model):

    LAYER_TYPES = (
        ('BL','Base Layer'),
        ('OL','Overlay'),
    )
        
    PROTOCOLS = (
        ('ARCGIS','ArcGIS93Rest'),
        ('WFS','WFS - Web Feature Service'),
        ('WMS','WMS - Web Map Service'),
        ('OP','OpenLayers Default'),
        ('OSM','Open Street Maps'),
    ) 
    layer_name = models.CharField(max_length = 20)
    layer_type = models.CharField(max_length = 5, choices = LAYER_TYPES)
    protocol = models.CharField(max_length = 10, choices = PROTOCOLS)
    source = models.URLField()
    layer = models.CharField(max_length = 300)
    test_project = models.ForeignKey(TestProject)
