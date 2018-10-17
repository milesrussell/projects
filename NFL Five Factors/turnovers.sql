SELECT gid AS game_id,
       team,
       SUM(ints) + SUM(fuml) AS num_turnovers
FROM offense
GROUP BY gid,
         team
