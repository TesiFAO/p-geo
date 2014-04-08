import json, os, glob
from flask import Flask
from flask.ext.cors import cross_origin  # this is how you would normally import
import sys

try:
    from utils import log, config, geoserver
except Exception, e:
    sys.path.append('../')
    from utils import log, config, geoserver

try:
        from gis import rasterstats
except Exception, e:
    sys.path.append('../')
    from utils import rasterstats

app = Flask(__name__)

configWPS = config.Config('WPS')
configGeoserver = geoserver.Geoserver()

@app.route('/wps/hist/<layers>')
@cross_origin()
def create_histogram(layers):
    l = layers.split(":")
    return rasterstats.get_histogram(configGeoserver.get('datadir') + 'data/'+ l[0]+'/'+ l[1] + '/'+ l[1] +'.geotiff', 256);

if __name__ == '__main__':
    print configWPS.get('ip')
    print configWPS.get('port')
    print configWPS.get('debug')
    app.run(host=configWPS.get('ip'), port=configWPS.get('port'), debug=configWPS.get('debug'))