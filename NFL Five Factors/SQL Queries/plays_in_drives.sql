/*
This query pulls information needed to build an expected points lookup table.
Unfortunately, because of the design of the database, we will have to do some
additional cleaning in Python before it is ready for analysis. That cleaning can
be found in the fill_nulls.py file. We only pull data on plays from 2013 through
2015.
*/

SELECT p.pid AS play_id,
       p.gid AS game_id,
       p.off AS team,
       p.dseq AS play_number_in_drive,
       p.dwn AS down,
       p.ytg AS distance,
       p.yfog AS yardline,
       p.pts AS points_scored,
       d.uid AS drive_id,
       g.seas AS season
FROM play p
LEFT JOIN drive d ON d.fpid = p.pid
JOIN game g ON g.gid = p.gid
WHERE p.type NOT IN ('NOPL') --excluding non plays
  AND p.dwn != 0 --excluding kickoffs, extra point attempts, two-point conversion attempts
  AND g.seas BETWEEN 2013 AND 2015
  AND p.dseq != 0; --getting rid of punts
