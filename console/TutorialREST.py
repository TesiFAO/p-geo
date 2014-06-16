from uuid import uuid4
from flask import current_app as app
from flask import jsonify
from flask import Flask, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper
from console import console_processes
import TutorialThread

app = Flask(__name__)
map_key = 'FENIX'

def crossdomain(origin = None, methods = None, headers = None, max_age = 21600, attach_to_all = True, automatic_options = True):
    """
        Taken from the Flask web-site:
        <a href='http://flask.pocoo.org/snippets/56/'>http://flask.pocoo.org/snippets/56/</a>
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()
    def get_methods():
        if methods is not None:
            return methods
        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp
            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp
        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/start/<sourceName>/<layerName>')
@crossdomain(origin='*')
def process_start(sourceName, layerName):
    fjp = TutorialThread.TutorialThread(sourceName, layerName)
    fjp.start()
    key = str(uuid4())
    if not map_key in console_processes:
        console_processes[map_key] = {};
    console_processes[map_key][key] = fjp
    percent_done = round(fjp.percent_done(), 1)
    done = False
    return jsonify(key = key, percent = percent_done, done = done)

@app.route('/kill/<key>')
@crossdomain(origin='*')
def kill(key):
    percent_done = console_processes[map_key][key].percent_done()
    del console_processes[map_key][key]
    done = True
    percent_done = round(percent_done, 1)
    return jsonify(key = key, percent = percent_done, done = done)

@app.route('/progress/<key>')
@crossdomain(origin='*')
def process_progress(key):
    if not map_key in console_processes:
        console_processes[map_key] = {}
    if not key in console_processes[map_key]:
        return jsonify(error = 'Invalid process key.')
    percent_done = console_processes[map_key][key].percent_done()
    done = False
    if not console_processes[map_key][key].is_alive() or percent_done == 100.0:
        del console_processes[map_key][key]
        done = True
    percent_done = round(percent_done, 1)
    return jsonify(key = key, percent = percent_done, done = done)

if __name__ == '__main__':
    app.run(port = 5000, debug = True)