/*
This query pulls the average starting field position for each team in each game.
*/

SELECT gid AS game_id,
       tname AS team,
       AVG(yfog) AS average_starting_field_position
FROM drive
GROUP BY gid,
         tname
