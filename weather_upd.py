# weatherデータの前処理

import pandas as pd
from datetime import datetime as dt
import os

base_dir = os.getenv('HOME') + '/PycharmProjects/Bike'
data_dir = base_dir + '/data'
out_dir = base_dir + '/output'

# 天気データ 読み込み
w1_df = pd.read_csv(data_dir + '/201402_weather_data.csv', parse_dates=['PDT'])
w2_df = pd.read_csv(data_dir + '/201408_weather_data.csv', parse_dates=['PDT'])
w3_df = pd.read_csv(data_dir + '/201508_weather_data.csv', parse_dates=['PDT'])
w4_df = pd.read_csv(data_dir + '/201608_weather_data.csv', parse_dates=['PDT'])

# 列名を統一
for w_df in [w1_df, w2_df, w3_df, w4_df]:
    w_df.columns = ['PDT', 'Max_Temperature_F', 'Mean_Temperature_F', 'Min_Temperature_F', 'Max_Dew_Point_F',
                 'Mean_Dew_Point_F', 'Min_Dew_Point_F', 'Max_Humidity', 'Mean_Humidity', 'Min_Humidity',
                 'Max_Sea_Level_Pressure_In', 'Mean_Sea_Level_Pressure_In', 'Min_Sea_Level_Pressure_In',
                 'Max_Visibility_Miles', 'Mean_Visibility_Miles', 'Min_Visibility_Miles', 'Max_Wind_Speed_MPH',
                 'Mean_Wind_Speed_MPH', 'Max_Gust_Speed_MPH', 'Precipitation_In', 'Cloud_Cover', 'Events',
                 'Wind_Dir_Degrees', 'Zip']

# 天気データの結合
wr_df = pd.concat([w1_df, w2_df, w3_df, w4_df])

# Redwoodを削除
wr_df = wr_df[wr_df.Zip != 94063]

# 年月日を追加
wr_df['year'] = wr_df['PDT'].map(lambda x: x.year)
wr_df['month'] = wr_df['PDT'].map(lambda x: x.month)
wr_df['day'] = wr_df['PDT'].map(lambda x: x.day)

# 第何週を追加
wr_df['isoweek'] = wr_df['PDT'].map(lambda x: dt.isocalendar(x)[1])

# 曜日を追加
wr_df['weekday'] = wr_df['PDT'].map(lambda x: x.isoweekday())


# 華氏を摂氏に変換
def f2c(f):
    return format((f-32)/1.8, '.2f')

wr_df['Max_Temperature_C'] = wr_df['Max_Temperature_F'].map(lambda x: f2c(x))
wr_df['Mean_Temperature_C'] = wr_df['Mean_Temperature_F'].map(lambda x: f2c(x))
wr_df['Min_Temperature_C'] = wr_df['Min_Temperature_F'].map(lambda x: f2c(x))
wr_df['Max_Dew_Point_C'] = wr_df['Max_Dew_Point_F'].map(lambda x: f2c(x))
wr_df['Mean_Dew_Point_C'] = wr_df['Mean_Dew_Point_F'].map(lambda x: f2c(x))
wr_df['Min_Dew_Point_C'] = wr_df['Min_Dew_Point_F'].map(lambda x: f2c(x))

# Events ブランク = 晴れと見なす
wr_df['Sunny'] = wr_df['Events'].map(lambda x: 1 if pd.isnull(x) else 0)

# 場所を追加
zip_dic = {94107: 'San Francisco', 94063: 'Redwood', 94301: 'Palo Alto', 94041: 'Mountain View', 95113: 'San Jose'}
wr_df['city'] = wr_df['Zip'].map(lambda x: zip_dic[x])

# CSV出力
wr_df.to_csv(data_dir + '/ALL_weather_data.csv')

print('Done!')
