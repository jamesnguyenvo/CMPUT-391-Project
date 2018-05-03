# Question 2
from __future__ import print_function
import sqlite3 as sql
import sys
from q1 import convertLat, convertLon, getOrigins

def main():
    # Make sure there is a proper amount of arguments
    if len(sys.argv) != 2:
        print("Missing command line arguments")
        sys.exit()

    database = sys.argv[1]

    # Check if the database exists
    try:
        file = open(database, 'r')
    except:
        print(database, "does not exist or could not be opened.")
        sys.exit()

    conn = sql.connect(database)
    conn.create_function("convertLat", 2, convertLat)
    conn.create_function("convertLon", 2, convertLon)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON;")
    conn.commit()

    # Create the areaMBR table if it does not already exist
    print("DROP TABLE IF EXISTS areaMBR;")
    print("""CREATE TABLE IF NOT EXISTS areaMBR ( 
           id integer, 
           minX float, 
           maxX float, 
           minY float,
           maxY float,
           PRIMARY KEY (id) 
           );""")

    # So now we must add the MBR of every closed way
    # So first find all the closed ways and their nodes
    # Find the max/min lat/lons
    # (Could possible do some group by stuff to do this in a single query)
    c.execute("SELECT w.id, min(n.x),max(n.x),min(n.y), max(n.y) \
    FROM way w, waypoint wp, nodeCartesian n \
    WHERE w.closed=1 and w.id=wp.wayid and n.id=wp.nodeid \
    GROUP BY w.id;")
    ways = c.fetchall()

    # So we will iterate through the resulting rows from the query
    # Print all the id's with x and y coords
    print("INSERT INTO areaMBR VALUES ")
    for wayid, minX, maxX, minY, maxY, in ways:

        if wayid == ways[-1][0]:
            print("(", wayid, ",", minX, ",", maxX, ",", minY, ",", maxY, ");", sep="")
            continue

        print("(",wayid,",", minX,",",maxX,",",minY,",",maxY, "),", sep="")

if __name__ == '__main__':
    main()
