import sys
import json
from datetime import timedelta
from flask import Flask, make_response, request, current_app
from flask.ext.cors import cross_origin  # this is how you would normally import
from flask import request
from flask import Response
from flask import render_template
from functools import update_wrapper
from bson import json_util
import datetime
from dateutil import parser
import flask
from flask import jsonify
import random
from random import uniform

try:
    from utils import log, config
except Exception, e:
    sys.path.append('../../')
    from utils import log, config

try:
    from mongo.crowddata import db
except Exception, e:
    sys.path.append('../../')
    from mongo.crowddata import db

crowddata = config.Config('crowddata')
l = log.Logger()

app = Flask(__name__)



@app.route('/crowddata')
@cross_origin(origins='*')
def default():
    return render_template('index.html')


#@app.route('/crowddata/insert/<db>/<collection>', methods=['PUT'])
@app.route('/crowddata/insert', methods=['PUT'])
@cross_origin(origins='*', headers=['Content-Type'])
def insert():
    print request.json
    db.insertData(request.json)
    return Response({'insert' : 'true'}, content_type='application/json; charset=utf-8')



#@app.route('/crowddata/find/<db>/<collection>', methods=['GET'])
@app.route('/crowddata/find/<collection>', methods=['GET'])
@cross_origin(origins='*')
def find(collection):
    result = db.find(collection)
    return Response(result, content_type='application/json; charset=utf-8')


@app.route('/crowddata/query', methods=['GET'])
@cross_origin(origins='*')
def query():
    return render_template('query.html')

#@app.route('/crowddata/find/<db>/<collection>/<varietycode>/<startdate>/<enddate>/<bbox>', methods=['GET'])
@app.route('/crowddata/map/data/<commoditycode>/<startdate>/<enddate>/<bbox>', methods=['GET'])
@cross_origin(origins='*')
def query_map(commoditycode, startdate, enddate, bbox ):
    commoditycode = [int(s) for s in commoditycode.split(',')]
    result = db.query_map(commoditycode, parser.parse(startdate), parser.parse(enddate), bbox)
    return  Response(result, content_type='application/json; charset=utf-8')


#@app.route('/crowddata/find/<db>/<collection>/<varietycode>/<startdate>/<enddate>/<bbox>', methods=['GET'])
@app.route('/crowddata/timeserie/data/<commoditycode>/<startdate>/<enddate>/<bbox>', methods=['GET'])
@cross_origin(origins='*')
def query_timeserie(commoditycode, startdate, enddate, bbox ):
    commoditycode = [int(s) for s in commoditycode.split(',')]
    result = db.query_timeserie(commoditycode, parser.parse(startdate), parser.parse(enddate), bbox)
    return  Response(result, content_type='application/json; charset=utf-8')

@app.route('/crowddata/find/date', methods=['GET'])
@cross_origin(origins='*')
def find_date( ):
    result = db.find_date()
    return  Response(result, content_type='application/json; charset=utf-8')



# for i in range(2, 3):
#     for j in range(1, 2):
#         for x in range(1, 10):
#             date = '2013,' + str(j) +',' + str(i)
#             print date
#             price = random.randrange(5,120,7)
#             x, y = uniform(-3,3), uniform(30, 40)
#             print price
#             db.insertData({'munitsymbol': 'kg', 'vendorcode': 1, 'varietyname': 'Variety of Cooking Bananas', 'fulldate': '2014,05,20,12,27,16', 'munitcode': 1, 'timezone': 'GMT+00:00', 'untouchedprice': 324, 'marketcode': 1, 'varietycode': 0, 'nationcode': 1, 'currencycode': 1, 'commoditycode': 1, 'price': price, 'commodityname': 'Cooking Bananas', 'citycode': 0, 'marketname': 'Market of Nairobi', 'date': date, 'geo': {'type': 'Point', 'coordinates': [x, y]}, 'vendorname': 'Vendor of Nairobi', 'kind': 0, 'notes': '', 'currencysymbol': 'KSh', 'quantity': 22})


if __name__ == '__main__':
    l.info(crowddata.get('ip') + ':' + str(crowddata.get('port')))
    app.run(host=crowddata.get('ip'), port=crowddata.get('port'), debug=crowddata.get('debug'))
