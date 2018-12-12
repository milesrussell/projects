
# coding: utf-8

# In[1]:


# loading in packages and data queried from CBA database
import pandas as pd
from pandasql import sqldf
import statsmodels.api as sm
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go

init_notebook_mode(connected=True)

pysqldf = lambda q: sqldf(q, globals())

df10 = pd.read_csv('~/projects/NFL Five Factors/plays_in_drives_10.csv', header=0)
df11 = pd.read_csv('~/projects/NFL Five Factors/plays_in_drives_11.csv', header=0)
df12 = pd.read_csv('~/projects/NFL Five Factors/plays_in_drives_12.csv', header=0)
df13 = pd.read_csv('~/projects/NFL Five Factors/plays_in_drives_13.csv', header=0)
df14 = pd.read_csv('~/projects/NFL Five Factors/plays_in_drives_14.csv', header=0)
df15 = pd.read_csv('~/projects/NFL Five Factors/plays_in_drives_15.csv', header=0)

turnovers = pd.read_csv('~/projects/NFL Five Factors/turnovers.csv', header=0)
position = pd.read_csv('~/projects/NFL Five Factors/field_position.csv', header=0)
home = pd.read_csv('~/projects/NFL Five Factors/home.csv', header=0)
visiting = pd.read_csv('~/projects/NFL Five Factors/visiting.csv', header=0)

frames = [df10, df11, df12, df13, df14, df15]

df = pd.concat(frames, ignore_index = True)


# In[2]:


# cleaning
plays = df.fillna(method='ffill')
plays['reverse_play_number_in_drive'] = plays.sort_values(['play_number_in_drive'], ascending = [False]).groupby(['game_id','team','drive_id']).cumcount() + 1
plays['drive_id'].astype('int32')


# In[3]:


# this query finds the number of points scored in each drive
q = """
SELECT points_scored,
       drive_id
FROM plays
WHERE reverse_play_number_in_drive = 1
"""

drivepoints = pysqldf(q)


# In[4]:


# this query finds the number of points scored per scoring opportunity
q2 = """
SELECT game_id,
       team,
       AVG(points_scored) AS points_per_trip_inside_forty,
       season
FROM (
        SELECT DISTINCT
               p.game_id,
               p.team,
               p.drive_id,
               p.season,
               CASE WHEN p.yardline >= 60 THEN 1
                    ELSE 0
                    END AS scoring_zone,
               p.points_scored

        FROM plays p
        JOIN
            (SELECT game_id,
                    drive_id,
                    team,
                    points_scored
             FROM plays
             WHERE reverse_play_number_in_drive = 1) a ON a.game_id = p.game_id
                                                      AND a.drive_id = p.drive_id
                                                      AND a.team = p.team
        WHERE scoring_zone = 1)

GROUP BY game_id,
         team,
         season
"""

ppo = pysqldf(q2)


# In[5]:


# this query finds the expected points of a drive by down, distance, and yardline
q3 = """
SELECT p.down,
       p.distance,
       p.yardline,
       AVG(d.points_scored) AS exp_points,
       count(*)
FROM plays p
JOIN drivepoints d ON d.drive_id = p.drive_id
GROUP BY p.down,
         p.distance, 
         p.yardline
"""

lookup = pysqldf(q3)


# In[6]:


# this query finds the expected points for each play

q4 = """
SELECT p.team,
       p.game_id,
       p.play_number_in_drive,
       p.drive_id,
       p.points_scored,
       l.exp_points
FROM plays p
JOIN lookup l ON l.down = p.down
             AND l.distance = p.distance
             AND l.yardline = p.yardline

"""

expected = pysqldf(q4)


# In[7]:


# this query success rate by team and game

q5 = """
SELECT s.team,
       s.game_id,
       AVG(s.success) AS success_rate
FROM
(SELECT e.team,
       e.game_id,
       e.play_number_in_drive,
       e.drive_id,
       e.exp_points,
       e2.exp_points AS next_exp_points,
       CASE WHEN e.points_scored > 0 THEN 1
            WHEN e.exp_points <= e2.exp_points THEN 1
            ELSE 0
       END AS success
FROM expected e
LEFT JOIN expected e2 ON e.drive_id = e2.drive_id
                  AND e.play_number_in_drive = (e2.play_number_in_drive - 1)) s
GROUP BY s.team,
         s.game_id
"""

success = pysqldf(q5)


# In[8]:


# this query finds average gained expected points on successful plays

q6 = """
SELECT s.team,
       s.game_id,
       AVG((CASE WHEN s.points_scored > 0 THEN points_scored ELSE s.next_exp_points END) - s.exp_points) AS explosiveness
FROM
(SELECT e.team,
       e.game_id,
       e.play_number_in_drive,
       e.drive_id,
       e.points_scored,
       e.exp_points,
       e2.exp_points AS next_exp_points,
       CASE WHEN e.points_scored > 0 THEN 1
            WHEN e.exp_points <= e2.exp_points THEN 1
            ELSE 0
       END AS success
FROM expected e
LEFT JOIN expected e2 ON e.drive_id = e2.drive_id
                  AND e.play_number_in_drive = (e2.play_number_in_drive - 1)) s
WHERE s.success = 1
GROUP BY s.team,
         s.game_id
"""

