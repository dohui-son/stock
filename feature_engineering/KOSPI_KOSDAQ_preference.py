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


idTotype = {}
typeToindex = {}

i = 0
for idx in sdf.index:
	stock_type = sdf['type'][idx]
	stock_id = sdf['stock_id'][idx]

	if not stock_id in idTotype:
		idTotype[stock_id] = stock_type

		if not stock_type in typeToindex:
			typeToindex[stock_type] = i
			i += 1

gid_dict = {}
for idx in df.index:
	month = df['month'][idx]
	group_id = df['group_id'][idx]
	stock_id = df['stock_id'][idx]
	buy_client_num = df['buy_client_num'][idx]

	if not stock_id in idTotype:
		continue

	if not group_id in gid_dict:
		gid_dict[group_id] = [[month, stock_id, buy_client_num]]
	else:
		gid_dict[group_id].append([month, stock_id, buy_client_num])


z = ['KOSPI', 'KOSDAQ']

f = open('KospiKosdaq.csv', 'wt', encoding='utf-8', newline='')
writer = csv.writer(f)

for group_id in gid_dict:
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

		if month < 202003:
			continue

		print(month)
		stock_type = [0] * 2
		for data in month_dict[month]:
			stock_type[typeToindex[idTotype[data[1]]]] += data[2]

		cdf = cdf.append(pd.DataFrame([stock_type], columns=z), ignore_index=True)

	a = 1.0 * cdf['KOSPI'].sum()
	b = 1.0 * cdf['KOSDAQ'].sum()

	writer.writerow([group_id, a / (a + b), b / (a + b)])
