# Project 2 README:
**Assumptions**
1. Assuming we are given a db
2. Assuming the db at least has tables initialized for q5 and q6
3. Q6 will abort if lines arent formatted correctly
4. Q6 will NOT abort if duplicate tags are found, and will instead let you know duplicates
were found and keep going

Question 1. Distance formula for part 1 is spherical earth projected to plane. We chose this method 
because it is still fairly accurate for shorter distances, but
remains more accurate for much larger distances
 * the mean latitude is also applied in radians, as it is ambiguous whether or not it is required
 
**How to run**
1. python3 q1.py [.db file] [node1] [node2]
2. python3 q2.py [.db file] [key=value] ... [key=value]
3. python3 q3.py [.db file] [wayid]
4. python3 q4.py [.db file] [key=value] ... [key=value]
5. python3 q5.py [.db file] [.tsv file]
6. python3 q6.py [.db file] [.tsv file]
