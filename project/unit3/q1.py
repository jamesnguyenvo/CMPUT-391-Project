# Question 1
from __future__ import print_function
import sys
import sqlite3 as sql
import math


def getOrigins(cursor):
    '''
    This function will grab the minimum latitude and longittude from the database to use as origins
    '''
    originLat = cursor.execute("SELECT MIN(lat) FROM node WHERE lat<>0 and lon<>0;").fetchone()[0]
    originLon = cursor.execute("SELECT MIN(lon) FROM node WHERE lat<>0 and lon<>0;").fetchone()[0]

    return originLat, originLon

def convertLat(lat, originLat):
    '''
    This function will convert the latitude given into a cartesian y coordinate
    relative to the lowest y coordinate value
    '''

    # Grab the lowest lat as origin
    # originLat = c2.execute("SELECT MIN(lat) FROM node WHERE lat<>0 and lon<>0;").fetchone()[0]
    diffY = lat - originLat  
    y = diffY * 111286
    
    return y

def convertLon(lon, originLon):
    '''
    This function will convert the longitude given into a cartesian x coordinate
    relative to the lowest x coordinate value
    '''
    
    # Grab the lowest lon as origin
    # originLon = c2.execute("SELECT MIN(lon) FROM node WHERE lat<>0 and lon<>0;").fetchone()[0]
    diffX = lon - originLon
    x = diffX * 67137

    return x

def printResults(resultList):
    for x in range (len(resultList)):
        if x == len(resultList) - 1:
            print(str(resultList[x]) + ';')
            break
        print(str(resultList[x]), ",", sep="")


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
    
    # Create the nodeCartesian table
    print("DROP TABLE IF EXISTS nodeCartesian;")
    print("""CREATE TABLE IF NOT EXISTS nodeCartesian ( 
           id integer, 
           x float, 
           y float, 
           PRIMARY KEY (id) 
           );""") 

    originLat, originLon = getOrigins(c)

    print("INSERT INTO nodeCartesian(id, x, y) VALUES ")
    # Query for the latitude and longitude conversions using our two created SQL function
    result = c.execute("SELECT id, convertLon(lon,?), convertLat(lat,?) FROM node;",[originLon, originLat]).fetchall()
    # Print all the id's with x and y coords
    printResults(result)

if __name__ == '__main__':
    main()