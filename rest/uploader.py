import os
import sys
from flask import Flask, request, redirect, url_for, send_from_directory
from flask.ext.cors import cross_origin  # this is how you would normally import
import werkzeug
import json

try:
    from geoserver import geoserver
except Exception, e:
    sys.path.append('../')
    from geoserver import geoserver

geoserver = geoserver.Geoserver()

app = Flask(__name__)

UPLOAD_FOLDER = '/home/vortex/Desktop/upload'
ALLOWED_RASTER_EXTENSIONS = set(['zip', 'tif', 'geotiff'])
ALLOWED_VECTOR_EXTENSIONS = set(['zip', 'geojson', 'json'])

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_RASTER_EXTENSIONS'] = ALLOWED_RASTER_EXTENSIONS
app.config['ALLOWED_VECTOR_EXTENSIONS'] = ALLOWED_VECTOR_EXTENSIONS

def allowed_raster_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_RASTER_EXTENSIONS

# Route that will process the file upload
@app.route('/upload/raster', methods=['POST'])
@cross_origin()
def upload_raster():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_raster_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = werkzeug.secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #TODO: upload raster
        print "UPLOAD RASTER"
        geoserver.publish_coveragestore(filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return json.dumps({"upload":"complete"})
    else:
        return json.dumps({"upload":"file_not_allowed"})

#TODO: remove it, it's used to show the file after the upload
@app.route('/raster/uploads/<filename>')
@cross_origin()
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True, threaded=True)