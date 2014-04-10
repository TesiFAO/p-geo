from osgeo import gdal, ogr
import os
import sys
import json

try:
    from utils import filesystem
except Exception, e:
    sys.path.append('../')
    from utils import filesystem


def create_geotiff_tiles(input_raster):
    """
    create a TILED geotiff
    :param input_raster:
    :return: output_file path
    """
    output_file = ""
    return output_file

def create_geotiff_overviews(input_raster):
    """
    create OVERVIEWS geotiff
    :param input_raster:
    :return: output_file path
    """
    output_file = ""
    return output_file
