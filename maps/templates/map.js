var map, layer, layers=[], mapOptions;

/*
This function craetes the map and layers.

Additional parameters and layers can be given to the
function.

map_div -- id of the element to create the map into
callback_function -- callback function the to be called after creation
    The callback_function will get the map as a parameter
*/
function create_map(map_div, callback_function) {
    
    {% for p in layer_data %}
        {% if p.protocol = 'ARCcache' %}
            layer = new OpenLayers.Layer.ArcGISCache(
                "{{ p.name }}",
                "{{ p.source }}",
                { layerInfo: {{ p.layer_info|safe }} },
                {% if p.layer_type = 'BL'%}
                    {isBaseLayer: true}
                {% else %}
                    {isBaseLayer: false}
                {% endif %}
                );
            layers.push(layer);
            mapOptions = {
                maxExtent: layer.fullExtent,
                units: layer.units,
                resolutions: layer.resolutions,
                numZoomLevels: layer.numZoomLevels,
                tileSize: layer.tileSize,
                displayProjection: layer.displayProjection
                };
        {% else %}
        {% if p.protocol = 'ARCGIS' %}
            layer = new OpenLayers.Layer.ArcGIS93Rest(
                "{{ p.name }}",
                "{{ p.source }}",
                {layers: "show:{{ p.layers }}",
                format: "png24",
                transparent: true},
                {% if p.layer_type = 'BL'%}
                    {isBaseLayer: true}
                    {% else %}
                    {isBaseLayer: false}
                {% endif %}
                );
            layers.push(layer)     
        {% else %}
        {% if p.protocol = 'OSM' %}
            layer = new OpenLayers.Layer.OSM(
                '{{ p.name }}'
                );
            layers.push(layer)
        {% else %}
        {% if p.protocol = 'WMS' %}
            layer = new OpenLayers.Layer.WMS(
                "{{ p.layer_name }}",
                "{{ p.source }}",
                {layers: "{{ p.layer }}"},
                {% if p.layer_type = 'BL'%}
                {isBaseLayer: true}
                {% else %}
                {isBaseLayer: false}
                {% endif %}
                );
            layers.push(layer)    
        {% else %}
        {% if p.protocol = 'WFS' %}
            layer = new OpenLayers.Layer.Vector(
                "{{ p.name }}",
                {strategies: [new OpenLayers.Strategy.BBOX()],
                protocol: new OpenLayers.Protocol.WFS({
                    url:  "{{ p.source }}",
                    version: "1.1.0",
                    featureType: "{{ p.layer }}",
                    featureNS: "http://localhost:8080/geoserver/BaseTest",
                    geometryName: "the_geom"
                }),
                    visibility: false,
                    onFeatureInsert: function(event) {
                        count_order(event);
                    },
                    {% if p.layer_type = 'BL'%}
                    {isBaseLayer: true}
                    {% else %}
                    {isBaseLayer: false}
                    {% endif %}
                });
            layers.push(layer)                
        {% endif %}       
        {% endif %}
        {% endif %}   
        {% endif %}
        {% endif %}            
        {% if p.protocol != "ARCcache"%}
            mapOptions = {
                projection:"EPSG:{{ map_data.projection }}",
                maxExtent: new OpenLayers.Bounds(89949.504,
                                                6502687.508,
                                                502203.000,
                                                7137049.802),
                maxResolution: 50,
                numZoomLevels: 10,
                tileSize: new OpenLayers.Size(256, 256)                           
                };
            
        {% endif %}
    {% endfor %}
    map = new OpenLayers.Map(map_div, mapOptions);     
    map.addLayers(layers);
    
    if(callback_function !== undefined) {
        callback_function(map);
    }
}
