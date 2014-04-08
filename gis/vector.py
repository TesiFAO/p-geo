from osgeo import ogr, osr
import os
import os.path

try:
    from utils import filesystem, log
except Exception, e:
    from utils import filesystem, log


def create_shp_from_feature(feat, projection=4326):
    outputFile = filesystem.tmp_filename('shp_', '.shp')

    # TODO: srs get layer
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(projection)

    # create the new shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    outds = driver.CreateDataSource( outputFile )
    outLayer = outds.CreateLayer(outputFile, srs)
    featureDefn = outLayer.GetLayerDefn()
    outFeature = ogr.Feature(featureDefn)

    # geometry of the feature
    geom = feat.GetGeometryRef()
    outFeature.SetGeometry(geom)
    outLayer.CreateFeature(outFeature)

    return outputFile

def create_shapefile_from_json(json_file, projection='EPSG:4326'):
    output_file = filesystem.tmp_filename('shp_', '.shp')
    os.system("ogr2ogr -skipfailures  -t_srs '" + projection + "' " + output_file + " "+ json_file + " OGRGeoJSON")
    return output_file