import psycopg2
import json

class DBConnection:
    con = None
    database = None

    def __init__(self, database):
        if DBConnection.con is None:
            try:
                self.database = database
                db_connect_string = self.get_connection_string(False)
                self.con = psycopg2.connect(db_connect_string)
                print('Database connection opened.')
            except psycopg2.DatabaseError as db_error:
                print("Erreur :\n{0}".format(db_error))

    # TODO: autocommit as parameter (FOR BULK)
    def insert(self, table, insert_keys, insert_values, values):
        try:
            self.con.autocommit=True;
            cur = self.con.cursor()
            # query
            sql = "INSERT INTO "+ table +" ("+ insert_keys +") VALUES ("+ insert_values +")"
            cur.execute(sql, values)
            return True
        except Exception, e:
            self.con.rollback()
            print "DBConnection.import_data Error: ", e
            return False


    def query(self, query):
        try:
            if (self.check_query(query)):
                cur = self.con.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                return rows
            else: return False
        except Exception, e:
            self.con.rollback()

    def __del__(self):
        self.close_connection();

    def __exit__(self):
        self.close_connection();

    def close_connection(self):
        if self.con is not None:
            self.con.close()
            print('Database connection closed.')

    def get_connection_string(self, add_pg=True):
        db_connection_string = ""
        if ( add_pg is True):
            db_connection_string += "PG:"
        db_connection_string += "host=%s port='%s' dbname=%s user=%s password=%s" %(self.database['host'], self.database['port'],self.database['dbname'], self.database['username'], self.database['password'])
        return db_connection_string

    # blacklist methods not alloweds
    def check_query(self, query):
        q = query.lower()
        if "insert" in q: return False
        if "update" in q: return False
        if "delete" in q: return False
        return True


def get_connection_string(database, add_pg=True):
    db_connection_string = ""
    if add_pg is True:
        db_connection_string += "PG:"
        db_connection_string += "host=%s port='%s' dbname=%s user=%s password=%s" %(database['host'], database['port'],database['dbname'], database['username'], database['password'])
    return db_connection_string