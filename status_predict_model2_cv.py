# bike_shortを目的変数とする分類予測、クロスバリデーション

import pandas as pd
from sklearn import model_selection
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
for city in cities:
    ss_df = pd.read_csv(data_dir + '/ALL_status_' + city + '_upd.csv')

    # しきい値で供給不足を分類
    ss_df['bike_availability'] = ss_df['bikes_available'] / (ss_df['bikes_available'] + ss_df['docks_available'])
    ss_df['bike_short'] = ss_df['bike_availability'].map(lambda x: 1 if x <= bs_th else 0)
    ss_df['dock_short'] = ss_df['bike_availability'].map(lambda x: 1 if x >= ds_th else 0)

    cols = ['station_id', 'type', 'model', 'score']
    score_out = pd.DataFrame(columns=cols)

    for sn_id in list(station_data[station_data['landmark'] == city]['station_id']):
        print('------------------ station_id:', int(sn_id), '------------------')
        ss_df_p = ss_df[ss_df['station_id'] == sn_id]

        ss_df_p = ss_df_p.reindex(columns=(X_cols + y_cols))

        X = ss_df_p[X_cols].fillna(0).as_matrix().astype('float')
        y = ss_df_p[y_cols].fillna(0).as_matrix().astype('int').flatten()

        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=0, test_size=0.1)

        # 標準化
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        for model in [LogisticRegression(), DecisionTreeClassifier(), KNeighborsClassifier(n_neighbors=6),
                      RandomForestClassifier()]:

            clf = model.fit(X_train, y_train)
            y_pred = clf.predict(X_test)

            # クロスバリデーション
            score_val = model_selection.cross_val_score(model, X, y, cv=5)

            print(clf.__class__.__name__)
            train_score = clf.score(X_train, y_train)
            test_score = clf.score(X_test, y_test)
            val_score = score_val.mean()
            print('train:', train_score)
            print('test:', test_score)
            print('val:', val_score)

            row_train = pd.Series([int(sn_id), 'train', clf.__class__.__name__, train_score],
                                  index=score_out.columns)
            score_out = score_out.append(row_train, ignore_index=True)
            row_test = pd.Series([int(sn_id), 'test', model.__class__.__name__, test_score],
                                 index=score_out.columns)
            score_out = score_out.append(row_test, ignore_index=True)
            row_test = pd.Series([int(sn_id), 'val', model.__class__.__name__, val_score],
                                 index=score_out.columns)
            score_out = score_out.append(row_test, ignore_index=True)

        # CSV出力
        score_out.to_csv(out_dir + '/predict_cross_val_' + city + '_ds.csv')

print('Done!')
