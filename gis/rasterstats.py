from osgeo import gdal, ogr
import os
import sys
import json
import vector
import struct
import subprocess
import glob
import numpy

try:
    from utils import filesystem, log
except Exception, e:
    sys.path.append('../')
    from utils import filesystem, log

try:
    from geoserver import postgis_utils
except Exception, e:
    sys.path.append('../')
    from geoserver import postgis_utils


logger = log.Logger()

# TODO: use force with min max and GetHistogram.
# TODO: loop over the available bands to make an array
def get_histogram( input_raster, force=False, buckets=256, include_out_of_range=0 ):

    ds = gdal.Open( input_raster )

    # pass the band selection
    band = 1

    # force the calculation of min max and of the histogram?
    # get min and max values (force the recalculation?)
    if (force == True ):
        (min, max)= ds.GetRasterBand(band).ComputeRasterMinMax(0)
    else:
        min = ds.GetRasterBand(band).GetMinimum()
        max = ds.GetRasterBand(band).GetMaximum()

    histogram = ds.GetRasterBand(band).GetHistogram( buckets=buckets, min=min, max=max, include_out_of_range = include_out_of_range )
    #return json.dumps({"buckets":buckets,"min":min,"max":max,"values":histogram}, )
    return {"buckets":buckets,"min":min,"max":max,"values":histogram}

def get_raster_statistics(input_raster, force=True):
    src_ds = gdal.Open(input_raster)
    stats = []
    for band in range(src_ds.RasterCount):
        band += 1
        srcband = src_ds.GetRasterBand(band)
        if srcband is None:
            continue

        '''if force:
            s = srcband.ComputeStatistics(0)
        else:
            s = srcband.GetStatistics(False, force)
        '''
        s = srcband.GetStatistics(False, force)
        if stats is None:
            continue
        stats.append({"min":s[0],"max":s[1],"mean":s[2],"stddev":s[3]})
    return stats

def get_zonalstatics_by_json(input_raster, json, force=True):
    print json
    print '-------------  '
    json_file = filesystem.create_tmp_file(json, 'json_', '.json')
    shp_file = vector.create_shapefile_from_json(json_file)
    shp = ogr.Open(shp_file)
    lyr = shp.GetLayer()
    stats = []
    # loop through the features in the layer
    feature = lyr.GetNextFeature()
    #print feature
    i = 0
    while feature:
        # create a tmp shapefile
        feature_shp_file = vector.create_shp_from_feature(feature)
        # create a tmp raster
        raster_file = crop_raster_by_vector(input_raster, feature_shp_file )
        # do statistics on the new raster
        stat = get_raster_statistics(raster_file, force)
        # calculate histogram
        hist = get_histogram(raster_file, force)
        stats.append({"fid":i,"stat": stat,"hist": hist})
        # check next feature
        feature = lyr.GetNextFeature()
        i+=1
    return stats


def crop_raster_by_vector(input_raster, input_polygon):
    output_file =  filesystem.tmp_filename('output_', '.tif')
    # crop layer by vector (using gdalwarp)
    # TODO: handle nodata
    #cmd = "gdalwarp -multi -of GTiff -cutline "+ input_polygon +" -crop_to_cutline " + input_raster + " " + outputfile + " -srcnodata 32767 -dstnodata 32767"
    # how to get the dstnodata value?
    # TODO: get the srs source file!!!
    cmd = "gdalwarp -q -multi -dstnodata 0 -of GTiff -cutline "+ input_polygon +" -crop_to_cutline " + input_raster + " " + output_file
    os.system(cmd)
    return output_file

def crop_raster_by_vector_postgis(input_raster, table, query=None, s_srs='EPSG:4326', t_srs='EPSG:4326', datastore=None, srsnodata=None, dstnodata='nodata'):
    #gdalwarp -cutline "PG:dbname=fenixspatial user=fenix password=Qwaszx" -csql 'select * from g2008_4326 where adm0_code=1' -crop_to_cutline -of GTiff -s_srs EPSG:4326 -t_srs EPSG:4326 3B42RT.2014012000.7.1day.tif 3B42RT.2014012000.7.1day_cut.ti
    output_file =  filesystem.tmp_filename('output_', '.tif')
    # get db connectin string from configfile (geoserver.json default datastore?)
    # TODO:handle connection to db
    db_connection_string = "PG:dbname=fenixspatial user=fenix password=Qwaszx"
    # TODO:handle nodata
    cmd = 'gdalwarp -q -multi -of GTiff -cutline "'+ db_connection_string +'" -csql "'+ query +'" -s_srs '+ s_srs + ' -t_srs '+ t_srs +' -crop_to_cutline ' + input_raster + ' ' + output_file
    logger.info('crop_raster_by_vector_postgis: ' + cmd)
    os.system(cmd)
    return output_file

def get_raster_statistics(input_raster, force=True):
    src_ds = gdal.Open(input_raster)
    stats = []
    for band in range(src_ds.RasterCount):
        band += 1
        srcband = src_ds.GetRasterBand(band)
        if srcband is None:
            continue

        '''if force:
            s = srcband.ComputeStatistics(0)
        else:
            s = srcband.GetStatistics(False, force)
        '''
        s = srcband.GetStatistics(False, force)
        if stats is None:
            continue
        stats.append({"min":s[0], "max":s[1], "mean":s[2], "stddev":s[3]})
    return stats

def cell_rasters_value(rasters, x, y, band=None):
    values = []
    for raster in rasters:
        values.append(cell_raster_value(raster, x, y, band))
    print values
    return values

def cell_raster_value(raster, x, y, band=None):
    #gdallocationinfo -valonly  3B42RT.2014030100.7.1day.tif -geoloc 7.57001 2.2323
    # TODO: check with -wgs84 values instad of -geoloc that is the reference system of the image
    # gdallocationinfo NGA_DEM_30.tif -l_srs EPSG:4326 4 1
    cmd = "gdallocationinfo -valonly " + raster + " -geoloc " + str(x) + " " + str(y)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.strip()
    #return { raster : output.strip() }

# def test():
#     #tiffs = glob.glob("/home/vortex/programs/layers/raster/TRMM/3B42RT/2014/03/original/*.tif")
#     # tiffs = glob.glob("/home/vortex/programs/layers/raster/RASTER/Vegetation/NDVI/*.tif")
#     #tiffs = glob.glob("/home/vortex/programs/layers/raster/TRMM/3B42RT/2014/03/original/geotiff/*.tif")
#     tiffs = glob.glob("/home/vortex/Desktop/TRMM/3B42RT/all/*.tif")
#     #tiff = ["/home/vortex/programs/layers/raster/RASTER/Terrain/DEM_30/NGA_DEM_30.tif"]
#     return cell_rasters_value(tiffs,7.42029131585, 9.86668319136)
#     #return cell_rasters_value(tiffs, 807554.158945, 1003293.38818)
#
# #test()
#
# a = crop_raster_by_vector_postgis('/home/vortex/Desktop/TRMM/3B42RT/2014/04/original/3B42RT.2014042000.7.1day.tif', 'g2008_4326', "select * from g2008_4326 where adm0_name='Italy'")
# print a
