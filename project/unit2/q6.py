from q5 import parseTsv
import sqlite3 as sql
import sys

# Split on consecutive lines or whatever
# First line contains the wayid and the tags associated with the way
# Second line contains at least 2 nodes to correspond to the way
# We can close the way after we finish inserting all the nodes

def insertValues(conn, tsv):
    c = conn.cursor()

    # Loop through the lines
    # When a blank line is encountered, expect one more blank line afterwards
    # When a non-blank line is encountered, expect one more non blank line afterwards
    # If these constraints are not met return -1 and make no commits? Or skip over the offending line

    blank = 0
    text = 0
    wayid = 0
    for line in tsv:
        if set(line) == {''}:
            # Make sure there wasn't just one text line
            if text == 1:
                print("File not formatted correctly, aborting changes")
                return -1

            text = 0
            blank += 1
            if blank == 3:
                print("File not formatted correctly, aborting changes")
                return -1

        else:
            # Make sure there were 2 blanks
            if blank == 1:
                print("File not formatted correctly, aborting changes")
                return -1

            # We can expect all these lines to contain at least one value
            blank = 0
            text += 1

            # The first line contains the wayid and tags
            if text == 1:
                wayid = line.pop(0)

                # Ensure wayid is a valid integer
                try:
                    test = int(wayid)

                except:
                    print(wayid, "is not a valid wayID, aborting")
                    sys.exit()

                # If the way already exists we will still add potential new tags
                # New ways will obviously be added as open
                try:
                    c.execute("INSERT INTO way VALUES (?,0)", [wayid])
                except:
                    # Continue to add the potentially new way tags
                    pass
                for tag in line:
                    # Ensure the tag is in the proper format
                    # Do this by making sure it is at least 3 characters long, and contains =
                    # somewhere that is not the first and last character
                    if len(tag.strip()) < 3 or "=" not in tag or (tag[0] == '=' or tag[-1] == '='):
                        if tag != '':
                            print(tag, "is an invalid tag")
                        continue

                    tag = tag.split("=",1)

                    # Ensure the tag doesn't already exist by querying for the tag
                    c.execute("SELECT count(*) FROM waytag WHERE id = ? AND k = ? AND v = ?", [wayid, tag[0], tag[1]])
                    count = c.fetchone()[0]
                    if int(count) > 0:
                        print(tag[0],"=",tag[1], "already exists for wayid =", wayid)
                        continue

                    # This try/except block is redundant and should be removed
                    # It exist if we rely on triggers to alert us if key/value pairs already exist
                    try:
                        c.execute("INSERT INTO waytag VALUES (?, ?, ?);", [wayid, tag[0], tag[1]])
                    except:
                        print(tag[0],"=",tag[1], "already exists for wayid =", wayid)

            # If you are on the second line, add the nodes to the way
            # First we are going to get all the nodes that already exist
            elif text == 2:
                c.execute("SELECT * FROM waypoint WHERE wayid = ?", [wayid])
                existing = c.fetchall()

                # In order to remove empty string values at the end of the line we are going to do some jank
                line2 = line[:]
                line2.reverse()
                iterLine = line2[:]
                for node in iterLine:
                    if node == '':
                        line2.remove('')
                    else:
                        line2.reverse()
                        line = line2[:]
                        break

                ordinal = 0
                for i in range(len(line)):
                    # See if and i'th index node already exists
                    # If it does then do nothing
                    # If it doesn't then add that node and ordinal to the way
                    try:
                        test = int(line[i])
                    except:
                        print(line[i], "is not a valid node, aborting")
                        sys.exit()
                    try:
                        exist = existing[i]
                    except:
                        # If node does not exist we must abort our adding of the way I guess, or break out of the loop at least

                        try:
                            c.execute("INSERT INTO waypoint VALUES (?,?,?)", [wayid, ordinal, line[i]])
                        except:
                            if line[i] == '':
                                print("Missing node value for wayid",str(wayid)+",","aborting")
                                sys.exit()
                            print("Node", line[i], "does not exist in the database, aborting")
                            sys.exit()
                    ordinal += 1

                # Finally check to see if the way should be opened or closed
                # We can do this by comparing only what is in the tsv, because if nothing is added
                # then we can assume that the way is already properly sets
                # Alternatively we could just query the entire way again and check that way
                # But that is one extra query we do not need to make
                if line[0] == line[-1]:
                    c.execute("UPDATE way SET closed = 1 WHERE id = ?", [wayid])


            # If there is a 3rd line the file is formatted incorrectly
            elif text == 3:
                print(tsv)
                print("File not formatted correctly, aborting changes")
                return -1
    conn.commit()

def main():

    if len(sys.argv) != 3:
        print("Invalid Arguments")
        sys.exit()

    database = sys.argv[1]
    tsv = sys.argv[2]
    # Check if database file at least exists
    try:
        file = open(database, 'r')
    except:
        print(database, "does not exist or could not be opened")
        sys.exit()

        # Check if database file at least exists
    try:
        file = open(tsv, 'r')
    except:
        print(tsv, "does not exist or could not be opened")
        sys.exit()

    conn = sql.connect(database)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON;")
    conn.commit()

    tsv = parseTsv(tsv)
    insertValues(conn, tsv)

if __name__ == '__main__':
    main()