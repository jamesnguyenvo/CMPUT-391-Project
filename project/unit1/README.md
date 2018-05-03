# Project 1 README:

Assumption: Database is empty, and named database.db file
Assumption: If a user deletes a waypoint in the middle of a path, the user cannot add more waypoints until that waypoint/ordinal pair is replaced

1. Connect to the ohaton terminal, as it greatly increases runtime
   (ssh ohaton.cs.ualberta.ca, navigate to unit1 directory)
2. Open a new terminal in unit1 directory
3. type sqlite3 and hit enter to open sqlite3
4. type .open database.db
5. type .read tables.sql
5. (OPTIONAL: type .read triggers.sql, will cause the program to take MUCH longer, use on sketchy .osm files)
6. in ohaton terminal type python3 parser.py, type your file name correctly
7. if you have not already, in your sqlite3 terminal, type .read triggers.sql after the previous step completes

NOTE: These instructions assume your .osm data is valid and final,
      like something you would download off open street maps
      That is, it assumes waypoints are not changed once closed, and
      non valid ordinal or nodes are not entered

      If you suspect your data may not be valid or contain errors and is
      not from a trusted source, there are additional triggers to apply to the
      tables to account for possible invalid data or failed constraints.

      It also adds constraints so the user can manually input data, and ensures
      the user does not violate any constraints (ie ordinal)
      

