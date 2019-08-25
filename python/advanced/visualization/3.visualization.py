#!/usr/bin/python3

import pandas as pd
df = pd.read_csv('AirPassengers.csv', index_col='id')
print(df['AirPassengers'])
print(df['time'][135])

names = ['Wade','James','Kobe','Curry']
total = [55,50,44,36]
data_set = list(zip(names,total))
data_frame = pd.DataFrame(data = data_set, column = ['Names','Total'])
data_frame.to_csv('points.csv',index = True, header = True)
