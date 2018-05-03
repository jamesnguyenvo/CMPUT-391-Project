# Question 4
from __future__ import print_function
import sqlite3 as sql
import sys
from random import uniform
import timeit

# This will also get the minimum bounding rectangle for the entire areaMBR table
# We will use this to help us randomly generate the lower left point for the rectangle
def createRectangle(cursor, l):

    cursor.execute("SELECT min(minX), max(maxX), min(minY), max(maxY) FROM areaMBR")
    # Grab the x and y values
    mbr = cursor.fetchall()[0]
    minX = mbr[0]
    maxX = mbr[1]
    minY = mbr[2]
    maxY = mbr[3]
    # Create the rectangle
    width = l * uniform(1, 10)
    height = l * uniform(1, 10)

    # X is lon, Y is lat
    x = uniform(minX-width, maxX)
    y = uniform(minY-height, maxY)

    # Increase the bounds such that a rectangle at touches the overall MBR
    minX = x
    maxX = x + width
    minY = y
    maxY = y + height

    return minX, maxX, minY, maxY


def main():
    # Make sure there is a proper amount of arguments
    if len(sys.argv) != 4:
        print("Missing command line arguments")
        sys.exit()

    database = sys.argv[1]
    l = int(sys.argv[2])
    k = int(sys.argv[3])

    # Check if the database exists
    try:
        file = open(database, 'r')
    except:
        print(database, "does not exist or could not be opened.")
        sys.exit()

    conn = sql.connect(database)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON;")
    conn.commit()

    # Repeat k times
    totalTime = 0.0
    count = 0
    for i in range(k):
        while count == 0:
            # Generate rectangles
            rectangle = createRectangle(c,l)
            # Grab the coordinate values of the generated rectangle 
            minX = rectangle[0]
            maxX = rectangle[1]
            minY = rectangle[2]
            maxY = rectangle[3]

            # Time the run time for the queries 
            start = timeit.default_timer()
            # Query for count of contained rectangles 
            # If the query result is 0, we do not consider this, and generate a new rectangle
            count = c.execute("SELECT COUNT(*) FROM areaMBR WHERE \
                      maxX <= ? AND minX >= ? AND maxY <= ? and minY >= ?;" \
                      , [maxX, minX, maxY, minY]).fetchone()[0]
            stop = timeit.default_timer()
            time = stop - start

        # add time to the queried database
        totalTime += time
        
    print(k, "\t", l, "\t", totalTime/k)

    # Then we should ensure at least one MBR exists inside it
    # (Could this be done implicitly without extra calculations?)

if __name__ == '__main__':
    main()
