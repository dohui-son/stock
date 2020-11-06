#고객그룹별 대분류 종목 매수 추이

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

df = pd.read_csv('./trade_train.csv', encoding='CP949')
df.columns = ['blank', 'month', 'group_id', 'client_num', 
'stock_id', 'is_buy', 'is_sell', 'buy_client_num', 'sell_client_num', 
'averge_buy_num', 'average_sell_num', 'median_buy_num', 'median_sell_num']

sdf = pd.read_csv('./stocks.csv', encoding='CP949')
sdf.columns = ['index', 'date', 'stock_id', 'stock_name', 'iscandidate',
'type', 'kind_large', 'kind_mid', 'kind_small', 'start_price', 'high_price',
'low_price', 'end_price', 'trade_size', 'trade_price']


stockTokind = {}
kindToindex = {}

i = 0
for idx in sdf.index:
    stock_id = sdf['stock_id'][idx]
    kind_large = sdf['kind_large'][idx]

    if not stock_id in stockTokind:
        stockTokind[stock_id] = kind_large

        if not kind_large in kindToindex:
            kindToindex[kind_large] = i
            i += 1

f = open('kind.csv', 'wt', encoding='CP949', newline='')
writer = csv.writer(f)
for kind_large in kindToindex:
    writer.writerow((kind_large, kindToindex[kind_large]))

print('done')

num = 0
gid_dict = {}
for idx in df.index:
    month = df['month'][idx]
    group_id = df['group_id'][idx]
    stock_id = df['stock_id'][idx]
    buy_client_num = df['buy_client_num'][idx]

    if not stock_id in stockTokind:
        continue

    if not group_id in gid_dict:
        gid_dict[group_id] = [[month, kindToindex[stockTokind[stock_id]], buy_client_num]]
    else:
        gid_dict[group_id].append([month, kindToindex[stockTokind[stock_id]], buy_client_num])


z = [idx for idx in range(0, i)]

for group_id in gid_dict:
    print(group_id)
    month_dict = {}
    prev = -1
    for row in gid_dict[group_id]:
        month = row[0]
        if prev == -1 or prev != month:
            month_dict[month] = [row]
            prev = month
        else:
            month_dict[month].append(row)

    cdf = pd.DataFrame(columns=z)
    for month in month_dict:
        numOfclient = [0 for idx in range(0, i)]
        for data in month_dict[month]:
            numOfclient[data[1]] += data[2]
        cdf = cdf.append(pd.DataFrame([numOfclient], columns=z), ignore_index=True)

    print(cdf)
    fig = cdf.plot(y=z, use_index=True).get_figure()
    path = './kind_large_fig/' + group_id + '.png'
    fig.savefig(path)

