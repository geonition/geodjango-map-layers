
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
    var mapOptions = {};
    var map_options_created = false;
    
    {% for layer in layer_data %}
        
        {% if layer.protocol == 'OSM-standard' %}
        layer = new OpenLayers.Layer.OSM('OSM-standard');
        gnt.maps.layers.push(layer);
        {% endif %}

        {% if layer.protocol == 'Bing-satellite' %}
        layer = new OpenLayers.Layer.Bing({
                                        name: "Satellite",
                                        type: "AerialWithLabels",
                                        key: "AjB69asvfCy_FaIvDNBzCFc2eJdF7m7_bA7-M-xpJKctrxjmYQjqYX5DRCH0sd3J",
                                        culture: "en"});
        gnt.maps.layers.push(layer);
        {% endif %}
        {% if layer.protocol == 'Imagefile' %}
        size = "{{layer.layer_info}}".split(',');
        layer = new OpenLayers.Layer.Image(
                        'Imagemap',
                        "{{ layer.source }}",
                        new OpenLayers.Bounds(0,0,size[0],size[1]),
                        new OpenLayers.Size(size[0], size[1]),
                        {numZoomLevels: 3});
        gnt.maps.layers.push(layer);
        {% endif %}
        
        {% if layer.protocol == 'OSM-cyclemap' %}
        layer = new OpenLayers.Layer.OSM('OSM-cyclemap',
            ["http://a.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
            "http://b.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
            "http://c.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png"]);
        gnt.maps.layers.push(layer);
        {% endif%}
        
        {% if layer.protocol == 'OSM-mapquest' %}
        layer = new OpenLayers.Layer.OSM('OSM-mapquest',
            ["http://otile1.mqcdn.com/tiles/1.0.0/osm/${z}/${x}/${y}.jpg",
             "http://otile2.mqcdn.com/tiles/1.0.0/osm/${z}/${x}/${y}.jpg",
             "http://otile3.mqcdn.com/tiles/1.0.0/osm/${z}/${x}/${y}.jpg",
             "http://otile4.mqcdn.com/tiles/1.0.0/osm/${z}/${x}/${y}.jpg"]);
        gnt.maps.layers.push(layer);
        {% endif %}
    
        {% if layer.protocol == 'OSM-watercolor' %}
        layer = new OpenLayers.Layer.OSM('OSM-watercolor',
            ["http://a.tile.stamen.com/watercolor/${z}/${x}/${y}.jpg",
             "http://b.tile.stamen.com/watercolor/${z}/${x}/${y}.jpg",
             "http://c.tile.stamen.com/watercolor/${z}/${x}/${y}.jpg",
             "http://d.tile.stamen.com/watercolor/${z}/${x}/${y}.jpg"]);
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
        
    
        {% if layer.protocol == 'ArcGISREST' %}
        layer = new OpenLayers.Layer.ArcGIS93Rest(
            "{{ layer.name }}",
            "{{ layer.source }}",
            {{ layer.layer_info|safe }},
            {isBaseLayer: false}        
        );
        gnt.maps.layers.push(layer);
        {% endif %}
        if(map_options_created === false) {
            mapOptions = {
                projection: "EPSG:{{ map_data.projection }}", // is this required?
                matrixSet: "EPSG:{{ map_data.projection }}",
                maxExtent: new OpenLayers.Bounds({{ map_data.max_extent }}),
                units: "m",
                maxResolution: {{ map_data.max_resolution }},
                format: "image/png",
                zoom: {{ map_data.zoom_level }},
                numZoomLevels: 15,
                style : "_null",
                tileSize: new OpenLayers.Size({{ map_data.tile_size }})
            };
        }
        {% if layer.protocol == 'WMTS' %}
        var matrixIds = new Array(16);
            for (var i=0; i<16; ++i) {
                matrixIds[i] = "EPSG:{{ map_data.projection }}:" + i;
        }

        mapOptions.url = "{{ layer.source }}";
        mapOptions.layer = "{{ layer.name }}";
        mapOptions.matrixIds = matrixIds;
        layer = new OpenLayers.Layer.WMTS(mapOptions);
        gnt.maps.layers.push(layer);
        {% endif %}
        {% if layer.protocol == 'WMS' %}
        layer = new OpenLayers.Layer.WMS( "OpenLayers WMS",
                    "{{ layer.source}}",
                    {layers: "{{ layer.name }}"});
        gnt.maps.layers.push(layer);
        {% endif %}
    {% endfor %}
    
    //make sure mapOptions controls are set correct
    mapOptions.controls = [new OpenLayers.Control.Navigation(),
                        new OpenLayers.Control.Attribution(),
                           new OpenLayers.Control.Zoom()];
    
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
