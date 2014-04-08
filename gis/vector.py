from osgeo import gdal, ogr, osr
import os
import os.path

try:
    from utils import filesystem, log
except Exception, e:
    from utils import filesystem, log

def create_shp_from_feature(feat, projection=4326):
    outputFile = filesystem.create_tmp_file();
    '''
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
    outLayer.CreateFeature(outFeature)     '''

    return outputFile

def createShapefileFromJSON(json_file, projection='EPSG:4326'):
    outputFile =filesystem.create_tmp_file();
    cmd = "ogr2ogr -skipfailures  -t_srs '" + projection + "' " + outputFile + " "+ json_file + " OGRGeoJSON"
    os.system(cmd)
    return outputFile

create_shp_from_feature('')