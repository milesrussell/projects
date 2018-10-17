## This file fills in nulls from the plays_in_drives query ##

import pandas as pd

df = pd.read_csv('~/projects/NFL Five Factors/plays_in_drives.csv', header=0)
data = df.fillna(method='ffill')

data
