import datetime
import manager_layer as l

#layer example
date = datetime.datetime(2014, 1, 30);
layer = {
    "workspace" : "modis",
    "layername" : "MOD13Q1_A2014033_3857",
    "stylename": "raster_style_modis",
    "title" : {
        "EN" : "MODIS 250m - 2014-01-30"
    },
    "description" : {
        "EN" : "MODIS"
    },
    "code": "MODISQ1",
    "resourceRepresentationType" : "RASTER",
    "coverageTime" : {
        "from" : date,
        "to": date,
        },
    "ReferenceSystem" : {
        "projection" : 4326,
        "projectionName" : "EPSG:4326"
    },
    #TODO: It's importatant the NODATA VALUE
    "nodata" :""

}

print layer

#delete_coveragestore(layer["layername"], layer["workspace"])
print l.publish_coveragestore(layer, '/home/vortex/Desktop/LAYERS/MODIS/033/AB_NDVI_3857.tif')
print l.g.set_default_style(layer["stylename"], layer["layername"], enabled=True)

#delete_coveragestore(layer["layername"], layer["workspace"])

# "uid" : "test:test7"

#g.reload_configuration_geoserver_slaves();

#reload_geoservers()
