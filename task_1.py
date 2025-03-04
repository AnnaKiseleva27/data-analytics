import pandas as pd
import numpy as np

# Load the data from the provided link
link = 'https://storage.yandexcloud.net/lms-itmo-ru-files-27a87tyf/Data_storage_and_processing/Ind_1/task1_v3_5_891434.csv'
df = pd.read_csv(link)
column_of_interest = df.columns[df.isin(['00:00:00']).any()][0]
#print(column_of_interest)
df_new0 = df.loc[df[column_of_interest].isin(['00:00:00'])]

indexes = df_new0.index.to_list()
index_min = min(indexes) - 1
#print(index_min)
index_max = max(indexes) +1
#print(index_max)
df_new = df.loc[index_min:index_max].copy()

type(df_new[column_of_interest].iloc[-1])
columns_to_convert = ['Рейс 1', 'Рейс 2', 'Рейс 3', 'Рейс 4']
df_new[columns_to_convert] = df_new[columns_to_convert].apply(pd.to_timedelta)

сolumns_to_diff = ['Рейс 1', 'Рейс 2', 'Рейс 4']
df_new[[f'Длительность прохождения интервалов {col}' for col in сolumns_to_diff]] = df_new[сolumns_to_diff].diff()

df_new['cумма средн длит'] = df_new.iloc[:, [5, 6, 7]].mean(axis=1)

interval = df_new[column_of_interest].iloc[-1] -  df_new[column_of_interest].iloc[-1 - (index_max-index_min)]
#print(interval)
interval_sum = df_new.loc[:,'cумма средн длит'].sum()
#print(interval_sum)
ceof = interval/interval_sum
df_new['длит рейс 2'] = df_new['cумма средн длит']*ceof

for i  in range(5, 10):
  df_new.loc[i, column_of_interest] = (
      df_new.loc[i-1, column_of_interest] +
      df_new.loc[i, 'длит рейс 2']
  )
print(df_new[column_of_interest][1:6])
