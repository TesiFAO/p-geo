import json, os, glob
from flask import Flask
from flask.ext.cors import cross_origin  # this is how you would normally import
import sys

try:
    from utils import log, config
except Exception, e:
    sys.path.append('../')
    from utils import log, config

try:
    from geoserver import geoserver
except Exception, e:
    sys.path.append('../')
    from geoserver import geoserver


try:
        from gis import rasterstats
except Exception, e:
    sys.path.append('../')
    from utils import rasterstats

configWPS = config.Config('WPS')
configGeoserver = geoserver.Geoserver()
l = log.Logger()

app = Flask(__name__)

@app.route('/wps/hist/<layers>')
@cross_origin()
def create_histogram(layers):
    l = layers.split(":")
    return rasterstats.get_histogram(configGeoserver.get('datadir') + 'data/'+ l[0]+'/'+ l[1] + '/'+ l[1] +'.geotiff', 256);


# TODO: make another service with <force> parameter
@app.route('/wps/coveragestats/<layers>')
@cross_origin()
def coverage_stats(layers):
    l = layers.split(":")
    return rasterstats.get_raster_statistics(configGeoserver.get('datadir') + 'data/'+ l[0]+'/'+ l[1] + '/'+ l[1] +'.geotiff', False);


if __name__ == '__main__':
    l.info('start')
    app.run(host=configWPS.get('ip'), port=configWPS.get('port'), debug=configWPS.get('debug'))