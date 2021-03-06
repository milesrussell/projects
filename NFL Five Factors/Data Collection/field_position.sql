/*
This query pulls the average starting field position for each team in each game
from 2013 through 2015.
*/

SELECT d.gid AS game_id,
       d.tname AS team,
       AVG(d.yfog) AS average_starting_field_position
FROM drive d
JOIN game g ON g.gid = d.gid
WHERE g.seas BETWEEN 2010 AND 2015
GROUP BY d.gid,
         d.tname;
