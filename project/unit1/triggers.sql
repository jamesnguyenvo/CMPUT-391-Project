-- TRIGGERS


-- ADDING WAYPOINT WHEN NODE DOESNT EXIST
CREATE TRIGGER waypoint_trigger5
BEFORE INSERT ON waypoint
WHEN NEW.nodeid NOT IN (SELECT id
                     FROM NODE
                     WHERE NEW.nodeid = id)
BEGIN
SELECT RAISE(ABORT, "NODE DOES NOT EXIST");
END;                     



-- ORDINAL ALREADY EXISTS
CREATE TRIGGER waypoint_trigger3
BEFORE INSERT ON waypoint
WHEN (NEW.ordinal <= (SELECT MAX(ordinal)
                     FROM waypoint
                     WHERE NEW.wayid = wayid))
BEGIN
SELECT RAISE(ABORT, "ORDINAL ALREADY EXISTS");
END;

--ORDINAL LESS THAN 0
CREATE TRIGGER waypoint_trigger2
BEFORE INSERT ON waypoint
WHEN (NEW.ordinal < 0)        
BEGIN 
SELECT RAISE(ABORT, "ORDINAL MUST BE >= 0");
END;

-- on delete of 1 of 2 only ordinals, delete waypoint
CREATE TRIGGER waypoint_delete
AFTER DELETE ON waypoint
WHEN 1 >= (SELECT COUNT(*) FROM waypoint WHERE wayid = old.wayid)
BEGIN
DELETE FROM way WHERE old.wayid = id;
DELETE FROM waypoint WHERE old.wayid = wayid;
END;

-- on delete of ordinal 0 open way
CREATE TRIGGER waypoint_delete2
AFTER DELETE ON waypoint
WHEN 0 != (SELECT MIN(ordinal) FROM waypoint WHERE old.nodeid = nodeid)
BEGIN
UPDATE way SET closed = 0;
END;

-- on deletion of last ordinal, check if way is closed
CREATE TRIGGER waypoint_delete3
AFTER DELETE ON waypoint
WHEN old.ordinal = (SELECT MAX(ordinal) + 1 FROM waypoint WHERE old.wayid = wayid) 
AND (SELECT nodeid FROM waypoint WHERE ordinal = 0 AND old.wayid = wayid) = 
(SELECT nodeid FROM waypoint WHERE ordinal = (SELECT MAX(ordinal) FROM waypoint WHERE old.wayid = wayid) AND old.wayid = wayid)
BEGIN
UPDATE way SET closed = 1;
END;

-- on deletion of last ordinal, check if way is open
CREATE TRIGGER waypoint_delete4
AFTER DELETE ON waypoint
WHEN old.ordinal = (SELECT MAX(ordinal) + 1 FROM waypoint WHERE old.wayid = wayid) 
AND (SELECT nodeid FROM waypoint WHERE ordinal = 0 AND old.wayid = wayid) != 
(SELECT nodeid FROM waypoint WHERE ordinal = (SELECT MAX(ordinal) FROM waypoint WHERE old.wayid = wayid) AND old.wayid = wayid)
BEGIN
UPDATE way SET closed = 0;
END;

-- ensure they cannot add ordinal higher than count
-- this makes sure if 0 is deleted then 
CREATE TRIGGER waypoint_insertion3
BEFORE INSERT ON waypoint
WHEN new.ordinal > (SELECT COUNT(*) FROM waypoint WHERE wayid = new.wayid)
BEGIN
SELECT RAISE(ABORT, "MISSING ORDINAL OR ORDINAL TOO LARGE");
END;

-- Adding waypoint trigger to check if it closes the way
CREATE TRIGGER waypoint_insertion 
AFTER INSERT ON waypoint
WHEN new.nodeid IN 
(SELECT nodeid FROM waypoint WHERE ordinal = 0 AND wayid = new.wayid) 
AND new.ordinal = (SELECT max(ordinal)
                   FROM waypoint
                   WHERE new.wayid = wayid)
BEGIN
UPDATE way SET closed = 1 WHERE new.wayid = id;
END;

-- Add waypoint trigger to check if it opens the way
CREATE TRIGGER waypoint_insertion2
AFTER INSERT ON waypoint
WHEN new.nodeid NOT IN
(SELECT nodeid FROM waypoint WHERE ordinal = 0 AND wayid = new.wayid)
AND new.ordinal = (SELECT max(ordinal)
                   FROM waypoint
                   WHERE new.wayid = wayid)
BEGIN
UPDATE way SET closed = 0 WHERE new.wayid = id;
END;
