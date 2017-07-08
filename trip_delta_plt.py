# tripデータを元にステーションごとのIn/Outグラフ化
# trip_delta_upd.py を先に実行

import pandas as pd
import os
import matplotlib.pyplot as plt

base_dir = os.getenv('HOME') + '/PycharmProjects/Bike'
data_dir = base_dir + '/data'
out_dir = base_dir + '/output'

# ステーションデータ
sn_df = pd.read_csv(data_dir + '/201608_station_data.csv')

# 時間ごとのプロット用
hours = list(range(24))

# 都市ごとのTripデータ (Start / End) 読み込み
cities = ['San Jose', 'San Francisco', 'Palo Alto', 'Mountain View']
for city in cities:
    out_df = pd.read_csv(data_dir + '/ALL_trip_' + city + '_Start.csv')
    in_df = pd.read_csv(data_dir + '/ALL_trip_' + city + '_End.csv')

    # ステーションごとのデータ読み込み
    for sn_id in list(sn_df[sn_df.landmark == city]['station_id']):
        sn_id = int(sn_id)
        print(city, sn_id)
        out_df_p = out_df[out_df['station_id'] == sn_id]
        in_df_p = in_df[in_df['station_id'] == sn_id]

        # 平日と週末でデータを分ける
        out_df_we = out_df_p[out_df_p['weekend'] == 1]
        out_df_wd = out_df_p[out_df_p['weekend'] != 1]
        in_df_we = in_df_p[in_df_p['weekend'] == 1]
        in_df_wd = in_df_p[in_df_p['weekend'] != 1]

        # 時間ごとにグループ化
        out_gp_we = out_df_we.groupby(['hour'], as_index=False)['Trip ID'].size()
        out_gp_wd = out_df_wd.groupby(['hour'], as_index=False)['Trip ID'].size()
        in_gp_we = in_df_we.groupby(['hour'], as_index=False)['Trip ID'].size()
        in_gp_wd = in_df_wd.groupby(['hour'], as_index=False)['Trip ID'].size()

        # グラフ作成
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))

        # 平日: 左
        ax1.plot(hours, out_gp_wd.loc[hours].fillna(0), '+-.', hours, in_gp_wd.loc[hours].fillna(0), 's-', linewidth=2)
        ax1.set_title('[' + city + '] ' + str(sn_id) + ' In/Out (Weekdays)')
        ax1.set_xlabel('Hours')
        ax1.set_ylabel('Trips')
        ax1.legend(['out', 'in'])
        ax1.grid(True)

        # 週末: 右
        ax2.plot(hours, out_gp_we.loc[hours].fillna(0), '+-.', hours, in_gp_we.loc[hours].fillna(0), 's-', linewidth=2)
        ax2.set_title('[' + city + '] ' + str(sn_id) + ' In/Out (Weekend)')
        ax2.set_xlabel('Hours')
        ax2.set_ylabel('Trips')
        ax2.legend(['out', 'in'])
        ax2.grid(True)

        # グラフ保存
        plt.savefig(out_dir + '/graph/ALL_' + city + '_' + str(sn_id) + '_Trip_InOut.png')
        plt.close()

print('Done!')
