-- way id, ordinal, nodeid
--INSERT INTO waypoint VALUES (4734674, 4, 5296018936);
--SELECT id FROM NODE WHERE id = 5296018936;

-- 160144888
SELECT nodeid FROM waypoint WHERE ordinal = 0 AND wayid = 160144888;
SELECT max(ordinal) FROM waypoint WHERE 160144888 = wayid;