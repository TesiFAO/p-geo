import sys

try:
    from postgresql.DBConnection import DBConnection
except Exception, e:
    sys.path.append('../../')
    from postgresql.DBConnection import DBConnection


class DBCrowddata:
    DBConnection = None

    def __init__(self, database):
        if self.DBConnection is None:
            self.DBConnection = DBConnection(database)

    def import_data(self, table, json_data ):
        try:
            for row in json_data:
                # check if lat and lon are in the file
                if ( 'lat' in row and 'lon' in row ) : row['geo'] = "POINT ("+ str(row['lat']) +" "+ str(row['lon']) +")";
                insert_keys = ""
                insert_values = ""
                for key in row.keys():
                    insert_keys += key + ","
                    if( key == 'geo'): insert_values += 'ST_GeomFromText(%s, 4326),'
                    else: insert_values += "%s,"

                #remove last comma
                insert_keys = insert_keys[:-1]
                insert_values = insert_values[:-1]

                return self.DBConnection.insert(table, insert_keys, insert_values, row.values())
        except Exception, e:
            print "DBCrowddata.import_data Error: ", e
            return False

    def query(self, query ):
        return self.DBConnection.query(query)




    

