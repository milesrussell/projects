import pandas as pd
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

df = pd.read_csv('~/projects/NFL Five Factors/plays_in_drives.csv', header=0)
data = df.fillna(method='ffill')
data['reverse_dseq'] = data.sort_values(['dseq'], ascending = [False]).groupby(['game_id','team','drive_id']).cumcount() + 1

q = """
SELECT game_id,
       team,
       AVG(points_scored) AS points_per_trip_inside_forty
FROM (
        SELECT DISTINCT
               d.game_id,
               d.team,
               d.drive_id,
               CASE WHEN d.yardline >= 60 THEN 1
                    ELSE 0
                    END AS scoring_zone,
               a.points_scored

        FROM data d
        JOIN
            (SELECT game_id,
                    drive_id,
                    team,
                    points_scored
             FROM data
             WHERE reverse_dseq = 1) a ON a.game_id = d.game_id
                                      AND a.drive_id = d.drive_id
                                      AND a.team = d.team
        WHERE scoring_zone = 1)

GROUP BY game_id,
         team
"""

query = pysqldf(q)

query
