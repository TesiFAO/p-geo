from psycopg2 import connect
import json


# def import_data(datastore, table, json_data):
#     db_connect_string = get_db_connect_string(datastore)
#     # print db_connect_string
#     try:
#         conn = connect(db_connect_string)
#         conn.autocommit=True;
#         _import_data(conn, table, json_data)
#     finally:
#         conn.close()
#     return True

def get_db_connect_string(datastore):
    db_connect_string = "host=%s port='%s' dbname=%s user=%s password=%s" %(datastore['host'], datastore['port'],datastore['dbname'], datastore['username'], datastore['password'])
    return db_connect_string

def _import_data(conn, table, json_data ):
    cur = conn.cursor()
    for row in json_data:
        # print row['code'], row['name']
        cur.execute('INSERT INTO data(code,name) VALUES (%s, %s)', (row['code'], row['name']))
    return False

def vacuum_analyze(conn, table):
    isolation_level = conn.isolation_level
    conn.set_isolation_level(0)
    cursor = conn.cursor()
    try:
        cursor.execute('vacuum analyze %s;' % table)
    finally:
        cursor.close()
        conn.set_isolation_level(isolation_level)



# datastore = {
#         "host" : "localhost",
#         "port" : "5432",
#         "username" : "fenix",
#         "password" : "Qwaszx",
#         "dbname" : "fenix"
#     }
#
# json_data = [{"code" : "test", "name" : "name"}]
#
# print "start"
# for count in range(1,1100):
#     import_data(datastore, "data", json_data)
#
# print "end"
#
# print "start"
# datastore = {
#         "host" : "localhost",
#         "port" : "5432",
#         "username" : "fenix",
#         "password" : "Qwaszx",
#         "dbname" : "fenix"
#     }
#
# json_data = [{"code" : "test", "name" : "name"}]
#
# db_connect_string = get_db_connect_string(datastore)
# conn = connect(db_connect_string)
# conn.autocommit=True;
# for count in range(1,1100):
#     _import_data(conn, "data", json_data)
# conn.close()
# print "end"