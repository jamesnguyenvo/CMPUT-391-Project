# Alright Q5
# Half the assignment
# Python3
from __future__ import print_function
import sqlite3 as sql
import sqlite3
import sys
from math import sqrt


# This will format the output from the rtreenode function so we can use it
def formatFunction(nodes):

    nodes = nodes.split("} {")
    nodes[0] = nodes[0][1:]
    if len(nodes) > 1:
        nodes[-1] = nodes[-1][:-1]

    # Split into usable info
    count = 0
    for node in nodes:
        nodes[count] = nodes[count].split()
        count += 1

    return nodes

def distance(point, point2):
    x,y = point
    centre = point2

    distance = sqrt(((x-centre[0])**2) + ((y-centre[1])**2))
    return distance


def createBranchList(nodes, point):

    x, y = point[0], point[1]
    branchList  = []

    # Create the branch list
    for node in nodes:
        nodeID = int(node[0])
        minX = float(node[1])
        maxX = float(node[2])
        minY = float(node[3])
        maxY = float(node[4])
        centre = maxX-((maxX-minX)/2), maxY-((maxY-minY)/2)

        # Compute the distance to the closest edge, NOT the centre
        # https://stackoverflow.com/questions/5254838/

        # If leaf node find the distance to the centre of the MBRs
        if nodeID >= 30000:
            d = distance(point, centre)

        # If not a leaf node find distance to edges
        else:
            d1 = distance(point, [minX, maxY])
            d2 = distance([0, y], [0,maxY])
            d3 = distance(point, [maxX, maxY])
            d4 = distance([x, 0],[minX, 0])
            d5 = distance([x,0], [maxX, 0])
            d6 = distance(point, [minX, minY])
            d7 = distance([0, y], [0,minY])
            d8 = distance(point, [maxX, minY])

            d = min(d1,d2,d3,d4,d5,d6,d7,d8)
            # Dmax is the furthest face, so this isnt quite right here
            # dmax = max(d1,d2,d3,d4,d5,d6,d7,d8)

            # If the point is inside then the distance is actually just 0
            if (x <= maxX and x >= minX and y >= minY and y <= maxY):
                d = 0

        branchList.append([d, nodeID])
    
    # Sort the branch list
    branchList.sort()
    return branchList

class NearestN():

    def __init__(self):
        self.nearest = []
        self.minimax = 1000

# Would we need a counter to ensure we dont recursively search the entire tree, but rather
# the nearest k
def nearestNeighbourSearch(node, point, nearest, k):

    x = point[0]
    y = point[1]

    # Query for the children of node 1
    # print(node)

    c.execute("SELECT rtreenode(2,data) FROM areaMBR_node where nodeno = ?", [str(node),])
    
    nodes = c.fetchall()

    nodes = nodes[0][0]
    nodes = formatFunction(nodes)
  
    # Get active branch list
    activeBranchList = createBranchList(nodes, point)

    # Sort active branch list based on minimax

    # If we are in a leaf node
    # (Hardcoded to check whether or not we are in a leaf node)
    # These are the closest x points to our input point
    # Im not sure if there may be closer points in other nodes
    if activeBranchList[0][1] >= 30000:
        for node in activeBranchList:

            nearest.append(node)

        # When we've found at least the k closest neighbours
        
        if len(nearest) >= max(k*5, k+1000):
            # Print nearest
            nearest.sort()
            for i in range(k):
                print(nearest[i][1], nearest[i][0], sep="\t")
            sys.exit()
        

    # If we are not in a leaf node
    else:

        # Perform downard pruning here
        # Not required as we do not want to prune, as we are looking for the k nearest neighbours

        # Iterate through active branch list
        for branch in activeBranchList:
            nearestNeighbourSearch(branch[1], point, nearest, k)

            # Perform upward pruning here
            # Same as above

    
    

    
    

if __name__ == '__main__':

    # Spoof system arguments for testing
    # sys.argv = ["", "unit3q3_rtree.db", "10", "10", "10"]


    # Make sure there is a proper amount of arguments
    if len(sys.argv) != 5:
        print("Missing command line arguments")
        sys.exit()

    database = sys.argv[1]
    x = int(sys.argv[2])
    y = int(sys.argv[3])
    k = int(sys.argv[4])


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

    # First we will check to make sure that the nodeIDs in the rtree and the nodes
    # in areaMBR will not conflict with each other

    maxR = c.execute("SELECT max(nodeno) FROM areaMBR_rowid;").fetchone()[0]
    minA = c.execute("SELECT min(rowid) FROM areaMBR_rowid;").fetchone()[0]

    if maxR >= minA:
        print("Invalid rtree setup")


    point = [x,y]
    nearest = []
    nearestNeighbourSearch(1, point, nearest, k)


    # Testing some shit by hand
    # 98224498|0.980200171470642|999.482055664063|2453.68896484375|3283.22680664063
    # 98223742|445.789672851562|799.5546875|623.624389648437|1089.03369140625
