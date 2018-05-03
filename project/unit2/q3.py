from q1 import distance
import sqlite3 as sql
import sys

if __name__ == '__main__':

    # Ensure correct number of arguments are provided
    if len(sys.argv) < 3:
        print("Missing way tag arguments")
        sys.exit()

    database = sys.argv[1]
    # Check if database file at least exists
    try:
        file = open(database, 'r')
    except:
        print(database, "does not exist or could not be opened")
        sys.exit()

    conn = sql.connect(database)
    conn.create_function("distance", 4, distance)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON;")
    conn.commit()

    wayID = sys.argv[2]

    # Ensure wayid given is valid
    try:
        wayID = int(wayID)
    except:
        print("Invalid wayID")
        sys.exit()


    c.execute("WITH ordinals(ordinal1, ordinal2, id1, id2) AS \
    (SELECT w1.ordinal, w2.ordinal, w1.nodeid, w2.nodeid \
    FROM waypoint w1, waypoint w2 \
    WHERE w1.wayid= ? AND w1.wayid=w2.wayid AND w2.ordinal = w1.ordinal + 1) \
    SELECT SUM(distance(n1.lat, n2.lat, n1.lon, n2.lon)) \
    FROM ordinals JOIN node n1, node n2 ON n1.id = ordinals.id1 AND n2.id = ordinals.id2;", [wayID])

    path = c.fetchone()[0]

    if path == None:
        print("Way does not exist or contains only one waypoint")
        sys.exit()

    print(path)

    conn.close()
    

