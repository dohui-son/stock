#(종목종가 - 종목시가)/종목종가, (종목고가 - 종목저가)/종목고가

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

sdf = pd.read_csv('./stocks.csv', encoding='CP949')
sdf.columns = ['index', 'date', 'stock_id', 'stock_name', 'iscandidate',
'type', 'kind_large', 'kind_mid', 'kind_small', 'start_price', 'high_price',
'low_price', 'end_price', 'trade_size', 'trade_price']


idToidx = {}
idxToid = {}
dateToidx = {}
idxTodate = {}
i = 0
j = 1
for idx in sdf.index:
	date = sdf['date'][idx]
	stock_id = sdf['stock_id'][idx]
	high_price = sdf['high_price'][idx]
	end_price = sdf['end_price'][idx]

	if not stock_id in idToidx:
		idToidx[stock_id] = i
		idxToid[i] = stock_id
		i += 1
	if not date in dateToidx:
		dateToidx[date] = j;
		idxTodate[j] = date;
		j += 1

#print(i)
#print(j)
ret = []
for index1 in range(0, i):
	ret.append([[idxToid[index1], index1]])
	for index2 in range(1, j):
		ret[-1].append([0, 0])

for idx in sdf.index:
	date = sdf['date'][idx]
	stock_id = sdf['stock_id'][idx]
	start_price = sdf['start_price'][idx]
	high_price = sdf['high_price'][idx]
	low_price = sdf['low_price'][idx]
	end_price = sdf['end_price'][idx]

	a = 0
	b = 0
	if end_price != 0:
		a = (1.0 * end_price - start_price) / end_price
	if high_price != 0:
		b = (1.0 * high_price - low_price) / high_price

	#ret[idToidx[stock_id]].append([date, a, b])
	ret[idToidx[stock_id]][dateToidx[date]][0] = a
	ret[idToidx[stock_id]][dateToidx[date]][1] = b

col = ['end', 'high']
ans = {}

for data in ret:
	stock_id = data.pop(0)[0]
	cdf = pd.DataFrame(data, columns=col)
	ans[stock_id] = cdf
	#print(cdf)

for stock_id in ans:
	print(stock_id)
	print(ans[stock_id])