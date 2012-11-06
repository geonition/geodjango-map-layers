from django.forms import ModelForm
from maps.models import ArcGISCacheLayer

class ArcGISCacheForm(ModelForm):
    
    class Meta:
        model = ArcGISCacheLayer