from osgeo import gdal
import json

def get_histogram( input_value_raster, force=False, buckets=256, include_out_of_range=0 ):

    ds = gdal.Open( input_value_raster )

    # pass the band selection
    band = 1

    # get min and max values (force the recalculation?)
    min = ds.GetRasterBand(band).GetMinimum()
    max = ds.GetRasterBand(band).GetMaximum()

    histogram = ds.GetRasterBand(band).GetHistogram( buckets=buckets, min=min, max=max, include_out_of_range = include_out_of_range )

    # encode the json
    return json.dumps({ "buckets":buckets,"min":min,"max":max,"values":histogram}, separators=(',',':'))

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

def get_zonalstatics_by_json(json, input_raster):
    jsonFile = createTmpFile(json)
    shpFile = createShapefileFromJSON(jsonFile)
    shp = ogr.Open(shpFile)
    lyr = shp.GetLayer()
    stats = []
    # loop through the features in the layer
    feature = lyr.GetNextFeature()
    #print feature
    i = 0
    while feature:
        # create a tmp shapefile
        feature_shp_file = createSHPFromFeature(feature)
        # create a tmp raster
        raster_file = cropRasterByVector(feature_shp_file, input_raster )
        # do statistics on the new raster
        stat = getRasterStatistics(raster_file)
        # calculate histogram
        hist = Histogram.calculate_histogram(raster_file)
        stats.append({"fid": i, "stat": stat, "hist": hist})
        # check next feature
        feature = lyr.GetNextFeature()
        i +=1
    return stats