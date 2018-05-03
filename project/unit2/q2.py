from q1 import distance
import sqlite3 as sql
import sys

'''Write a C program, in a file called q2.c that takes as input the database file and a list of
strings of the form key=value; finds all nodes in the database that have at least one 
tag matching a key/value combination from the input list; and prints to STDOUT: the number of 
such node elements, as well as the largest pairwise distance among those nodes.
The maximum distance must be computed by a SQL query that uses the function you created for Q1.'''

if __name__ == '__main__':

    # Ensure correct number of arguments are provided
    if len(sys.argv) < 2:
        print("Missing arguments")
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

    # Make sure at least one tag is given
    tags = sys.argv[2:]
    if len(tags) == 0:
        print("Missing arguments")
        sys.exit()

    # Ensure tag is in correct format here
    tag = tags.pop(0)

    if len(tag.strip()) < 3 or "=" not in tag or (tag[0] == '=' or tag[-1] == '='):
        print(tag, "is an invalid tag, please try again")
        sys.exit()

    tag = tag.split("=",1)

    # First create the query string using all the tags
    queryString = "SELECT count(*) FROM node, nodetag WHERE node.id = nodetag.id AND ("
    tagString = "k = '" + tag[0] + "' AND v = '" + tag[1] + "'"
    queryString += tagString

    # Loop through the tags and add each remaining tag to the query string
    for tag in tags:
        if len(tag.strip()) < 3 or "=" not in tag or (tag[0] == '=' or tag[-1] == '='):
            print(tag, "is an invalid tag, continuing to next tag")
            continue
        tag = tag.split("=",1)
        string = " OR k = '" + tag[0] + "' AND v = '" + tag[1] + "'"
        queryString += string
        tagString += string
    queryString += ")"
    # Get the count for these nodes
    # print(queryString)
    c.execute(queryString)
    count = c.fetchone()[0]

    # Now get distance on this same query instead of count
    # We must cross product each nodes lat long with each other
    # Then store the nodes lat long in a recursive table
    # Then select the max

    # queryString = '''
    # WITH RECURSIVE
    # total(x, y) AS(
    # SELECT n1.lat, n1.lon
    # FROM node n1, nodetag
    # WHERE k = "crossing" AND v = "zebra" AND nodetag.id = n1.id)
    # SELECT max(distance(t1.x, t2.x, t1.y, t2.y))
    # FROM total t1, total t2
    # WHERE t1.x != t2.x AND t1.y != t2.y;
    # '''

    queryString = '''WITH RECURSIVE 
    total(x, y) AS(
    SELECT n1.lat, n1.lon
    FROM node n1, nodetag
    WHERE nodetag.id = n1.id AND (''' + tagString + '''))
    SELECT max(distance(t1.x, t2.x, t1.y, t2.y))
    FROM total t1, total t2
    WHERE t1.x != t2.x AND t1.y != t2.y;'''

    #
    # print(queryString)
    c.execute(queryString)
    distance = c.fetchone()[0]
    print(count, distance)