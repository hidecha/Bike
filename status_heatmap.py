# statusデータを元にbike_availabilityヒートマップを描画
# status_upd.py を先に実行

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

base_dir = os.getenv('HOME') + '/PycharmProjects/Bike'
data_dir = base_dir + '/data'
out_dir = base_dir + '/output'

# ステーションデータ
sn_df = pd.read_csv(data_dir + '/201608_station_data.csv')

# 都市ごとのステータス
cities = ['San Jose', 'San Francisco', 'Palo Alto', 'Mountain View']
for city in cities:
    ss_df = pd.read_csv(data_dir + '/ALL_status_' + city + '_upd.csv')

    # 2016年平日のみ抽出
    ss_df_p = ss_df[ss_df['year'] == 2016][ss_df['weekday'] < 6]

    ss_df_p['bike_availability'] = ss_df_p['bikes_available'] / (ss_df_p['bikes_available'] + ss_df_p['docks_available'])
    ss_pv = pd.pivot_table(data=ss_df_p, values='bike_availability', columns='hour', index='station_id', aggfunc='mean')

    sn_ids = len(sn_df[sn_df['landmark'] == city])

    plt.figure(figsize=(10, sn_ids/2))
    sns.heatmap(ss_pv, fmt='g', center=0.5)
    plt.title('[' + city + '] 2016 Bike Availability')
    plt.savefig(out_dir + '/graph/2016_' + city + '_BikeAvailability_wd.png')
    plt.close()

print('Done!')
