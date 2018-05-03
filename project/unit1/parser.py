import xml.etree.ElementTree as ET
import sqlite3 as sql

def main():
    xmlFile = input("Enter the name of the file eg. edmonton.osm: ")
    #xmlFile = 'test.osm'
    #xmlFile = 'edmonton.osm'
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    conn = sql.connect('database.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON;")
    
    xmlParse(xmlFile, c, root)
    conn.commit()
    conn.close()
    
def xmlParse(xmlFile, dbConnection, treeRoot):
    
    for child in treeRoot.iter():
        # check if child element is type node
        if child.tag == 'node':
            values = (child.get('id'), child.get('lat'), child.get('lon'))
            dbConnection.execute('INSERT INTO node VALUES (?,?,?);', values)
            # find tags of nodes
            for ndtag in child:
                if ndtag.tag == 'tag':
                    values = (child.get('id'), ndtag.get('k'), ndtag.get('v'))
                    dbConnection.execute('INSERT INTO nodetag VALUES (?,?,?);', values)
        # the child is a way
        elif child.tag == 'way':
            ordinal = 0
            ndrefList = []
            values = (child.get('id'), '0')
            dbConnection.execute('INSERT INTO way VALUES (?,?);', values)
            for ndref in child.iter(): 
                #find waypoints of ways
                if ndref.tag == 'nd':
                    values = [child.get('id'), ordinal, ndref.get('ref')]
                    
                    # If foreign key constraint failed do not add
                    # eg if the node in a way doesnt exist already
                    try:
                        dbConnection.execute('INSERT INTO waypoint VALUES (?,?,?);', values)
                        ndrefList.append(ndref.get('ref'))
                        ordinal += 1                         
                    except:
                        pass
                           
                #check for tags of ways
                elif ndref.tag == 'tag':
                    values = (child.get('id'), ndref.get('k'), ndtag.get('v'))
                    dbConnection.execute('INSERT INTO waytag VALUES (?,?,?);', values)  
            # check if the way is closed
            if ndrefList[0] == ndrefList[len(ndrefList)-1]:

                values = [1, child.get('id')] 
                dbConnection.execute('UPDATE way SET closed=? WHERE id=?;', values)
main() 

