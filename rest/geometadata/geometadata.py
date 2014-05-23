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

# def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
#     if methods is not None:
#         methods = ', '.join(sorted(x.upper() for x in methods))
#     if headers is not None and not isinstance(headers, basestring):
#         headers = ', '.join(x.upper() for x in headers)
#     if not isinstance(origin, basestring):
#         origin = ', '.join(origin)
#     if isinstance(max_age, timedelta):
#         max_age = max_age.total_seconds()
#
#     def get_methods():
#         if methods is not None:
#             return methods
#
#         options_resp = current_app.make_default_options_response()
#         return options_resp.headers['allow']
#
#     def decorator(f):
#         def wrapped_function(*args, **kwargs):
#             if automatic_options and request.method == 'OPTIONS':
#                 resp = current_app.make_default_options_response()
#             else:
#                 resp = make_response(f(*args, **kwargs))
#             if not attach_to_all and request.method != 'OPTIONS':
#                 return resp
#
#             h = resp.headers
#
#             h['Access-Control-Allow-Origin'] = origin
#             h['Access-Control-Allow-Methods'] = get_methods()
#             h['Access-Control-Max-Age'] = str(max_age)
#             if headers is not None:
#                 h['Access-Control-Allow-Headers'] = headers
#             return resp
#
#         f.provide_automatic_options = False
#         return update_wrapper(wrapped_function, f)
#     return decorator

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



