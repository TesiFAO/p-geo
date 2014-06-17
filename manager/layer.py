from geoserver.geoserver import Geoserver
from mongo.geometadata import db

# GeoServer Instance
g = Geoserver()

def publish_layer(layer, path):
    return None

def publish_coveragestore(layer, path, overwrite=False):
    """
    Publish a Raster layer



    layer = {
        "workspace" : "test",
        "layername" : "test",
        "stylename": "raster_modis_ndvi",
        "title" : {
            "EN" : "MODIS"
        },
        "description" : {
            "EN" : "MODIS"
        },
        "code": "MODISQ1",
        "resourceRepresentationType" : "RASTER",
        "coverageTime" : {
            "from" : "2014-01-01",
            "to": "2014-01-31"
        },
        "ReferenceSystem" : {
            "projection" : 4326,
            "projectionName" : "EPSG:4326"
        }
    }

    """
    try:
        # Check if use a User workspace, or the default workspace
        workspace = None
        if ( "workspace" in layer ): workspace = layer["workspace"]
        else: workspace = g.get_default_workspace()

        print "Publishing: ", workspace, ":", layer["layername"]

        # publishing layer on GeoServer Master and GeoServers slaves
        g.publish_coveragestore(layer["layername"], path, workspace, overwrite)

        # publishing the style TODO: this can be done when the layer is published
        g.set_default_style(layer["stylename"], layer["layername"], True)

        # publish layer on geometadata catalog
        layer["uid"] = workspace + ":" + layer["layername"]
        db.insertMetadata(layer)

    except Exception, e:
        print e


def delete_coveragestore(layername, workspace=None):
    try:

        # getting the right workspace
        if ( workspace is None ): workspace = g.get_default_workspace()

        print "Deleting: ", workspace, ":", layername

        # delete layer from GeoServer
        g.delete_coveragestore(layername, workspace);

        #delete layer on geometadata catalog
        db.removeMetadata({"uid" : workspace + ":" + layername})

    except Exception, e:
        print e


def reload_geoservers():
    g.reload_configuration_geoserver_slaves(True);
    return None


#layer example
layer = {
    "workspace" : "test",
    "layername" : "test",
    "stylename": "raster_modis_ndvi",
    "title" : {
        "EN" : "MODIS"
    },
    "description" : {
        "EN" : "MODIS"
    },
    "code": "MODISQ1",
    "resourceRepresentationType" : "RASTER",
    "coverageTime" : {
        "from" : "2014-01-01",
        "to": "2014-01-31"
    },
    "ReferenceSystem" : {
        "projection" : 4326,
        "projectionName" : "EPSG:4326"
    },
    #TODO: It's importatant the NODATA VALUE
    "nodata" :""

}

#publish_coveragestore(layer, '/home/vortex/Desktop/LAYERS/MODIS/AB_NDVI_4326.tif')

#g.set_default_style(layer["stylename"], layer["layername"], enabled=True)

#delete_coveragestore(layer["layername"], layer["workspace"])

# "uid" : "test:test7"

#g.reload_configuration_geoserver_slaves();

reload_geoservers()