import json, os, glob
from flask import Flask
from flask.ext.cors import cross_origin  # this is how you would normally import
from flask import request
import sys
#import jsonify

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
    # http://127.0.0.1:1236/wps/hist/fenix:output3_4326_deflate/%7B%22type%22:%22FeatureCollection%22,%22features%22:%5B%7B%22type%22:%22Feature%22,%22properties%22:%7B%7D,%22geometry%22:%7B%22type%22:%22Polygon%22,%22coordinates%22:%5B%5B%5B13.0078125,-36.03133177633187%5D,%5B13.0078125,-28.30438068296277%5D,%5B35.15625,-28.30438068296277%5D,%5B35.15625,-36.03133177633187%5D,%5B13.0078125,-36.03133177633187%5D%5D%5D%7D%7D%5D%7D
    if request.method == 'POST':
        print 'POST'
    else:
        print 'GET'
    l = layers.split(":")
    return json.dumps(rasterstats.get_zonalstatics_by_json(configGeoserver.get('datadir') + 'data/'+ l[0]+'/'+ l[1] + '/'+ l[1] +'.geotiff',geojson ))

@app.route('/wps/raster/gfi/<layers>/<x>/<y>', methods=['GET', 'POST'])
@cross_origin()
def raster_gfi(layers, x, y):
    '''
    this service returns
    :param layers: array of layers ["workspace:layername] or ["layername"] using the default workspace
    :param x: x coordinate
    :param y: y coordinate
    :return: the values at the xy coordinates of the given layers
    '''
    # http://127.0.0.1:1236/wps/raster/gfi/%5B%22fenix:3B42RT.2014030100.7.1day_tiled2222%22,%22fenix:3B42RT.2014030100.7.1day_tiled%22%5D/8.64/2.4
    if request.method == 'POST':
        #TODO: handle and check POST request
        layers = request.form['layers']
        x = request.form['x']
        y = request.form['y']
    '''else:
        layers = request.args.get('layer', '')
        x = request.args.get('x', '')
        y = request.args.get('y', '')
    '''

    ls = json.loads(layers)
    querylayers = []
    for l in ls:
        ql = []
        if not ":" in l: ql.append(configGeoserver.get('default_workspace')); ql.append(l);
        else: ql = l.split(":")
        querylayers.append(configGeoserver.get('datadir') + 'data' + os.sep + ql[0]+ os.sep + ql[1] + os.sep + ql[1] +'.geotiff')
    result = json.dumps(rasterstats.cell_rasters_value(querylayers, x, y))
    print result
    return result


# TODO: make another service with <force> parameter
@app.route('/wps/coveragestats/<layers>')
@cross_origin()
def coverage_stats(layers):
    l = layers.split(":")
    return json.dumps(rasterstats.get_raster_statistics(configGeoserver.get('datadir') + 'data/'+ l[0]+'/'+ l[1] + '/'+ l[1] +'.geotiff', False))


@app.route('/wps/test')
@cross_origin()
def wps_test():
    return json.dumps(rasterstats.test())


@app.route('/wps')
@cross_origin()
def wps_home():
    return "WPS processing"



if __name__ == '__main__':
    l.info(configWPS.get('ip') + ':' + str(configWPS.get('port')))
    app.run(host=configWPS.get('ip'), port=configWPS.get('port'), debug=configWPS.get('debug'), threaded=True)
