from flask import Flask
from flask import Response
from flask.ext.cors import cross_origin
from utils import config as c
from ftplib import FTP
import json

app = Flask(__name__)

@app.route('/list/<sourceName>')
@cross_origin(origins='*')
def listProducts(sourceName):
    config = c.Config(sourceName)
    ftp = FTP(config.get('ftp'))
    ftp.login()
    ftp.cwd(config.get('ftp_dir'))
    l = ftp.nlst()
    ftp.quit()
    return Response(json.dumps(l), content_type = 'application/json; charset=utf-8')

@app.route('/list/<sourceName>/<productName>')
@cross_origin(origins='*')
def listYears(sourceName, productName):
    config = c.Config(sourceName)
    ftp = FTP(config.get('ftp'))
    ftp.login()
    ftp.cwd(config.get('ftp_dir'))
    ftp.cwd(productName)
    l = ftp.nlst()
    ftp.quit()
    return Response(json.dumps(l), content_type = 'application/json; charset=utf-8')

@app.route('/list/<sourceName>/<productName>/<year>')
@cross_origin(origins='*')
def listDays(sourceName, productName, year):
    config = c.Config(sourceName)
    ftp = FTP(config.get('ftp'))
    ftp.login()
    ftp.cwd(config.get('ftp_dir'))
    ftp.cwd(productName)
    ftp.cwd(year)
    l = ftp.nlst()
    ftp.quit()
    return Response(json.dumps(l), content_type = 'application/json; charset=utf-8')

@app.route('/list/<sourceName>/<productName>/<year>/<day>')
@cross_origin(origins='*')
def listLayers(sourceName, productName, year, day):
    config = c.Config(sourceName)
    ftp = FTP(config.get('ftp'))
    ftp.login()
    ftp.cwd(config.get('ftp_dir'))
    ftp.cwd(productName)
    ftp.cwd(year)
    ftp.cwd(day)
    l = ftp.nlst()
    ftp.quit()
    return Response(json.dumps(l), content_type = 'application/json; charset=utf-8')


if __name__ == '__main__':
    app.run(port = 5001, debug = True)