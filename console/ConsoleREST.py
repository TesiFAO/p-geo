from flask import current_app as app
from flask import jsonify
from flask import Flask
from flask.ext.cors import cross_origin
from console import console_processes
from console import threads_map_key
import ConsoleThread

app = Flask(__name__)


@app.route('/start/<source_name>/<product>/<year>/<day>/<layer_name>')
@cross_origin(origins='*')
def process_start(source_name, product, year, day, layer_name):
    fjp = ConsoleThread.LayerDownloadThread(source_name, product, year, day, layer_name)
    fjp.start()
    key = layer_name
    if not threads_map_key in console_processes:
        console_processes[threads_map_key] = {}
    console_processes[threads_map_key][key] = fjp
    percent_done = round(fjp.percent_done(), 1)
    done = False
    return jsonify(key=key, percent=percent_done, done=done)


@app.route('/progress/<key>')
@cross_origin(origins='*')
def process_progress(key):
    if not threads_map_key in console_processes:
        console_processes[threads_map_key] = {}
    if not key in console_processes[threads_map_key]:
        return jsonify(key=key, percent=100, done=True)
    percent_done = console_processes[threads_map_key][key].percent_done()
    done = False
    if not console_processes[threads_map_key][key].is_alive() or percent_done == 100.0:
        del console_processes[threads_map_key][key]
        done = True
    percent_done = round(percent_done, 1)
    return jsonify(key=key, percent=percent_done, done=done)


@app.route('/kill/<key>')
@cross_origin(origins='*')
def kill(key):
    percent_done = console_processes[threads_map_key][key].percent_done()
    del console_processes[threads_map_key][key]
    done = True
    percent_done = round(percent_done, 1)
    return jsonify(key=key, percent=percent_done, done=done)

if __name__ == '__main__':
    app.run(debug=True)