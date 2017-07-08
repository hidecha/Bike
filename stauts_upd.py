# statusデータの前処理
# weather_upd.py を先に実行

import pandas as pd
from datetime import datetime as dt
import os

base_dir = os.getenv('HOME') + '/PycharmProjects/Bike'
data_dir = base_dir + '/data'
out_dir = base_dir + '/output'

# ステータスデータ読み込み
s1_df = pd.read_csv(data_dir + '/201402_status_data.csv', parse_dates=['time'])
s2_df = pd.read_csv(data_dir + '/201408_status_data.csv', parse_dates=['time'])
s3_df = pd.read_csv(data_dir + '/201508_status_data.csv', parse_dates=['time'])
s4_df = pd.read_csv(data_dir + '/201608_status_data.csv', parse_dates=['time'])

# ステータスデータ結合
ss_df = pd.concat([s1_df, s2_df, s3_df, s4_df])

# 年を追加
ss_df['year'] = ss_df['time'].map(lambda x: x.year)

# 第何週を追加
ss_df['isoweek'] = ss_df['time'].map(lambda x: dt.isocalendar(x)[1])

# 曜日を追加
ss_df['weekday'] = ss_df['time'].map(lambda x: x.isoweekday())

# 時刻を追加
ss_df['hour'] = ss_df['time'].map(lambda x: x.hour)
ss_df['min'] = ss_df['time'].map(lambda x: x.minute)

# 日付 (文字型) を追加
ss_df['PDT'] = ss_df['time'].map(lambda x: dt.strftime(x, '%Y-%m-%d'))

# ステーションデータ
sn_df = pd.read_csv(data_dir + '/201608_station_data.csv')

# 天気データ
wr_df = pd.read_csv(data_dir + '/ALL_weather_data.csv', parse_dates=['PDT']).ix[:,
        ['PDT', 'Mean_Temperature_C', 'Mean_Humidity', 'Mean_Wind_Speed_MPH', 'Sunny', 'city']]

# ステータスと天気を結合するため日付を文字型に変換
wr_df['PDT'] = wr_df['PDT'].map(lambda x: dt.strftime(x, '%Y-%m-%d'))

# 都市ごとのステータス
cities = ['San Jose', 'San Francisco', 'Palo Alto', 'Mountain View']
for city in cities:
    sn_list = list(sn_df[sn_df['landmark'] == city]['station_id'])
    ss_df_p = ss_df[ss_df['station_id'].isin(sn_list)]

    # 天気データを結合
    wr_df_p = wr_df[wr_df['city'] == city]
    ss_wr_df = pd.merge(ss_df_p, wr_df_p, on=['PDT'], how='left')
    ss_wr_df_out = ss_wr_df.ix[:, ['station_id', 'bikes_available', 'docks_available', 'year', 'isoweek', 'weekday',
                        'hour', 'min', 'PDT', 'Mean_Temperature_C', 'Mean_Humidity', 'Mean_Wind_Speed_MPH', 'Sunny']]
    ss_wr_df_out.to_csv(data_dir + '/ALL_status_' + city + '_upd.csv')

print('Done!')
