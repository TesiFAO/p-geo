from osgeo import ogr

import os.path
import psycopg2
import os.path
import subprocess
import util
import osr
from urllib import urlencode
from urllib2 import urlopen
import json



def import_shapefile(datastore, shapefile, table, overwrite=False):
    #ogrds = _connect_to_db(datastore['host'], datastore['port'],datastore['dbname'], datastore['username'], datastore['password'])
    #_import_shapefile(ogrds, shapefile, table, overwrite)
    _import_shp2(datastore['host'], datastore['port'],datastore['dbname'], datastore['username'], datastore['password'], shapefile, table)
    return True

def _connect_to_db(databaseServer, databasePort,databaseName, databaseUser, databasePW):
    connString = "PG: host=%s port='%s' dbname=%s user=%s password=%s" %(databaseServer, databasePort,databaseName,databaseUser,databasePW)
    ogrds = ogr.Open(connString)
    return ogrds

def _import_shapefile(ogrds, shapefile, table, overwrite):
    ogr.RegisterAll()
    shapeDS = ogr.Open(shapefile)
    sourceLayer = shapeDS.GetLayerByIndex(0)
    options = []
    # TODO; test if the layer
    if ( overwrite ):
        # delete
        print 'delete table if exist'

    else:
        print 'check if table exist, and if exist return error'
        name = ogrds.CopyLayer(sourceLayer, table, options).GetName()
        return True
    return False


"""
This is mostly a Python wrapper for the shp2pgsql command line utility.
"""

IMPORT_MODE_CREATE = "c"
IMPORT_MODE_APPEND = "a"
IMPORT_MODE_STRUCTURE = "p"
IMPORT_MODE_DATA = ""
IMPORT_MODE_SPATIAL_INDEX = ""

#RODO: how to handle the encoding?
def shape_to_pgsql(conn, shape_path, table, mode, srid=-1, log_file=None, batch_size=1000):

    dbf_file = shape_path[0:-4] + '.dbf'
    prj_file = shape_path[0:-4] + '.prj'

    #Try detecting the SRID, by default we set to 4326 and hope the best
    srid = get_prj_srid(prj_file)

    args = [
        'shp2pgsql',  #TODO: pass the command dynamically in the config file of the server
        "-%s" % mode,
        "-W", "latin1",
        "-s", str(srid),
        shape_path,
        table]
    print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=log_file)

    cursor = conn.cursor()
    try:
        with p.stdout as stdout:
            for commands in util.groupsgen(util.read_until(stdout, ';'), batch_size):
                command = ''.join(commands).strip()
                if len(command) > 0:
                    cursor.execute(command)
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()


# TODO: enable it to recognize Mercator used by ESRI (3857)
def get_prj_srid(prj_file, srid="4326"):
    """
    if it doesn't find the SRID uses 4326 as default one
    :param prj_file:
    :param srid:
    :return:
    """
    if os.path.isfile(prj_file):
        prj_filef = open(prj_file, 'r')
        prj_txt = prj_filef.read()
        prj_filef.close()
        srs = osr.SpatialReference()
        srs.ImportFromESRI([prj_txt])
        srs.AutoIdentifyEPSG()
        # this is used to check if the prj is 'WGS_1984_Web_Mercator_Auxiliary_Sphere' (the one used by ESRI)
        mercator_ESRI = check_if_ESRI_mercator(srs.GetAttrValue('PROJCS'))
        if ( mercator_ESRI != None ):
            return mercator_ESRI
        else:
            code = srs.GetAuthorityCode(None)
            if code:
                srid = code
            else:
                #Ok, no luck, lets try with the OpenGeo service
                check_srid = check_if_ESRI_mercator(prj_txt)
                if check_srid != None:
                    srid = check_srid
                '''
                query = urlencode({
                    'exact' : True,
                    'error' : True,
                    'mode' : 'wkt',
                    'terms' : prj_txt})
                print query
                webres = urlopen('http://prj2epsg.org/search.json', query)
                jres = json.loads(webres.read())
                print jres
                if jres['codes']:
                    srid = int(jres['codes'][0]['code'])  '''
    else:
        print "TODO: .prj doesn't exist try to get from the shp? or send error"
    print srid
    return srid


def check_if_ESRI_mercator(projcs):
    print projcs
    if projcs == 'WGS_1984_Web_Mercator_Auxiliary_Sphere':
        return 3857
    return None

def check_prj_from_webservice(prj_txt):
    query = urlencode({
        'exact' : True,
        'error' : True,
        'mode' : 'wkt',
        'terms' : prj_txt})
    webres = urlopen('http://prj2epsg.org/search.json', query)
    jres = json.loads(webres.read())
    print jres
    if jres['codes']:
        return int(jres['codes'][0]['code']) #srid
    return None


def vacuum_analyze(conn, table):
    isolation_level = conn.isolation_level
    conn.set_isolation_level(0)
    cursor = conn.cursor()
    try:
        cursor.execute('vacuum analyze %s;' % table)
    finally:
        cursor.close()
        conn.set_isolation_level(isolation_level)


def _import_shp2(databaseServer, databasePort,databaseName, databaseUser, databasePW, shapefile, table):

    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (databaseServer, databaseName, databaseUser, databasePW))
    shape_to_pgsql(conn, shapefile, table, IMPORT_MODE_CREATE + IMPORT_MODE_DATA + IMPORT_MODE_SPATIAL_INDEX)
    vacuum_analyze(conn, table)



