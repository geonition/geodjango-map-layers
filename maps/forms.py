from django.core.exceptions import ValidationError
from django.forms import Field
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField
from django.utils import simplejson as json
from django.utils import translation
from maps.models import Layer
from maps.models import Map

_ = translation.ugettext

class LayerField(ModelMultipleChoiceField):

    def clean(self, value):
        #check that wkid, tileSize (rows, cols), Resolutions (lods) for ArcGISCache layers match
        wkid = None
        rows = None
        cols = None
        lods = None
        
        arcgiscachelayers = Layer.objects.filter(slug_name__in=value, protocol='ArcGISCache')
        for layer in arcgiscachelayers:
            info = json.loads(layer.layer_info)
            if wkid == None:
                wkid = info['spatialReference']['wkid']
                rows = info['tileInfo']['rows']
                cols = info['tileInfo']['cols']
                lods = info['tileInfo']['lods']
            else:
                if wkid != info['spatialReference']['wkid']:
                    raise ValidationError(_(u'The coordinate reference system has to be the same for all ArcCache layers in a map'))
                elif rows != info['tileInfo']['rows'] or cols != info['tileInfo']['cols']:
                    raise ValidationError(_(u'The tile size of each ArcGIS cached layer has to be same for one map'))
                elif lods != info['tileInfo']['lods']:
                    raise ValidationError(_(u'The level of detail has to be the same for all ArcGIS cache layers for one map'))
        
        super(LayerField, self).clean(value)
        return value
            
class MapForm(ModelForm):
    
    layers = LayerField(queryset=Layer.objects.all())
    
    class Meta:
        model = Map