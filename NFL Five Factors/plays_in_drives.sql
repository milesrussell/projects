/*
This query pulls information needed to build an expected points lookup table.
Unfortunately, because of the design of the database, we will have to do some
additional cleaning in Python before it is ready for analysis. That cleaning can
be found in the fill_nulls.py file.
*/
SELECT p.pid AS play_id,
       p.gid AS game_id,
       p.off AS team,
       p.dseq AS play_number_in_drive,
       p.dwn AS down,
       p.ytg AS distance,
       p.yfog AS yardline,
       p.pts AS points_scored,
       d.uid AS drive_id
FROM play p
LEFT JOIN drive d ON d.fpid = p.pid
WHERE p.type NOT IN ('NOPL') --excluding non plays
  AND p.dwn != 0 --excluding kickoffs, extra point attempts, two-point conversion attempts

LIMIT 50000 --limited to 50,000 rows so that the query would finish in a reasonable time
