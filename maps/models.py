from django.db import models
from django.conf import settings
from django.utils import translation
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from urllib2 import urlopen
from django.utils import simplejson as json
from PIL import Image
from cStringIO import StringIO
#from lxml import etree as ET
from xml.etree import ElementTree as ET
import urllib2

_ = translation.ugettext

class Layer(models.Model):
    LAYER_TYPES = (
        ('BL','Base Layer'),
        ('OL','Overlay'),
    )

    PROTOCOLS = (
        ('ArcGISCache','ArcGIS Cache'),
        ('ArcGISREST','ArcGISRest'),
        ('Bing-satellite','Bing satellite'),
        ('Imagefile','Imagefile'),
        ('WMTS','WMTS'),
        ('WMS','WMS'),
        ('OSM-standard', 'OSM standard'),
        ('OSM-cyclemap', 'OSM cyclemap'),
        ('OSM-watercolor', 'OSM watercolor'),
        ('OSM-mapquest', 'OSM mapquest'),
        ('Google-satellite', 'Google satellite'),
        ('Google-hybrid', 'Google hybrid'),
        ('Google-road', 'Google road'),
        ('Google-terrain', 'Google terrain'),
    )

    slug_name = models.SlugField(max_length = 100,
                                 primary_key = True,
                                 editable = False)
    name = models.CharField(max_length = 100)
    layer_type = models.CharField(max_length = 5,
                                  choices = LAYER_TYPES,
                                  help_text = _('Use base layer for basemaps. There can be only one visible base layer. Overlays are drawn over the basemap, there can be a multiple overlay layers.'))
    protocol = models.CharField(max_length = 20,
                                choices = PROTOCOLS)
    source = models.URLField(blank = True)
    layer_info = models.TextField(editable = True,
                                  blank = True)
    layers = models.CharField(max_length = 300,
                              blank = True)
    
    #For layer attribution
    attr_title = models.CharField(max_length = 100,
                                  blank = True,default = '',
                                  verbose_name = _('attribution text')
                                  )
    attr_url = models.URLField(blank = True,default = '',
                               verbose_name = _('attribution link')
                               )
    attr_logo_url = models.URLField(blank = True,default = '',
                                    verbose_name = _('logo URL')
                                    )
    attr_logo_format = models.CharField(max_length = 30,
                                        blank = True,default = '',
                                        verbose_name = _('logo content type')
                                        )
    attr_logo_height = models.IntegerField(null = True,
                                           blank = True,
                                           verbose_name = _('logo image width')
                                           )
    attr_logo_width = models.IntegerField(null = True,
                                          blank = True,
                                          verbose_name = _('logo image height')
                                          )

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name).replace('_', '-') #undescores are a problem in admin view on site
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
        ('Bing-satellite','Bing satellite'),
        ('Imagefile','Imagefile'),
        ('WMTS','WMTS'),
        ('WMS','WMS'),
        ('OSM-standard', 'OpenStreetMap standard'),
        ('OSM-cyclemap', 'OpenStreetMap cyclemap'),
        ('OSM-watercolor', 'OpenStreetMap Stamen watercolor'),
        ('OSM-mapquest', 'OpenStreetMap mapquest'),
        ('Google-satellite', 'Google satellite'),
        ('Google-hybrid', 'Google hybrid'),
        ('Google-road', 'Google road'),
        ('Google-terrain', 'Google terrain'),
    )

    service_type = models.CharField(
        max_length = 100,
        choices = SERVICE_TYPES
    )
    source = models.URLField(blank = True,
                             help_text = _('For ArcGIS Servers give as source the service url that end with /rest/services. \nFor OSM services leave this field blank.\n For Imagefile, add the full url to the image.\n For WMTS services the url should end with service/wmts.'))

    def parse_wmts_services(self, url):