explode = pysqldf(q6)


# In[9]:


# this query brings all of the data together, ready for analysis

q7 = """
SELECT s.team,
       s.game_id,
       s.success_rate - s2.success_rate AS suc_margin,
       e.explosiveness - e2.explosiveness AS expl_margin,
       ppo.points_per_trip_inside_forty - ppo2.points_per_trip_inside_forty AS ppo_margin,
       t.turnover_diff AS turn_margin,
       p.average_starting_field_position - p2.average_starting_field_position AS pos_margin,
       COALESCE(h.win, v.win) AS win,
       ppo.season
       
FROM success s
JOIN success s2 ON s.team != s2.team AND s.game_id = s2.game_id

JOIN ppo ON ppo.team = s.team AND ppo.game_id = s.game_id
JOIN ppo ppo2 ON ppo2.team != s.team AND ppo2.game_id = s.game_id

JOIN explode e ON e.team = s.team AND e.game_id = s.game_id
JOIN explode e2 ON e2.team != s.team AND e2.game_id = s.game_id


JOIN turnovers t ON t.team = s.team AND t.game_id = s.game_id

JOIN position p ON p.team = s.team AND p.game_id = s.game_id
JOIN position p2 ON p2.team != s.team AND p2.game_id = s.game_id


LEFT JOIN home h ON h.home_team = s.team AND h.game_id = s.game_id
LEFT JOIN visiting v ON v.visiting_team = s.team AND v.game_id = s.game_id 

WHERE COALESCE(h.win, v.win) IS NOT NULL
"""

data = pysqldf(q7)

final = data.set_index(['game_id', 'team'])

# making test and train set
train = final[final['season'] != 2015]
test = final[final['season'] == 2015]

ytrain = train['win']
xtrain = train[['suc_margin','expl_margin','ppo_margin','turn_margin','pos_margin']]
ytest = test['win']
xtest = test[['suc_margin','expl_margin','ppo_margin','turn_margin','pos_margin']]


# In[10]:


# fitting a logit
model = sm.Logit(ytrain, xtrain)
reg = model.fit()
print(reg.summary())


# In[11]:


# getting logit marginal effects
mEff = reg.get_margeff(at = 'overall', method = 'eydx')
mEff.summary()


# In[12]:


# generating predictions on test data
pred = pd.DataFrame({'probability':reg.predict(xtest)})
predictions = pred.reset_index()


# In[13]:


# making a dataframe of actual wins and win probability
q8 = """
SELECT d.game_id,
       d.team,
       p.probability
FROM data d
JOIN predictions p ON p.game_id = d.game_id AND d.team = p.team
WHERE d.win = 1
"""

example2 = pysqldf(q8)


# In[14]:


# making a dataframe of of each game and win probability
q9 = """
SELECT d.game_id,
       e.team AS winner,
       d.team AS loser,
       e.probability
FROM example2 e
JOIN data d ON d.team != e.team AND e.game_id = d.game_id
ORDER BY e.probability ASC
"""

e = pysqldf(q9)
e


# In[15]:


# distribution of win probabilities
data = [go.Histogram(
                x = example2.probability, 
                nbinsx = 30)]
layout = go.Layout(
    title = "Distribution of win probabilities for actual wins",
    yaxis = dict(title = 'Count'),
    xaxis = dict(title = 'Win Probability'),
    bargap = 0.05)

fig = go.Figure(data = data, layout = layout)

iplot(fig)


# In[16]:


# comparing wins to second order wins
q10 = """
SELECT team,
       wins,
       second_order_wins,
       wins - second_order_wins AS win_diff
FROM
    (SELECT d.team,
           SUM(d.win) AS wins,
           SUM(p.probability) AS second_order_wins
    FROM final d
    JOIN predictions p ON p.game_id = d.game_id AND d.team = p.team
    GROUP BY d.team)
    
ORDER BY win_diff
"""

d = pysqldf(q10)
d


# In[17]:


# differences between wins and second order wins
data = [go.Histogram(
                x = d.win_diff, 
                xbins = dict(size = 0.5))]
layout = go.Layout(
    title = "Differences between wins and second order wins",
    yaxis = dict(title = 'Count of Teams'),
    xaxis = dict(title = 'Difference'),
    bargap = 0.1)

fig = go.Figure(data = data, layout = layout)

iplot(fig)


# In[18]:


# 1st and 10 from every yardline
example = lookup[(lookup['down'] == 1) & (lookup['distance'] == 10)]
example.head()


# In[19]:


# scatter of expected points 1st and 10
trace = go.Scatter(x = example.yardline, 
                   y = example.exp_points, 
                   mode = 'lines+markers',
                   name = 'Expected Points')

layout = go.Layout(
    title = "Expected Points for 1st and 10",
    yaxis = dict(title = 'Exp Points'),
    xaxis = dict(title = 'Yards from own goal'))

data = [trace]

fig = go.Figure(data = data, layout = layout)

iplot(fig)


# In[20]:


f = e[e['winner'] == 'ARI']
f


# In[21]:


g = e[e['loser'] == 'SEA']
g

