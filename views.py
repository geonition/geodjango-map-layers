# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from models import TestProject , LayerDetail 

def base_test(request):

    project = TestProject.on_site.all()[0]
    
    base_layer = LayerDetail.objects.filter( layer_type = 'BL',test_project = project.id ) 
    
    overlay = LayerDetail.objects.filter( layer_type = 'OL',test_project = project.id )
    
    return render_to_response('base_test.html',
                                {'project' : project,
                                 'base_layer' : base_layer,
                                 'overlay' : overlay},
                                context_instance = RequestContext(request))
    
    
