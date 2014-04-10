from osgeo import ogr

def import_shapefile(datastore, shapefile, table, overwrite=False):
    ogrds = _connect_to_db(datastore['host'], datastore['port'],datastore['dbname'], datastore['username'], datastore['password'])
    _import_shapefile(ogrds, shapefile, table, overwrite)
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
        name = ogrds.CopyLayer(sourceLayer,table,options).GetName()
        return True
    return False