#        parser = ET.XMLParser(ns_clean=True)
        urls = [u.strip() for u in url.split(',')]
        resp = urllib2.urlopen(urls[0] + '?REQUEST=GetCapabilities')
        info = ET.parse(resp).getroot()
        urls = ['\"'+u+'\"' for u in urls]
        layernames = []
        #python 2.6 does not have iter method
        try:
            for elem in info.iter('{http://www.opengis.net/ows/1.1}Title'):
                layernames.append(elem.text)
        except AttributeError:
            for elem in info.getiterator('{http://www.opengis.net/ows/1.1}Title'):
                layernames.append(elem.text)

        for layername in layernames:
            layer, created = Layer.objects.get_or_create(
                        name = layername,
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'WMTS',
                            'source': '[' + ', '.join(urls) + ']',
                            'layer_info': '',
                            'layers': ''
                        })

    def parse_wms_services(self, url):
        # example url input: http://wms1.map.mapita.fi/knummi/wms,http://wms2.map.mapita.fi/knummi/wms
        # spaces are not allowed in a URLField
#        parser = ET.XMLParser(ns_clean=True)
        urls = [u.strip() for u in url.split(',')]
        #resp = urllib2.urlopen(urls[0] + '?service=WMS&version=1.1.0&request=GetCapabilities')
        resp = urllib2.urlopen(urls[0] + '?REQUEST=GetCapabilities')
        
        info = ET.parse(resp).getroot()
        urls = ['\"'+u+'\"' for u in urls]
        layernames = []
        for elem in info.findall('./Capability/Layer/Layer/Name'):
            layernames.append(elem.text) #not all of these are useful layers

        for layername in layernames:
            layer, created = Layer.objects.get_or_create(
                        name = layername,
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'WMS',
                            'source': '[' + ', '.join(urls) + ']',
                            'layer_info': '',
                            'layers': ''
                        })



    def parse_arcgis_services(self, url, folder=''):
        """
        This function parses arcGIS services from the given url
        and creates the layers found.
        """
        info = json.loads(urlopen('%s%s%s' % (url, folder, '?f=json')).read())
        services = info['services']

        for service in services:

            #parse the services provided and add to layers
            if service['type'] == 'MapServer':

                #MapServers
                mapurl = '%s/%s/MapServer?f=json' % (url, service['name'])

                mapserver_info = json.loads(urlopen(mapurl).read())
                if mapserver_info.has_key('error'):
                    continue

                #ArcGIS cache layer
                if mapserver_info['singleFusedMapCache']:
                    layer, created = Layer.objects.get_or_create(
                        name = "EPSG:%s-arcgiscache-%s-%s" % (mapserver_info['spatialReference']['wkid'],
                                                         service['name'],
                                                         mapserver_info['documentInfo']['Title']),
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'ArcGISCache',
                            'source': '%s/%s/MapServer' % (url, service['name']),
                            'layer_info': json.dumps({
                                'tileInfo': mapserver_info['tileInfo'],
                                'fullExtent': mapserver_info['fullExtent'],
                                'spatialReference': mapserver_info['spatialReference'],
                                'units': mapserver_info['units'],
                                'initialExtent': mapserver_info['initialExtent'],
                                'copyrightText': mapserver_info['copyrightText']
                            })
                        })

                    if not created:
                        layer.layer_type = 'BL'
                        layer.protocol = 'ArcGISCache'
                        layer.source = '%s/%s/MapServer' % (url, service['name'])
                        layer.layer_info = json.dumps({
                                'tileInfo': mapserver_info['tileInfo'],
                                'fullExtent': mapserver_info['fullExtent'],
                                'spatialReference': mapserver_info['spatialReference'],
                                'units': mapserver_info['units'],
                                'initialExtent': mapserver_info['initialExtent'],
                                'copyrightText': mapserver_info['copyrightText']
                            })
                        layer.save()

                #create one ArcGISRest layer from the service
                available_layers = [str(al['id']) for al in mapserver_info['layers']]
                img_format = "png"

                layer, created = Layer.objects.get_or_create(
                    name = "EPSG:%s-arcgisrest-%s-%s" % (mapserver_info['spatialReference']['wkid'],
                                                     service['name'],
                                                     mapserver_info['documentInfo']['Title']),
                    defaults = {
                        'layer_type': 'OL',
                        'protocol': 'ArcGISREST',
                        'source': '%s/%s/MapServer/export' % (url, service['name']),
                        'layer_info': json.dumps({
                            'layers': "show:%s" % ','.join(available_layers),
                            'format': img_format,
                            'transparent': True
                        })
                    })

                if not created:
                    layer.layer_type = 'OL'
                    layer.protocol = 'ArcGISREST'
                    layer.source = '%s/%s/MapServer/export' % (url, service['name'])
                    layer.layer_info = json.dumps({
                            'layers': "show:%s" % ','.join(available_layers),
                            'format': img_format,
                            'transparent': True
                        })
                    layer.save()

        #for all folders found do parsing again
        folders = info['folders']
        for folder in folders:
            self.parse_arcgis_services(url, folder='/%s' % folder)

    def save(self, *args, **kwargs):

        if self.service_type == 'ArcGISServer':

            self.parse_arcgis_services(self.source)

        elif self.service_type == 'WMTS':

            self.parse_wmts_services(self.source)

        elif self.service_type == 'WMS':

            self.parse_wms_services(self.source)

        elif self.service_type == 'OSM-standard':
            # create layers for OpenStreetMap styles

            #osm standard
            layer, created = Layer.objects.get_or_create(
                        name = "osm-standard",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'OSM-standard',
                            'source': '',
                            'layer_info': '',
                            'layers': ''
                        })

        elif self.service_type == 'OSM-cyclemap':
            # create layers for OpenStreetMap styles

            #osm standard
            layer, created = Layer.objects.get_or_create(
                        name = "osm-cyclemap",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'OSM-cyclemap',
                            'source': '',
                            'layer_info': '',
                            'layers': ''
                        })


        elif self.service_type == 'OSM-mapquest':
            # create layers for OpenStreetMap styles

            #osm standard
            layer, created = Layer.objects.get_or_create(
                        name = "osm-mapquest",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'OSM-mapquest',
                            'source': '',
                            'layer_info': '',
                            'layers': ''
                        })

        elif self.service_type == 'OSM-watercolor':
            # create layers for OpenStreetMap styles

            #osm standard
            layer, created = Layer.objects.get_or_create(
                        name = "osm-watercolor",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'OSM-watercolor',
                            'source': '',
                            'layer_info': '',
                            'layers': ''
                        })

        elif self.service_type == 'Bing-satellite':
            layer, created = Layer.objects.get_or_create(
                        name = "bing-satellite",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'Bing-satellite',
                            'source': '',
                            'layer_info': '',
                            'layers': ''
                        })

        elif self.service_type == 'Imagefile':
            img_file = urlopen(self.source)
            im = StringIO(img_file.read())
            width, height = Image.open(im).size
            w, h = str(width), str(height)
            #json_info = '{ "bounds" : "[ 0,0,'+w+','+h+']", "size" : "'+w+','+h+'" ]}'
            layer, created = Layer.objects.get_or_create(
                        name = "image",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'Imagefile',
                            'source': self.source,
                            'layer_info': w+','+h,
                            'layers': ''
                        })

        elif self.service_type == 'Google-satellite':
            layer, created = Layer.objects.get_or_create(
                        name = "google-satellite",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'Google-satellite',
                            'source': '',
                            'layer_info': '',
                            'layers': ''
                        })

        elif self.service_type == 'Google-hybrid':
            layer, created = Layer.objects.get_or_create(
                        name = "google-hybrid",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'Google-hybrid',
                            'source': '',
                            'layer_info': '',
                            'layers': ''
                        })

        elif self.service_type == 'Google-road':
            layer, created = Layer.objects.get_or_create(
                        name = "google-road",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'Google-road',
                            'source': '',
                            'layer_info': '',
                            'layers': ''
                        })

        elif self.service_type == 'Google-terrain':
            layer, created = Layer.objects.get_or_create(
                        name = "google-terrain",
                        defaults = {
                            'layer_type': 'BL',
                            'protocol': 'Google-terrain',
                            'source': '',
                            'layer_info': '',
                            'layers': ''
                        })

        super(Source, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s' % (self.service_type, self.source)



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
    max_resolution = models.FloatField(default = 50.0,
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

