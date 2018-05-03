import sqlite3 as sql
import sys
from math import radians, sqrt, cos


''' Write a C program, in a file called q1.c that takes as input the database file and 
two node identifiers and prints to STDOUT their geographical distance, computed by
a suitable function from https://en.wikipedia.org/wiki/Geographical_distance and links therein.
The distance must be computed by a new SQL function, called from a query in your code.
In your README.m file for this assignment, explain your choice of distance function. 
Your explanation will count for 1/2 mark towards your grade in this question.
'''

# This is our SQL distance function
# I'm going to change it so that it computes the distance between every node pair and returns the maximum


def distance(lat1, lat2, lon1, lon2):
        # Using spherical distance from wikipedia
        lat = radians(lat2 - lat1)
        mLat = radians((lat1 + lat2) / 2)
        lon = radians(lon2 - lon1)
        distance = 6371.009 * sqrt(lat ** 2 + (cos(mLat) * lon) ** 2)
        return distance

def computeDistance(c, node1, node2):
    # First we must query the database to ensure both nodes exist
    # This assumes that if they exist, they have legal values
    c.execute("SELECT * FROM node WHERE id = ? or id = ?", (node1, node2))
    nodes = c.fetchall()
    if len(nodes) != 2:
        # One or both nodes does not exist in the database
        # Return -1
        return -1
    c.execute("SELECT distance(n1.lat,n2.lat, n1.lon, n2.lon) FROM node n1, node n2 WHERE n1.id = ? AND n2.id = ?", (node1, node2))
    return c.fetchone()[0]
    # Lets try to create the SQLite function here

def main():
    # Ensure correct number of arguments are provided
    if len(sys.argv) != 4:
        print("Missing arguments")
        sys.exit()

    database = sys.argv[1]
    node1 = sys.argv[2]
    node2 = sys.argv[3]

    # Ensure nodes are integers
    try:
        node1 = int(node1)
        node2 = int(node2)
    except:
        print("Invalid nodes given")
        sys.exit()

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


    result = computeDistance(c, node1, node2)
    if result == -1:
        print("One or both nodes does not exist")
        sys.exit()
    print(result)
    conn.close()

if __name__ == '__main__':
    main()