# Project 3 README:

### Question 1: 
Assumptions: 
* We are using Edmonton data, therefore use the constants: 67,137 and 111,286 for longitude and latitude respectively.
* unit1.sql is a valid db with respect to unit 1.

Go to the proper directory, and then write into terminal: 

    cp unit1.sql unit3q1.sql
    python q1.py unit1.sql > q1_output
    sqlite3 unit3q1.sql < q1_output

### Question 2:
Go to the proper directory, and then write into terminal: 
 
    cp unit3q1.sql unit3q2.sql
    python q2.py unit3q1.sql > q2_output
    sqlite3 unit3q2.sql < q2_output

### Question 3:

* Go to the proper directory 
* Create two database copies of unit3q2.sql and name them unit3q3_btree.sql, and unit3q3_rtree.sql
* Open SQL and read each database, copying the SQL commands from q3.md into their respective databases

### Question 4:
Assumption: 
* We do not count the time it takes to check if a rectangle for q4 is valid 

Go to the proper directory, and then write into terminal: 
 
    python q4.py unit3q3_btree.sql 25 100
    python q4.py unit3q3_btree.sql 50 100
    python q4.py unit3q3_btree.sql 75 100
    python q4.py unit3q3_btree.sql 100 100
    python q4.py unit3q3_btree.sql 125 100
    python q4.py unit3q3_rtree.sql 25 100
    python q4.py unit3q3_rtree.sql 50 100
    python q4.py unit3q3_rtree.sql 75 100
    python q4.py unit3q3_rtree.sql 100 100
    python q4.py unit3q3_rtree.sql 125 100
    
Record the values into a file named q4.md

### Question 5:
Assumption:
* Assuming the rtree node id's do not conflict with the db nodeids
* (We hardcode a safe value to differentiate between rtree nodes and mbrs)

Go to the proper directory, and then write into terminal: 
    
    python q5.py unit3q3_rtree.sql <x> <y> <k> 

 
 
