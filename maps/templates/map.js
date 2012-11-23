
/*
 Maps namespace
 
 gnt.maps
*/
gnt.maps = {};


var map = undefined;
gnt.maps.layer = undefined;
gnt.maps.layers = [];


/*
This function creates the map and layers.

Additional parameters and layers can be given to the
function.

map_div -- id of the element to create the map into
initial_extent -- initial extent where the map should open
callback_function -- callback function the to be called after creation
    The callback_function will get the map as a parameter
*/
gnt.maps.create_map = function (map_div, callback_function) {
    var mapOptions;
    var map_options_created = false;
    
    {% for layer in layer_data %}
    
        {% if layer.protocol == 'OSM' %}
        layer = new OpenLayers.Layer.OSM();
        gnt.maps.layers.push(layer);
        {% endif %}
        
        {% if layer.protocol == 'ArcGISCache' %}
        var layer_info = {{ layer.layer_info|safe }}; 
        layer = new OpenLayers.Layer.ArcGISCache(
                    "{{ layer.name }}",
                    "{{ layer.source }}",
                    {
                    layerInfo: layer_info,
                    attribution: layer_info.copyrightText
                    }
                );
        gnt.maps.layers.push(layer);
        
        mapOptions = {
            maxExtent: layer.maxExtent,
            units: layer.units,
            resolutions: layer.resolutions,
            numZoomLevels: layer.lods.length,
            tileSize: layer.tileSize,
            projection: layer.projection,
            restrictedExtent: layer.maxExtent
        };
        {% endif %}
    {% endfor %}
    
    //make sure mapOptions controls are set correct
    mapOptions.controls = [new OpenLayers.Control.Navigation(),
                           new OpenLayers.Control.Zoom(),
                           new OpenLayers.Control.Attribution()];
    
    {% if layer_data|length > 1 %}
    mapOptions.controls.push(new OpenLayers.Control.LayerSwitcher())
    {% endif %}
    
    mapOptions['theme'] = null;
    
    map = new OpenLayers.Map(map_div, mapOptions);
    map.addLayers(gnt.maps.layers);
    map.zoomToMaxExtent();

    if(callback_function !== undefined) {
        callback_function(map);
    }
};
