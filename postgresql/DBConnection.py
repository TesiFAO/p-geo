import psycopg2
import json

class DBConnection:
    con = None


    def __init__(self, database):
        if DBConnection.con is None:
            try:
                db_connect_string = "host=%s port='%s' dbname=%s user=%s password=%s" %(database['host'], database['port'],database['dbname'], database['username'], database['password'])
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
                print rows
                print json.dumps(rows)
                return json.dumps(rows)
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

    # blacklist methods not alloweds
    def check_query(self, query):
        q = query.lower()
        if "insert" in q: return False
        if "update" in q: return False
        if "delete" in q: return False
        return True