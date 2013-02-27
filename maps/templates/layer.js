gnt.maps = {};

var map = undefined;
gnt.maps.layer = undefined;
gnt.maps.layers = [];
{% if 'Google' in layer_data.protocol %}
gnt.maps.GoogleLoaded = false;
gnt.maps.loadGoogleMaps = function() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "https://maps.googleapis.com/maps/api/js?key={{ layer_data.key }}&sensor=false&callback=gnt.maps.create_google";
  document.body.appendChild(script);
};

gnt.maps.create_google = function() {
    gnt.maps.GoogleLoaded = true;
    gnt.maps.create_map(gnt.maps.map_div, gnt.maps.callback_function);
};
{% endif %}

gnt.maps.create_map = function (map_div, callback_function) {
    {% if 'Google' in layer_data.protocol %}
    if(!gnt.maps.GoogleLoaded) {
        gnt.maps.map_div = map_div;
        gnt.maps.callback_function = callback_function;
        gnt.maps.loadGoogleMaps()
        return;
    }
    {% endif %}
    var mapOptions = {};
    var map_options_created = false;
    var initial_center = [0,0];

    {% if layer_data.protocol == 'OSM-standard' %}
    layer = new OpenLayers.Layer.OSM('OSM-standard');
    gnt.maps.layers.push(layer);
    {% endif %}

    {% if layer_data.protocol == 'Google-satellite' %}
    layer = new OpenLayers.Layer.Google('Satellite', {
                                    type: google.maps.MapTypeId.SATELLITE,
                                    numZoomLevels: 22
                                    });
    gnt.maps.layers.push(layer);
    {% endif %}

    {% if layer_data.protocol == 'Google-hybrid' %}
    layer = new OpenLayers.Layer.Google('Hybrid', {
                                    type: google.maps.MapTypeId.HYBRID,
                                    numZoomLevels: 22
                                    });
    gnt.maps.layers.push(layer);
    {% endif %}
    {% if layer_data.protocol == 'Google-road' %}
    layer = new OpenLayers.Layer.Google('Road', {
                                    type: google.maps.MapTypeId.ROAD
                                    });
    gnt.maps.layers.push(layer);
    {% endif %}
    {% if layer_data.protocol == 'Google-terrain' %}
    layer = new OpenLayers.Layer.Google('Terrain', {
                                    type: google.maps.MapTypeId.TERRAIN
                                    });
    gnt.maps.layers.push(layer);
    {% endif %}
    {% if layer_data.protocol == 'Bing-satellite' %}
    layer = new OpenLayers.Layer.Bing({
                                    name: "Satellite",
                                    type: "AerialWithLabels",
                                    key: "AjB69asvfCy_FaIvDNBzCFc2eJdF7m7_bA7-M-xpJKctrxjmYQjqYX5DRCH0sd3J",
                                    culture: "en"});
    gnt.maps.layers.push(layer);
    {% endif %}

    {% if layer_data.protocol == 'OSM-cyclemap' %}
    layer = new OpenLayers.Layer.OSM('OSM-cyclemap',
        ["http://a.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
        "http://b.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
        "http://c.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png"]);
    gnt.maps.layers.push(layer);
    {% endif %}

    {% if layer_data.protocol == 'OSM-mapquest' %}
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

    {% if layer_data.protocol == 'ArcGISREST' %}
    layer = new OpenLayers.Layer.ArcGIS93Rest(
        "{{ layer_data.name }}",
        "{{ layer_data.source }}",
        {{ layer_data.layer_info|safe }},
        {isBaseLayer: false}
    );
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
