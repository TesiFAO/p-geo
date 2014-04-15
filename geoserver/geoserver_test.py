import geoserver
from osgeo import ogr

import os.path
import psycopg2
import osgeo.ogr
import config
import psycopg2
import os.path
from sys import argv
import subprocess
import util
import osr
from urllib import urlencode
from urllib2 import urlopen
import json

g = geoserver.Geoserver()
#print g.get('username')
#g.publish_raster('/home/vortex/Desktop/TMP/output3_4326_tt_nodata.tif', 'asdasdasd')
#g.create_coveragestore('testasd', '/home/vortex/Desktop/TMP/output3_4326_tt_nodata.tif', 'fenix')
#a = g.publish_coveragestore('guido_test', '/home/vortex/Desktop/TMP/output3_4326_tt_nodata.tif', 'fenix')
#print str(a)

#g.set_default_style('evi', 'guido_test')

g.publish_shapefile('/home/vortex/Desktop/layers/test_import/IND_ports.shp', 'IND_ports_2',)
print 'END'



'''
srs = osr.SpatialReference()
srs.ImportFromEPSG('Mercator_Auxiliary_Sphere')
print srs
srs.AutoIdentifyEPSG()   ;'''