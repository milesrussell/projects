/*
This query returns the gameid, the visiting team, and whether the visiting team won.
*/
SELECT gid AS game_id,
       v AS visiting_team,
       CASE WHEN ptsv > ptsh THEN 1 ELSE 0 END AS win
FROM game
WHERE seas BETWEEN 2010 AND 2015
 AND ptsh - ptsv != 0;
