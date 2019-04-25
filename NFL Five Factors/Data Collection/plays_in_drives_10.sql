/*
This query pulls information needed to build an expected points lookup table.
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
WHERE p.type IN ('RUSH', 'PASS', 'FGXP')
  AND p.dwn != 0 --excluding extra point attempts
  AND g.seas = 2010;
