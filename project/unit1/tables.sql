DROP TABLE IF EXISTS node;
DROP TABLE IF EXISTS way;
DROP TABLE IF EXISTS waypoint;
DROP TABLE IF EXISTS nodetag;
DROP TABLE IF EXISTS waytag;

CREATE TABLE node (
  id integer,
  lat float, 
  lon float,
  PRIMARY KEY(id)
);

CREATE TABLE way (
  id integer,
  closed boolean,
  PRIMARY KEY(id)
);

CREATE TABLE waypoint (
  wayid integer,
  ordinal integer,
  nodeid integer,
  FOREIGN KEY (wayid) REFERENCES way ON DELETE CASCADE,
  FOREIGN KEY (nodeid) REFERENCES node ON DELETE CASCADE
);

CREATE TABLE nodetag (
  id integer,
  k text,
  v text,
  FOREIGN KEY (id) REFERENCES node
); 

CREATE TABLE waytag (
  id integer,
  k text,
  v text,
  FOREIGN KEY (id) REFERENCES way
); 

-- Adding a waypoint where the wayid doesnt exist in the database
CREATE TRIGGER waypoint_trigger4
BEFORE INSERT ON waypoint
WHEN (NEW.wayid != (SELECT id
                   FROM way
                   WHERE NEW.wayid = id))
BEGIN
SELECT RAISE(ABORT, "WAY DOES NOT EXIST");
END;
