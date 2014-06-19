import glob
import sys
import os
from osgeo import gdal
from ftplib import FTP
import subprocess
import datetime

try:
    from utils import log, config, filesystem, ftp
except Exception, e:
    sys.path.append('../')
    from utils import log, config, filesystem, ftp

try:
    from manager import manager_layer
except Exception, e:
    sys.path.append('../')
    from manager import manager_layer



def process_hdfs(obj):
    print obj

    # extract bands
    hdfs = extract_files_and_band_names(obj["source_path"], obj["band"])

    # extract hdf bands
    single_hdfs = create_hdf_files(obj["output_path"], hdfs)

    # merge tiles
    hdf_merged = merge_hdf_files(obj["output_path"], obj["output_path"], obj["gdal_merge"])

    # translate
    tiff = warp_hdf_file(hdf_merged, obj["output_path"], obj["output_file_name"], obj["gdalwarp"])

    #add overviews
    if ( obj.has_key("gdaladdo") ):
        tiff = overviews_tif_file(tiff, obj["gdaladdo"]["parameters"], obj["gdaladdo"]["overviews_levels"]  )

    return tiff


def extract_files_and_band_names(path, band):
    bands = []
    hdfs = glob.glob(path + "/*.hdf")
    for f in hdfs:
        gtif = gdal.Open(f)
        sds = gtif.GetSubDatasets()
        bands.append(sds[int(band) - 1][0])
    return bands


def create_hdf_files(output_path, files):
    print "Create HDF Files"
    output_files = []
    i = 0;
    for f in files:
        print f
        cmd = "gdal_translate '" + f + "' " + output_path + "/" + str(i) + ".hdf"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        i += 1;
        #TODO catch the error
        print output
        print error

def merge_hdf_files(source_path, output_path, parameters=None):
    print "Merge HDF Files"
    print parameters
    output_file = output_path + "/output.hdf"

    # creating the cmd
    cmd = "gdal_merge.py "
    for key in parameters.keys():
        cmd += " " + key + " " + str(parameters[key])
    cmd += " " + source_path + "/*.hdf -o " + output_file

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output
    print error
    return output_file

def warp_hdf_file(source_file, output_path, output_file_name, parameters=None ):
    print "Warp HDF File to Tif"
    output_file = output_path + "/" + output_file_name

    cmd = "gdalwarp "
    for key in parameters.keys():
        cmd += " " + key + " " + str(parameters[key])
    cmd += " " + source_file + " " + output_file

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output
    print error
    return output_file


def overviews_tif_file(output_file, parameters=None, overviews_levels=None):
    print "Create Overviews TIFF File "


    cmd = "gdaladdo "
    for key in parameters.keys():
        cmd += " " + key + " " + str(parameters[key])
    cmd += " " + output_file
    cmd += " " + overviews_levels

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output
    print error
    return output_file


obj = {
    "output_file_name" : "MODIS_250m.tif",
    "source_path" : "/home/kalimaha/Development/GIS/MODIS/SADEC/",
    "band" : 1,
    "output_path" : "/home/kalimaha/Development/GIS/MODIS/SADEC/OUTPUT",
    "gdal_merge" : {
        "-n" : -3000,
        "-a_nodata" : -3000
    },
    "gdalwarp" : {
        "-multi" : "",
        "-of" : "GTiff",
        "-tr" : "0.0020833325, -0.0020833325",
        "-s_srs" :"'+proj=sinu +R=6371007.181 +nadgrids=@null +wktext'",
        "-co" : "'TILED=YES'",
        "-t_srs" : "EPSG:4326",
        "-srcnodata" : -3000,
        "-dstnodata" : "nodata"
    },
    "gdaladdo" : {
        "parameters" : {
            "-r" : "average"
        },
        "overviews_levels" : "2 4 8 16"
    }

}


output_file = process_hdfs(obj)
print output_file

# UPLOAD LAYER


#layer example
date = datetime.datetime(2014, 1, 30);
layer = {
    "workspace" : "modis",
    "layername" : "test_bella_guide3",
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

print manager_layer.publish_coveragestore(layer, output_file)
print manager_layer.g.set_default_style(layer["stylename"], layer["layername"], enabled=True)