from osgeo import gdal, ogr
import os
import sys
import json
import vector

try:
    from utils import filesystem
except Exception, e:
    sys.path.append('../')
    from utils import filesystem

def get_histogram( input_value_raster, force=False, buckets=256, include_out_of_range=0 ):

    ds = gdal.Open( input_value_raster )
    print input_value_raster

    # pass the band selection
    band = 1

    # force the calculation of min max and of the histogram?
    # get min and max values (force the recalculation?)
    min = ds.GetRasterBand(band).GetMinimum()
    max = ds.GetRasterBand(band).GetMaximum()

    histogram = ds.GetRasterBand(band).GetHistogram( buckets=buckets, min=min, max=max, include_out_of_range = include_out_of_range )
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
        stats.append({"min":s[0], "max":s[1], "mean":s[2], "stddev":s[3]})
    return stats

def get_zonalstatics_by_json(input_raster, json):
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
        stat = get_raster_statistics(raster_file)
        # calculate histogram
        hist = get_histogram(raster_file)
        stats.append({"fid": i, "stat": stat, "hist": hist})
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
    cmd = "gdalwarp -q -multi -dstnodata 0 -of GTiff -cutline "+ input_polygon +" -crop_to_cutline " + input_raster + " " + output_file
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

'''
json = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[6.85546875,45.13555516012536],[7.778320312499999,45.935870621190546],[12.3486328125,46.73986059969267],[13.38134765625,45.598665689820656],[12.7880859375,44.38669150215206],[19.1162109375,40.17887331434696],[15.029296875,36.2265501474709],[7.6025390625,39.13006024213511],[7.470703125,41.343824581185686],[10.21728515625,41.44272637767212],[9.64599609375,43.14909399920127],[7.91015625,43.30919109985686],[7.580566406250001,43.89789239125797],[7.778320312499999,44.24519901522129],[7.00927734375,44.308126684886126],[6.85546875,45.13555516012536]]]}}]}';
json2 = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-81.5625,-34.88593094075315],[-81.5625,11.86735091145932],[-28.125,11.86735091145932],[-28.125,-34.88593094075315],[-81.5625,-34.88593094075315]]]}}]}'
input_raster = '/home/vortex/Desktop/TMP/output3_4326_tt_nodata.tif'
zonalStats = get_zonalstatics_by_json(input_raster, json)
print zonalStats     '''
