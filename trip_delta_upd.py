import pandas as pd
from datetime import datetime as dt
import os

base_dir = os.getenv('HOME') + '/PycharmProjects/Bike'
data_dir = base_dir + '/data'
out_dir = base_dir + '/output'

# ステーションデータ
sn_df = pd.read_csv(data_dir + '/201608_station_data.csv')

# Tripデータ結合
print('Loading trip data...')
t1_df = pd.read_csv(data_dir + '/201402_trip_data.csv', parse_dates=['Start Date', 'End Date'], index_col=['Trip ID'])
t1_df['Subscriber Type'] = t1_df['Subscription Type']   # 201402_trip_data.csv のみフィールド名が異なるため修正
t2_df = pd.read_csv(data_dir + '/201408_trip_data.csv', parse_dates=['Start Date', 'End Date'], index_col=['Trip ID'])
t3_df = pd.read_csv(data_dir + '/201508_trip_data.csv', parse_dates=['Start Date', 'End Date'], index_col=['Trip ID'])
t4_df = pd.read_csv(data_dir + '/201608_trip_data.csv', parse_dates=['Start Date', 'End Date'], index_col=['Trip ID'])
tp_df = pd.concat([t1_df, t2_df, t3_df, t4_df])

# 都市ごとのTripデータ
cities = ['San Jose', 'San Francisco', 'Palo Alto', 'Mountain View']
for city in cities:
    # 都市のステーション一覧
    sn_list = list(sn_df[sn_df.landmark == city]['station_id'])

    # Trip Start / End データ取得
    for flg in ['Start', 'End']:
        print(city, flg)
        tp_df_p = tp_df[tp_df[flg + ' Terminal'].isin(sn_list)]

        # フィールド追加
        tp_df_p['station_id'] = tp_df_p[flg + ' Terminal']
        tp_df_p['year'] = tp_df_p[flg + ' Date'].map(lambda x: x.year)
        tp_df_p['isoweek'] = tp_df_p[flg + ' Date'].map(lambda x: dt.isocalendar(x)[1])
        tp_df_p['weekday'] = tp_df_p[flg + ' Date'].map(lambda x: x.isoweekday())
        tp_df_p['weekend'] = tp_df_p['weekday'].map(lambda x: 1 if x >= 6 else 0)
        tp_df_p['hour'] = tp_df_p[flg + ' Date'].map(lambda x: x.hour)
        tp_df_p['min'] = tp_df_p[flg + ' Date'].map(lambda x: x.minute)
        tp_df_p['PDT'] = tp_df_p[flg + ' Date'].map(lambda x: dt.date(x))
        tp_df_p['time'] = tp_df_p[flg + ' Date']

        # 必要なフィールドをCSV出力
        tp_df_out = tp_df_p.ix[:, ['station_id', 'Subscriber Type', 'year', 'isoweek', 'weekday', 'weekend', 'hour', 'min', 'PDT', 'time']]
        tp_df_out.to_csv(data_dir + '/ALL_trip_' + city + '_' + flg + '.csv')

print('Done!')
