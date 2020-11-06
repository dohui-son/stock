# 전월매도고객수/그룹고객수, 전월매수고객수/그룹고객수 상관관계

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

df = pd.read_csv('./trade_train.csv', encoding='CP949')
df.columns = ['blank', 'month', 'group_id', 'client_num', 
'stock_id', 'is_buy', 'is_sell', 'buy_client_num', 'sell_client_num', 
'averge_buy_num', 'average_sell_num', 'median_buy_num', 'median_sell_num']

idToidx = {}
idxToid = {}
dateToidx = {}
idxTodate = {}
i = 0
j = 1
for idx in df.index:
	month = df['month'][idx]
	group_id = df['group_id'][idx]
	stock_id = df['stock_id'][idx]

	if not (group_id, stock_id) in idToidx:
		idToidx[(group_id, stock_id)] = i
		idxToid[i] = (group_id, stock_id)
		i += 1
	if not month in dateToidx:
		dateToidx[month] = j
		idxTodate[j] = month
		j += 1

#print(i)
#print(j)
ret = []
for index1 in range(0, i):
	ret.append([[idxToid[index1], index1]])
	for index2 in range(1, j):
		ret[-1].append([0, 0])

#print(ret)

for idx in df.index:
	month = df['month'][idx]
	group_id = df['group_id'][idx]
	stock_id = df['stock_id'][idx]
	client_num = df['client_num'][idx]
	buy_client_num = df['buy_client_num'][idx]
	sell_client_num = df['sell_client_num'][idx]

	ret[idToidx[(group_id, stock_id)]][dateToidx[month]][0] = 1.0 * sell_client_num / client_num
	ret[idToidx[(group_id, stock_id)]][dateToidx[month]][1] = 1.0 * buy_client_num / client_num

col = ['sell', 'buy']
ans = {}

for data in ret:
	tup_id = data.pop(0)[0]
	data.pop(0)
	cdf = pd.DataFrame(data, columns=col)
	ans[tup_id] = cdf
	#print(cdf)

for tup_id in ans:
	print(tup_id)
	print(ans[tup_id])