from threading import Thread
from threading import Lock
import Queue
from ftplib import FTP
import os
import uuid
import time
from threading import Timer

from flask import current_app as app
from flask import jsonify
from flask import Flask
from flask.ext.cors import cross_origin

import ConsoleThread
from utils import config as c


app = Flask(__name__)
thread_manager_processes = {}
progress_map = {}
threads_map_key = 'FENIX'


class LayerDownloadThread(Thread):
    layer_name = None
    source_name = None
    total_size = 0
    download_size = 0

    def __init__(self, source_name, product, year, day, thread_name, q, key, queue_lock):

        Thread.__init__(self)

        self.source_name = source_name
        self.thread_name = thread_name
        self.product = product
        self.year = year
        self.day = day
        self.config = c.Config(self.source_name)
        self.q = q
        self.key = key
        self.queue_lock = queue_lock

    def run(self):

        while not exit_flag:
            self.queue_lock.acquire()
            if not self.q.empty():
                self.layer_name = self.q.get()
                if self.layer_name not in progress_map:
                    progress_map[self.layer_name] = {}
                self.queue_lock.release()
                ftp = FTP(self.config.get('ftp'))
                ftp.login()
                ftp.cwd(self.config.get('ftp_dir') + self.product + '/' + self.year + '/' + self.day + '/')
                ftp.sendcmd('TYPE i')
                total_size = ftp.size(self.layer_name)
                file = self.layer_name
                local_file = os.path.join(self.config.get('targetDir'), file)
                if not os.path.isfile(local_file):
                    try:
                        file_size = os.stat(local_file).st_size
                        if file_size < self.total_size:
                            with open(local_file, 'w') as f:
                                def callback(chunk):
                                    f.write(chunk)
                                    self.download_size += len(chunk)
                                    progress_map[self.layer_name]['layer_name'] = self.layer_name
                                    progress_map[self.layer_name]['total_size'] = total_size
                                    if 'download_size' not in progress_map[self.layer_name]:
                                        progress_map[self.layer_name]['download_size'] = 0
                                    progress_map[self.layer_name]['download_size'] = progress_map[self.layer_name]['download_size'] + len(chunk)
                                    progress_map[self.layer_name]['progress'] = float(progress_map[self.layer_name]['download_size']) / float(progress_map[self.layer_name]['total_size']) * 100
                                ftp.retrbinary('RETR %s' % file, callback)
                    except:
                        with open(local_file, 'w') as f:
                            def callback(chunk):
                                f.write(chunk)
                                self.download_size += len(chunk)
                                progress_map[self.layer_name]['layer_name'] = self.layer_name
                                progress_map[self.layer_name]['total_size'] = total_size
                                if 'download_size' not in progress_map[self.layer_name]:
                                    progress_map[self.layer_name]['download_size'] = 0
                                progress_map[self.layer_name]['download_size'] = progress_map[self.layer_name]['download_size'] + len(chunk)
                                progress_map[self.layer_name]['progress'] = float(progress_map[self.layer_name]['download_size']) / float(progress_map[self.layer_name]['total_size']) * 100
                            ftp.retrbinary('RETR %s' % file, callback)
                ftp.quit()
            else:
                self.queue_lock.release()
            time.sleep(1)

    def percent_done(self):
        return float(self.download_size) / float(self.total_size) * 100


class Manager(Thread):

    def __init__(self, source, product, year, day):
        Thread.__init__(self)
        self.source = source
        self.product = product
        self.year = year
        self.day = day

    def run(self):
        t = Timer(1, self.start_manager)
        t.start()

    def start_manager(self):

        global exit_flag
        exit_flag = 0

        print 'START | Layers Download Manager'

        config = c.Config(self.source)
        ftp = FTP(config.get('ftp'))
        ftp.login()
        ftp.cwd(config.get('ftp_dir'))
        ftp.cwd(self.product)
        ftp.cwd(self.year)
        ftp.cwd(self.day)
        global name_list
        name_list = ftp.nlst()
        ftp.quit()

        thread_list = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliet']
        queue_lock = Lock()
        work_queue = Queue.Queue(len(name_list))
        threads = []

        for tName in thread_list:
            key = str(uuid.uuid4())
            thread = LayerDownloadThread(self.source, self.product, self.year, self.day, tName, work_queue, key, queue_lock)
            thread.start()
            if not threads_map_key in thread_manager_processes:
                thread_manager_processes[threads_map_key] = {}
            thread_manager_processes[threads_map_key][key] = thread
            threads.append(thread)

        queue_lock.acquire()
        for word in name_list:
            work_queue.put(word)
        queue_lock.release()

        while not work_queue.empty():
            pass

        exit_flag = 1

        for t in threads:
            t.join()

        print 'DONE | Layers Download Manager'


@app.route('/start/manager/<source_name>/<product>/<year>/<day>')
@cross_origin(origins='*')
def manager_start(source_name, product, year, day):
    manager = Manager(source_name, product, year, day)
    manager.run()
    return jsonify(key='Q Will Start Soon', percent=0, done=False)


@app.route('/start/<source_name>/<product>/<year>/<day>/<layer_name>')
@cross_origin(origins='*')
def process_start(source_name, product, year, day, layer_name):
    fjp = ConsoleThread.LayerDownloadThread(source_name, product, year, day, layer_name)
    fjp.start()
    key = layer_name
    if not threads_map_key in thread_manager_processes:
        thread_manager_processes[threads_map_key] = {}
    thread_manager_processes[threads_map_key][key] = fjp
    percent_done = round(fjp.percent_done(), 1)
    done = False
    return jsonify(key=key, percent=percent_done, done=done)


@app.route('/progress/<layer_name>')
@cross_origin(origins='*')
def process_progress(layer_name):
    if layer_name not in progress_map:
        progress = {}
        progress['download_size'] = 'unknown'
        progress['layer_name'] = 'unknown'
        progress['progress'] = 'unknown'
        progress['total_size'] = 'unknown'
        return jsonify(progress=progress)
    return jsonify(progress=progress_map[layer_name])


@app.route('/kill/<key>')
@cross_origin(origins='*')
def kill(key):
    percent_done = thread_manager_processes[threads_map_key][key].percent_done()
    del thread_manager_processes[threads_map_key][key]
    done = True
    percent_done = round(percent_done, 1)
    return jsonify(key=key, percent=percent_done, done=done)


@app.route('/list/keys')
@cross_origin(origins='*')
def list_keys():
    urls = []
    for t in name_list:
        urls.append('http://127.0.0.1:5000/progress/' + t)
        print 'http://127.0.0.1:5000/progress/' + t
    return jsonify(keys=urls)


if __name__ == '__main__':
    app.run(debug=True)