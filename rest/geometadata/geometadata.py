import sys
import json
from datetime import timedelta
from flask import Flask, make_response, request, current_app
from functools import update_wrapper
from flask.ext.cors import cross_origin  # this is how you would normally import
from flask import Response
from flask import render_template
from flask import request

try:
    from utils import log, config
except Exception, e:
    sys.path.append('../../')
    from utils import log, config

try:
    from mongo.geometadata import db
except Exception, e:
    sys.path.append('../../')
    from mongo.geometadata import db

config = config.Config('geometadata')
l = log.Logger()

app = Flask(__name__)

@app.route('/geometadata')
@cross_origin(origins='*')
def default():
    return render_template('default.html')

@app.route('/geometadata/query')
@cross_origin(origins='*')
def test():
    return render_template('query.html')


@app.route('/geometadata/find/<collection>', methods=['GET'])
@cross_origin(origins='*')
def find(collection):
    result = db.find(collection)
    return Response(result, content_type='application/json; charset=utf-8')

@app.route('/geometadata/find/<collection>/<layername>', methods=['GET'])
@cross_origin(origins='*')
def find_by_layername(collection, layername):
    result = db.find_by_layername(collection, layername)
    return Response(result, content_type='application/json; charset=utf-8')


# http://localhost:10800/geometadata/find/bycode/MOD13Q1/-1
@app.route('/geometadata/find/bycode/<code>/<sortdate>', methods=['GET'])
@cross_origin(origins='*')
def find_by_code(code, sortdate):
    collection = "layer"
    print sortdate
    result = db.find_by_code(collection, code, int(sortdate))
    return Response(result, content_type='application/json; charset=utf-8')


@app.route('/geometadata/query/<collection>', methods=['PUT'])
@cross_origin(origins='*')
def query_post(collection):
    # print collection
    # query = json.dumps(request.form['payload'])
    payload = json.loads(request.json['payload'])
    print payload
    result = db.find_query(collection, payload)
    print result
    return Response(result, content_type='application/json; charset=utf-8')


@app.route('/geometadata/delete/<layername>', methods=['DELETE'])
@cross_origin()
def delete_layer( layername):
    return "TODO :Remove layername from layer and stats collections"


if __name__ == '__main__':
    l.info(config.get('ip') + ':' + str(config.get('port')))
    app.run(host=config.get('ip'), port=config.get('port'), debug=config.get('debug'))



