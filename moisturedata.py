import sqlite3

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def select_all(conn, table):
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
        
def main():
    database = "pivotmanager.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("Query all moisture data:")
        select_all(conn, "moisture) 
 
if __name__ == '__main__':
    main()