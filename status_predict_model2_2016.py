import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

# ロジスティック回帰
from sklearn.linear_model import LogisticRegression

# 決定木
from sklearn.tree import DecisionTreeClassifier

# k-NN
from sklearn.neighbors import KNeighborsClassifier

# ランダムフォレスト
from sklearn.ensemble import RandomForestClassifier

base_dir = os.getenv('HOME') + '/PycharmProjects/Bike'
data_dir = base_dir + '/data'
out_dir = base_dir + '/output'

station_data = pd.read_csv(data_dir + '/201608_station_data.csv')

# しきい値
bs_th, ds_th = 0.15, 0.85

# 説明変数
X_cols = ['isoweek', 'weekday', 'hour', 'min', 'Sunny', 'Mean_Temperature_C', 'Mean_Wind_Speed_MPH']

# 目的変数
y_cols = ['dock_short']

# 都市ごとのステータス
cities = ['San Jose', 'San Francisco', 'Palo Alto', 'Mountain View']
#cities = ['Mountain View']
for city in cities:
    ss_df = pd.read_csv(data_dir + '/ALL_status_' + city + '_upd.csv')

    # しきい値で供給不足を分類
    ss_df['bike_availability'] = ss_df['bikes_available'] / (ss_df['bikes_available'] + ss_df['docks_available'])
    ss_df['bike_short'] = ss_df['bike_availability'].map(lambda x: 1 if x <= bs_th else 0)
    ss_df['dock_short'] = ss_df['bike_availability'].map(lambda x: 1 if x >= ds_th else 0)

    score_out = pd.DataFrame(columns=['station_id', 'type', 'model', 'score'])

    for sn_id in list(station_data[station_data['landmark'] == city]['station_id']):
        ss_df_p = ss_df[ss_df['station_id'] == sn_id]

        # 2016以外をtrainデータ, 2016をtestデータとする
        ss_df_2015 = ss_df_p[ss_df_p['year'] != 2016]

        print('------------------ station_id:', int(sn_id), '------------------')
        if len(ss_df_2015) > 0:     # 2016以外のデータがあった場合、処理を続行
            ss_df_2016 = ss_df_p[ss_df_p['year'] == 2016]
            ss_df_2015 = ss_df_2015.reindex(columns=(X_cols + y_cols))
            ss_df_2016 = ss_df_2016.reindex(columns=(X_cols + y_cols))

            X_train = ss_df_2015[X_cols].fillna(0).as_matrix().astype('float')
            X_test = ss_df_2016[X_cols].fillna(0).as_matrix().astype('int')

            y_train = ss_df_2015[y_cols].fillna(0).as_matrix().astype('float').flatten()
            y_test = ss_df_2016[y_cols].fillna(0).as_matrix().astype('int').flatten()

            # 標準化
            scaler = StandardScaler()
            scaler.fit(X_train)
            X_train = scaler.transform(X_train)
            X_test = scaler.transform(X_test)

            # モデル予測
            for model in [LogisticRegression(), DecisionTreeClassifier(), KNeighborsClassifier(n_neighbors=6),
                          RandomForestClassifier()]:
                clf = model.fit(X_train, y_train)
                y_pred = clf.predict(X_test)

                print(clf.__class__.__name__)
                train_score = clf.score(X_train, y_train)
                test_score = clf.score(X_test, y_test)
                print('train(!2016):', train_score)
                print('test(2016):', test_score)

                row_train = pd.Series([int(sn_id), 'train', clf.__class__.__name__, train_score],
                                      index=score_out.columns)
                score_out = score_out.append(row_train, ignore_index=True)
                row_test = pd.Series([int(sn_id), 'test', clf.__class__.__name__, test_score],
                                     index=score_out.columns)
                score_out = score_out.append(row_test, ignore_index=True)
        else:
            print('No 2015 data!')

    # スコア出力
    score_out.to_csv(out_dir + '/predict_2016by2015_' + city + '_ds.csv')
