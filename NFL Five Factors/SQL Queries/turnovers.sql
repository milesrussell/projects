/*
This query pulls the number of turnovers for each team in each game from 2013
through 2015.
*/

SELECT team.game_id,
       team.team,
       opp.num_turnovers - team.num_turnovers AS turnover_diff
FROM
    (SELECT o.gid AS game_id,
           o.team,
           SUM(o.ints) + SUM(o.fuml) AS num_turnovers,
           g.seas AS season
    FROM offense o
    JOIN game g ON g.gid = o.gid
    WHERE g.seas BETWEEN 2013 AND 2015
    GROUP BY o.gid,
             o.team,
             g.seas) team

LEFT JOIN
    (SELECT o.gid AS game_id,
           o.team,
           SUM(o.ints) + SUM(o.fuml) AS num_turnovers,
           g.seas AS season
    FROM offense o
    JOIN game g ON g.gid = o.gid
    WHERE g.seas BETWEEN 2013 AND 2015
    GROUP BY o.gid,
             o.team,
             g.seas) opp ON team.game_id = opp.game_id
                        AND team.team != opp.team
