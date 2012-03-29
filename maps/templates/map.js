function init() {
    var map, layer, layers=[];
    {% for p in layer_data %}
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
    {% endfor %}    
    var mapOptions = {
        projection:"EPSG:{{ map_data.projection }}",
        maxExtent: new OpenLayers.Bounds(89949.504,
                                         6502687.508,
                                         502203.000,
                                         7137049.802),
        maxResolution: 50,
        numZoomLevels: 10,
        tileSize: new OpenLayers.Size(256, 256)                           
        };
    map = new OpenLayers.Map("Map",mapOptions);     
    map.addLayers(layers);
    map.addControl(new OpenLayers.Control.LayerSwitcher({ascending: true}));
};
