
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
    {% for p in layer_data %}
        {% if p.protocol = 'ARCcache' %}
            var layer_info = {{ p.layer_info|safe }};
            layer = new OpenLayers.Layer.ArcGISCache(
                "{{ p.name }}",
                "{{ p.source }}",
                { layerInfo: layer_info}
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
            map_options_created = true;
        {% else %}
        {% if p.protocol = 'WMTS' %}
            var matrixIds = new Array(16);
            for (var i=0; i<16; ++i) {
                matrixIds[i] = "EPSG:{{ map_data.projection }}:" + i;
            }
            layer = new OpenLayers.Layer.WMTS({
                name: "{{ p.name }}",
                url: "{{ p.source }}",
                layer: "{{ p.layers }}",
                matrixSet: "EPSG:{{ map_data.projection }}",
                matrixIds: matrixIds,
                format: "image/png",
                style: "_null",
                attribution: "Map data &copy; MML MTK 05-10/2012, <a href='http://www.maanmittauslaitos.fi/avoindata_lisenssi_versio1_20120501' target='_blank'>Lisenssi</a>",
                opacity: 1,
                /*{% if p.layer_type = 'BL'%}
                    isBaseLayer: true,
                    {% else %}*/
                 //   isBaseLayer: false,
                //{% endif %}*/
               //wrapDateLine: false,
                //visibility: true
            });
            gnt.maps.layers.push(layer);
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
            gnt.maps.layers.push(layer);
        {% else %}
        {% if p.protocol = 'OSM' %}
            layer = new OpenLayers.Layer.OSM();
            gnt.maps.layers.push(layer);
        {% else %}
        {% if p.protocol = 'WMS' %}
            layer = new OpenLayers.Layer.WMS(
                "{{ p.name }}",
                "{{ p.source }}",
                {layers: "{{ p.layers }}"},
                {% if p.layer_type = 'BL'%}
                {isBaseLayer: true}
                {% else %}
                {isBaseLayer: false}
                {% endif %}
                );
            gnt.maps.layers.push(layer);
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
            gnt.maps.layers.push(layer);
        {% endif %}
        {% endif %}
        {% endif %}
        {% endif %}
        {% endif %}
        {% endif %}
        if(map_options_created === false) {
            mapOptions = {
                projection: "EPSG:{{ map_data.projection }}",
                maxExtent: new OpenLayers.Bounds({{ map_data.max_extent }}),
                units: "m",
                maxResolution: {{ map_data.max_resolution }},
                //maxResolution: 19.109257068634033,
                //maxResolution: 156543.0339,
                //minResolution: 2.388657133579254,
                zoom: {{ map_data.zoom_level }},
                numZoomLevels: 15,
                tileSize: new OpenLayers.Size({{ map_data.tile_size }})
            };
        }
    {% endfor %}
    
    //make sure mapOptions controls are set correct
    mapOptions.controls = [new OpenLayers.Control.Navigation(),
                        new OpenLayers.Control.Attribution(),
                           new OpenLayers.Control.Zoom()];
    
    mapOptions['theme'] = null;
    
    map = new OpenLayers.Map(map_div, mapOptions);
    map.addLayers(gnt.maps.layers);

    if(callback_function !== undefined) {
        callback_function(map);
    }
};
