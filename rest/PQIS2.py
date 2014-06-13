import numpy as np
import sys
from flask import Flask, Response, request, redirect, url_for, send_from_directory
from flask.ext.cors import cross_origin  # this is how you would normally import

app = Flask(__name__)

# Route that will process the file upload
@app.route('/<matrix>', methods=['GET'])
@cross_origin()
# 1,1,1,1,1,1;27,-60,2,0,30,0;3,0,-32,30,0,0;0,3,27,-32,0,2;0,27,0,2,-30,0;0,0,3,0,0,-2
def invert(matrix):
    try:
        tmp_matrix = []
        for column in matrix.split(';'):
            tmp_matrix.append([float(s) for s in column.split(',')])
        # a = np.array([[1,1,1,1,1,1],[27,-60,2,0,30,0],[3,0,-32,30,0,0],[0,3,27,-32,0,2],[0,27,0,2,-30,0],[0,0,3,0,0,-2]])
        a = np.array(tmp_matrix)
        x = np.linalg.inv(a)
        x = np.transpose(x)
    except Exception, e:
        print e
    return Response(np.array_str(x), content_type='text; charset=utf-8')

if __name__ == '__main__':
    app.run(port=10500, debug=False)






