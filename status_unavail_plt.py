import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

base_dir = os.getenv('HOME') + '/PycharmProjects/Bike'
data_dir = base_dir + '/data'
out_dir = base_dir + '/output'

sn_df = pd.read_csv(data_dir + '/201608_station_data.csv')

def station_ids(landmark):
    return list(station_data[station_data.landmark == landmark]['station_id'])

cities = ['San Jose', 'San Francisco', 'Palo Alto', 'Mountain View']
for city in cities:

    sn_list = list(sn_df[sn_df['landmark'] == city]['station_id'])

    status_data_part = pd.read_csv(data_dir + '/2016_status_' + landmark + '_upd.csv')
    few_bikes = status_data_part[status_data_part['docks_available'] == 0]

    few_bikes_pivot = pd.pivot_table(data=few_bikes, values='docks_available', columns='station_id', index='hour',
                                aggfunc='count').fillna(0)
    plt.figure(figsize=(18, 12))
    sns.heatmap(few_bikes_pivot, annot=True, fmt='g', cmap='Reds')
    plt.savefig(out_dir + '/2016_' + landmark + '_ZeroDocks.png')
    plt.close()
