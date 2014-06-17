import sys

try:
    from utils import config, log, filesystem
except Exception, e:
    sys.path.append('../')
    from utils import config, log, filesystem

try:
    from gis import rasterstats
except Exception, e:
    sys.path.append('../')
    from gis import rasterstats

try:
    from postgresql import DBConnection
except Exception, e:
    sys.path.append('../')
    from postgresql import DBConnection

#  Mongo GeoStats Database (used to store the the statistics of the layer)
try:
    from mongo.geostats import db as db_geostats
except Exception, e:
    sys.path.append('../')
    from mongo.geostats import db as db_geostats


class GeoStats:

    # json with the layer definition
    layer = None

    # json with the geostats configurations
    geostats = None

    # layer_uid used in saving the statistics and initializid in the init method
    layer_uid = None

    # path to the layer
    layer_path = None

    # connection to the PostGIS Database
    db_connection_string = None

    # Datastore (Table) used by the PostGIS Database
    datastore = None

    config = config.Config('geostatistics')

    def __init__(self, datastore = None):
        # TODO: pass and alternative datastore
        if  ( datastore is None): self.datastore = self._get_default_datastore();
        else: self.datastore = datastore
        self.db_connection_string = DBConnection.get_connection_string(self.datastore, True)
        return None

    def _get_default_datastore(self):
        default_datastore = self.config.get('default_datastore')
        datastore = self.config.get('spatial_datastores')
        for d in datastore:
            if (default_datastore in d['datastore']):
                return d
        return False

    def stats_layer_json(self, layer, geostats):
        '''
        :param layer: json layer containing the uid stored in the GeoMetadata Database
        :param geostats: json with statistics definitions
        :return:
        '''
        self.layer = layer
        self.geostats = geostats

        # finding the layer path
        self.layer_path = self.config.get("datadir")
        if ( ":" in self.layer["uid"] ):
            l = self.layer["uid"].split(":")
            self.layer_path += l[0] + "/" + l[1] + ".geotiff";
            # layer_uid used in saving the statistics
            self.layer_uid = l[0] + "_" + l[1]
        else:
            # this one is supposed to be passed with the relative extension
            self.layer_path += self.config["datadir"] + self.layer["uid"];
            # layer_uid used in saving the statistics
            self.layer_uid = self.layer["uid"]

        # layer_uid used in saving the statistics
        self.layer_uid += "_" + self.geostats["name"]

        # get statistics
        self._get_statistics()



    def stats_layer_filename(self, layer_filename, geostats):
        '''
        :param layer_filename: filename store int he "datadir" folder
        :param geostats: json with statistics definitions
        :return:
        '''
        self.layer_path = config["datadir"] + layer_filename
        self.geostats = geostats

    def stats_layer_path(self, layer_path, geostats):
        '''
        :param layer_path: layer_path
        :param geostats: json with statistics definitions
        :return:
        '''
        self.layer_path = layer_path
        self.geostats = geostats

    def _get_statistics(self):
        # TODO: a switch
        if ( "query" in self.geostats ):
            self._get_stats_query(self.geostats['query'], self.geostats['code'])
        if ( "query_condition" in self.geostats ):
            self._get_stats_query_condition()

        return None

    def _get_stats_query(self, query, code, save_stats=True):

        # crop raster by vector using postgis
        file_path = rasterstats.crop_raster_by_vector_postgis(self.layer_path, query, self.db_connection_string, "nodata")
        print file_path

        # do statistics on the file
        stats = self.get_stats(file_path, True)

        # save statistics
        if save_stats is True:
            json = {
                "code" : code,
                "info" : stats
            }
            db_geostats.insert_stats(self.layer_uid, json)

        return stats

    def _get_stats_query_condition(self):
        # get all codes from query TODO: (It's ugly)
        db = DBConnection.DBConnection(self.datastore);

        column_filter = self.geostats['query_condition']['column_filter']
        select = self.geostats['query_condition']['select']
        from_query = self.geostats['query_condition']['from']
        where = self.geostats['query_condition']['where']

        query = "SELECT " + select + " FROM "+ from_query +" WHERE " + where
        print query
        result = db.query(query)
        print result

        for r in result:
            print r[0]
            # TODO: problems with query Strings and Integers (or whatever)
            query = "SELECT * FROM " + from_query + " WHERE " + column_filter + " IN (" + str(r[0]) + ")"
            print query
            stats = self._get_stats_query(query, str(r[0]), True)
        return stats

    def get_stats(self, file_path, remove_file=False):
        s = rasterstats.get_raster_statistics(file_path, True)
        hist = rasterstats.get_histogram(file_path, True)
        stats = {"stats": s,"hist": hist}

        # remove tmp file
        if ( remove_file is True):
            filesystem.remove(file_path)
        return stats

    def _save_stats(self, uid, code, stats):
        db_geostats.insert_stats()

layer = {
    # the stored UID in the GeoMetadata database
    "uid" : "MODIS:test",

}

geostats = {
    "code" : "226",
    "query": "SELECT * FROM gaul0_3857 WHERE adm0_code IN ('226') ",
    "statistics" : "all",
    "save_stats" : True

}

geostats = {
    "query_condition" : {
        "column_filter" : "adm1_code",
        "select" : "distinct(adm1_code)",
        "from"   : "gaul1_3857",
        "where"  : "adm0_code IN ('226')"
    },
    "save_stats" : True
}

geostats = {
    "name" : "gaul2",
    "query_condition" : {
        "column_filter" : "adm2_code",
        "select" : "distinct(adm2_code)",
        "from"   : "gaul2_3857",
        "where"  : "adm0_code IN ('226')"
    },
    "save_stats" : True
}



gs = GeoStats()
gs.stats_layer_json(layer, geostats)