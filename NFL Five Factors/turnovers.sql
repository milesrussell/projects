/*
This query pulls the number of turnovers for each team in each game from 2010
through 2015.
*/

SELECT o.gid AS game_id,
       o.team,
       SUM(o.ints) + SUM(o.fuml) AS num_turnovers,
       g.seas AS season
FROM offense o
JOIN game g ON g.gid = o.gid
WHERE g.seas BETWEEN 2010 AND 2015
GROUP BY o.gid,
         o.team,
         g.seas;
