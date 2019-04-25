/*
This query returns the gameid, the home team, and whether the home team won.
*/
SELECT gid AS game_id,
       h AS home_team,
       CASE WHEN ptsh > ptsv THEN 1 ELSE 0 END AS win
FROM game
WHERE seas BETWEEN 2010 AND 2015
 AND ptsh != ptsv;