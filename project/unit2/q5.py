import sqlite3 as sql
import sys

def parseTsv(file):
    file = open(file, 'r')
    file = file.read()
    file = file.splitlines()
    file2 = []

    for line in file:
        l = line.split('\t')
        file2.append(l)

    return file2

def insertValues(conn, values):

    c = conn.cursor()

    for row in values:
        # If row has less than 3 values skip it, no error
        if len(row) < 3:
            continue

        # Ensure that at least the first 3 values are integers
        if len(row[0]) == 0 or len(row[1]) == 0 or len(row[2]) == 0:
            print(row[0], row[1], row[2], "are invalid node data, continuing to next node")
            continue
        try:
            test = int(row[0])
            test = int(row[1])
            test = int(row[2])
        except:
            print("id, lat, lon must be integers, continuing to next node")
            continue

        # Ensure it doesnt try to add an existing node, or catch if it does
        try:
            c.execute("INSERT INTO node VALUES (?, ?, ?);",row[:3])
        except:
            print("Trying to add a node that already exists!")
            # do not continue as it may have new tags that are relevant

        # If a row has more than 3 values, we must insert the following values into nodetag
        tags = row[3:]
        for tag in tags:

            # This is just in case we have null tags
            if tag == '':
                continue

            # Ensure the tag is in the proper format
            # Do this by making sure it is at least 3 characters long, and contains =
            # somewhere that is not the first and last character
            if len(tag.strip()) < 3 or "=" not in tag or (tag[0] == '=' or tag[-1] == '='):
                print(tag, "is an invalid tag")
                continue

            tag = tag.split("=",1)
            # Same idea, check to make sure its not adding into a node that doesnt exist, or the tag doesnt already exist
            # We could just lazily use a try/except statement if we really wanted
            # Ok, there are no triggers that prevent a duplicate key/value pair from being added
            # We could add a trigger to the db or make a basic one in python here
            c.execute("SELECT count(*) FROM nodetag WHERE id = ? AND k = ? AND v = ?", [row[0], tag[0], tag[1]])
            count = c.fetchone()[0]
            if int(count) > 0:
                print("Key/Value pair already exists")
                continue
            try:
                c.execute("INSERT INTO nodetag VALUES (?, ?, ?);", [row[0], tag[0], tag[1]])
            except:
                print("Key/Value pair already exists")

    conn.commit()

def main():
    # Ensure correct number of arguments are provided
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

    conn.close()

if __name__ == '__main__':
    main()