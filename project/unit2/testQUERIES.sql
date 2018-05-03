--SELECT count(*) FROM nodetag, node WHERE node.id = nodetag.id AND (k = "tourism" AND v = "artwork" OR k = "crossing" AND v = "zebra");

--SELECT * from waypoint WHERE wayid=546489525;


--WITH RECURSIVE
--totalDistance(x) as (
--SELECT 1
--UNION ALL
--SELECT x+1 FROM totalDistance
--)
--SELECT x from totalDistance;

--SELECT * FROM waypoint w1, waypoint w2 WHERE w1.wayid = 546489525 AND w2.wayid = w1.wayid AND w1.ordinal = w2.ordinal+1;

-- WITH RECURSIVE
--     totalDistance(x) as
--   (SELECT ordinal from waypoint w1 WHERE wayid = 546489525
--   UNION ALL
--   SELECT ordinal from waypoint w2 WHERE wayid = 546489525 AND w1.ordinal = w2.ordinal+1)
-- SELECT x FROM totalDistance;

-- SELECT * FROM node n, waypoint w1, waypoint w2 WHERE w1.wayid = 546489525 AND w2.wayid = w1.wayid AND n.id = w1.nodeid

-- this is what we want
-- SELECT * FROM waypoint, node WHERE wayid = 546489525 AND nodeid = id
--
--
-- -- This looks promising
-- SELECT * FROM node n, waypoint w1, waypoint w2
-- WHERE w1.wayid = 546489525 AND w2.wayid = w1.wayid AND n.id = w1.nodeid AND w1.ordinal = w2.ordinal+1
--
-- -- So we want to compute distance between each of these
-- SELECT sum(ordinal) FROM waypoint, node WHERE wayid = 546489525 AND nodeid = id LIMIT 2
--
--
-- -- could we do some jank with max() ordinal and count of already computed distances???
-- SELECT ordinal + (SELECT ordinal FROM waypoint AS w2 WHERE w2.wayid = 546489525 AND waypoint.ordinal < w2.ordinal) AS os FROM waypoint
--
-- SELECT ordinal + (SELECT ordinal FROM waypoint AS w2 WHERE w2.wayid = 546489525 AND waypoint.ordinal < w2.ordinal) AS os FROM waypoint WHERE wayid = 546489525
--

WITH RECURSIVE
total(x,y) AS (
VALUES(0,0)
UNION
SELECT ordinal, ordinal+ordinal FROM waypoint, node, total WHERE wayid = 546489525 AND nodeid = id AND (ordinal = x OR ordinal = x+1)
)
SELECT sum(x) FROM total

WITH RECURSIVE
total(x,y) AS (
VALUES(0,0)
UNION
SELECT ordinal, ordinal+ordinal FROM waypoint, node, total WHERE wayid = 546489525 AND nodeid = id AND (ordinal = x OR ordinal = x+1)
)
SELECT sum(x) FROM total


-- Can we scale this up???
SELECT lat, lon FROM waypoint, node WHERE wayid = 546489525 AND nodeid = id LIMIT 0,2

--q4 test
WITH ordinals(ordinal1, ordinal2, id1, id2, wid) AS 
(SELECT w1.ordinal, w2.ordinal, w1.nodeid, w2.nodeid, wt.id 
FROM waypoint w1, waypoint w2, waytag wt
WHERE wt.id = w1.wayid AND wt.k = 'psv' AND w1.wayid=w2.wayid AND w2.ordinal = w1.ordinal + 1) 
SELECT ordinal1
FROM ordinals JOIN node n1, node n2 ON n1.id = ordinals.id1 AND n2.id = ordinals.id2;
