import MySQLdb

def get_db_connection():
    conn = MySQLdb.connect(
        host='campuslink.cnaw2608ajs2.us-east-1.rds.amazonaws.com',
        user='CampusLink',
        password='13020101',
        database='campuslink_integrado'
    )
    conn.autocommit = True
    return conn
