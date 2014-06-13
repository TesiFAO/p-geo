import sys
from flask import Flask, make_response, request, current_app
from flask.ext.cors import cross_origin  # this is how you would normally import
from flask import request
from flask import Response
from random import randrange
import random
from datetime import timedelta, datetime
import json
import csv

try:
    from utils import log, config
except Exception, e:
    sys.path.append('../../')
    from utils import log, config

try:
    from postgresql.crowddata.crowddata import DBCrowddata
except Exception, e:
    sys.path.append('../../')
    from postgresql.crowddata.crowddata import DBCrowddata

config = config.Config('crowddata_postgresql')
database = config.get('database')
print database
db = DBCrowddata(database)
l = log.Logger()

app = Flask(__name__)

print "CONFIGURE THE DATABASE singleton instance!"

@app.route('/crowddata')
@cross_origin(origins='*')
def default():
    return Response("Crowddata", content_type='text charset=utf-8')


@app.route('/crowddata/insert', methods=['PUT'])
@cross_origin(origins='*', headers=['Content-Type'])
def insert():
    result = {}
    print request.json['table']
    print request.json['data']
    if (db.import_data(request.json['table'], request.json['data'])): result['insert'] = True;
    else: result['insert'] = False;
    return Response(json.dumps(result), content_type='application/json; charset=utf-8')

@app.route('/crowddata/query', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def query():
    print request.json['query']
    return Response(db.query(request.json['query']), content_type='application/json; charset=utf-8')


if __name__ == '__main__':
    l.info(config.get('ip') + ':' + str(config.get('port')))
    app.run(host=config.get('ip'), port=config.get('port'), debug=config.get('debug'))