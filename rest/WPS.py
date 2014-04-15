import json, os, glob
from flask import Flask
from flask.ext.cors import cross_origin  # this is how you would normally import
from flask import request
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
    return json.dumps(rasterstats.get_histogram(configGeoserver.get('datadir') + 'data/'+ l[0]+'/'+ l[1] + '/'+ l[1] +'.geotiff', 256))


@app.route('/wps/hist/<layers>/<geojson>', methods=['GET', 'POST'])
@cross_origin()
def create_histogram_geojson(layers, geojson):
    if request.method == 'POST':
        print 'POST'
    else:
        print 'GET'
    l = layers.split(":")
    return json.dumps(rasterstats.get_zonalstatics_by_json(configGeoserver.get('datadir') + 'data/'+ l[0]+'/'+ l[1] + '/'+ l[1] +'.geotiff',geojson ))


# TODO: make another service with <force> parameter
@app.route('/wps/coveragestats/<layers>')
@cross_origin()
def coverage_stats(layers):
    l = layers.split(":")
    return json.dumps(rasterstats.get_raster_statistics(configGeoserver.get('datadir') + 'data/'+ l[0]+'/'+ l[1] + '/'+ l[1] +'.geotiff', False))


if __name__ == '__main__':
    l.info(configWPS.get('ip') + ':' + str(configWPS.get('port')))
    app.run(host=configWPS.get('ip'), port=configWPS.get('port'), debug=configWPS.get('debug'))