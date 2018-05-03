from q1 import distance
import sqlite3 as sql
import sys

if __name__ == '__main__':

    # Ensure correct number of arguments are provided
    if len(sys.argv) < 2:
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

    # Grab tags to be searched for 
    tags = sys.argv[2:]

    # Ensures at least one tag is given to be searched for
    if len(tags) == 0:
        print("Missing arguments")
        sys.exit()

    # Ensure legal tags
    tag = tags.pop(0)

    if len(tag.strip()) < 3 or "=" not in tag or (tag[0] == '=' or tag[-1] == '='):
        print(tag, "is an invalid tag, please try again")
        sys.exit()

    firstTag = tag.split("=",1)
    
    # Add the first waytag 
    queryString = "SELECT COUNT(id) FROM waytag WHERE "
    tagString = "k = '" + firstTag[0] + "' AND v = '" + firstTag[1] + "'"
    queryString += tagString

    # Concatenate the rest of the tags 
    for tag in tags:
        if len(tag.strip()) < 3 or "=" not in tag or (tag[0] == '=' or tag[-1] == '='):
            print(tag, "is an invalid tag, continuing to next tag")
            continue

        tag = tag.split('=',1)
        queryString += " OR k = '" + tag[0] + "' AND v = '" + tag[1] + "'"
    queryString += ';'
    
    c.execute(queryString)
    count = c.fetchone()[0]

    # We now must compute the same query except so that it returns ID
    queryString = queryString.replace("COUNT(id)", "id")
    c.execute(queryString)
    ids = c.fetchall()

    largestD = 0
    # Now for each ID compute the path distance and return the largest one
    for id in ids:
        c.execute("WITH ordinals(ordinal1, ordinal2, id1, id2) AS \
            (SELECT w1.ordinal, w2.ordinal, w1.nodeid, w2.nodeid \
            FROM waypoint w1, waypoint w2 \
            WHERE w1.wayid= ? AND w1.wayid=w2.wayid AND w2.ordinal = w1.ordinal + 1) \
            SELECT SUM(distance(n1.lat, n2.lat, n1.lon, n2.lon)) \
            FROM ordinals JOIN node n1, node n2 ON n1.id = ordinals.id1 AND n2.id = ordinals.id2;", [id[0]])
        dist = c.fetchone()[0]

        if dist == None:
            dist = 0

        if dist > largestD:
            largestD = dist

    # queryString = ""
    print(count, largestD)
   
   

    
