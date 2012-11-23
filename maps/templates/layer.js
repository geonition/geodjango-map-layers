gnt.maps = {};

var map = undefined;
gnt.maps.layer = undefined;
gnt.maps.layers = [];

gnt.maps.create_map = function (map_div, callback_function) {
    var mapOptions = {};
    var map_options_created = false;
    var initial_center = [0,0];
    
    {% if layer_data.protocol == 'OSM' %}
    layer = new OpenLayers.Layer.OSM();
    gnt.maps.layers.push(layer);
    {% endif %}
    
    {% if layer_data.protocol == 'ArcGISCache' %}
    var layer_info = {{ layer_data.layer_info|safe }}; 
    layer = new OpenLayers.Layer.ArcGISCache(
                "{{ layer_data.name }}",
                "{{ layer_data.source }}",
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
    
    //make sure mapOptions controls are set correct
    mapOptions.controls = [new OpenLayers.Control.Navigation(),
                           new OpenLayers.Control.Zoom(),
                           new OpenLayers.Control.Attribution()];
    
    mapOptions['theme'] = null;
    
    map = new OpenLayers.Map(map_div, mapOptions);
    map.addLayers(gnt.maps.layers);
    map.zoomToMaxExtent();

    if(callback_function !== undefined) {
        callback_function(map);
    }
};