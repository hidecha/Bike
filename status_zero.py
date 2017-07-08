# bikes_available, docks_available=0をステーションごとにカウント

import pandas as pd
import os

base_dir = os.getenv('HOME') + '/PycharmProjects/Bike'
data_dir = base_dir + '/data'
out_dir = base_dir + '/output'

# ステーションデータ
sn_df = pd.read_csv(data_dir + '/201608_station_data.csv')

# 都市ごとのステータス
cities = ['San Jose', 'San Francisco', 'Palo Alto', 'Mountain View']
for city in cities:
    print(city)
    ss_df = pd.read_csv(data_dir + '/ALL_status_' + city + '_upd.csv')
    for flg in ['bikes', 'docks']:
        ss_df_p = ss_df[ss_df[flg + '_available'] == 0]
        ss_df_g = ss_df_p.groupby('station_id', as_index=False)[flg + '_available'].count()
        ss_df_g.to_csv(out_dir + '/' + flg + 'Zero_' + city + '.csv')

print('Done!')
