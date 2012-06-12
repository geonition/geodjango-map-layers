
var map, layer, layers=[], mapOptions;

/*
This function craetes the map and layers.

Additional parameters and layers can be given to the
function.

map_div -- id of the element to create the map into
initial_extent -- initial extent where the map should open
callback_function -- callback function the to be called after creation
    The callback_function will get the map as a parameter
*/
function create_map(map_div, callback_function) {
    var map_options_created = false;
    {% for p in layer_data %}
        {% if p.protocol = 'ARCcache' %}
            var layer_info = {{ p.layer_info|safe }};
            layer = new OpenLayers.Layer.ArcGISCache(
                "{{ p.name }}",
                "{{ p.source }}",
                { layerInfo: layer_info}
            );
            layers.push(layer);
            mapOptions = {
                maxExtent: layer.maxExtent,
                units: layer.units,
                resolutions: layer.resolutions,
                numZoomLevels: layer.lods.length,
                tileSize: layer.tileSize,
                projection: layer.projection,
                restrictedExtent: layer.maxExtent
            };
            map_options_created = true;
        {% else %}
        {% if p.protocol = 'WMTS' %}
            layer = new OpenLayers.Layer.WMTS({
                name: "{{ p.name }}",
                url: "{{ p.source }}",
                layer: "{{ p.layers }}",
                matrixSet: "EPSG:3067",
                format: "image/png",
                style: "_null",
                opacity: 0.7,
                isBaseLayer: false
            });
            layers.push(layer);
        {% else %}
        {% if p.protocol = 'TMS' %}
            layer = new OpenLayers.Layer.TMS(
                "{{ p.name }}", // name for display in LayerSwitcher
                "{{ p.source }}", // service endpoint
                {layername: "{{ p.layers }}", type: "png"} // required properties
            );
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
            layers.push(layer);
        {% else %}
        {% if p.protocol = 'OSM' %}
            layer = new OpenLayers.Layer.OSM(
                '{{ p.name }}'
                );
            layers.push(layer);
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
            layers.push(layer);
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
                    isBaseLayer: true
                    {% else %}
                    isBaseLayer: false
                    {% endif %}
                });
            layers.push(layer);
        {% endif %}
        {% endif %}
        {% endif %}
        {% endif %}
        {% endif %}
        {% endif %}
        {% endif %}
        if(map_options_created == false) {
            mapOptions = {
                projection:"EPSG:{{ map_data.projection }}",
                maxExtent: new OpenLayers.Bounds({{ map_data.max_extent }}),
                maxResolution: {{ map_data.max_resolution }},
                numZoomLevels: {{ map_data.zoom_level }},
                tileSize: new OpenLayers.Size({{ map_data.tile_size }})
            };
        }
    {% endfor %}
    
    //make sure mapOptions controls are set correct
    /*mapOptions.controls = [new OpenLayers.Control.Navigation(),
                           new OpenLayers.Control.Zoom()];*/
    mapOptions.theme = null;
    
    map = new OpenLayers.Map(map_div, mapOptions);
    map.addLayers(layers);

    if(callback_function !== undefined) {
        callback_function(map);
    }
};
