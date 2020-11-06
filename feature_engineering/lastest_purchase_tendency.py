import pandas as pd
import csv

df = pd.read_csv('./trade_train.csv', encoding='CP949')
df.columns = ['blank', 'month', 'group_id', 'client_num', 
'stock_id', 'is_buy', 'is_sell', 'buy_client_num', 'sell_client_num', 
'averge_buy_num', 'average_sell_num', 'median_buy_num', 'median_sell_num']

df['month'] = df['month'].astype(str)

for idx in df.index:
	month = df['month'][idx]
	df.at[idx, 'month'] = month[:4] + '-' + month[4:] + '-01'

sdf = pd.read_csv('./stocks.csv', encoding='CP949')
sdf.columns = ['index', 'date', 'stock_id', 'stock_name', 'iscandidate',
'type', 'kind_large', 'kind_mid', 'kind_small', 'start_price', 'high_price',
'low_price', 'end_price', 'trade_size', 'trade_price']


isCandidateStock = {}
for idx in sdf.index:
	iscandidate = sdf['iscandidate'][idx]
	stock_id = sdf['stock_id'][idx]
	if iscandidate == 'Y':
		isCandidateStock[stock_id] = True
	else:
		isCandidateStock[stock_id] = False

kdf = {}
month_list = [['2019-07-01', 0], ['2019-08-01', 0], ['2019-09-01', 0], ['2019-10-01', 0], 
['2019-11-01', 0], ['2019-12-01', 0], ['2020-01-01', 0], ['2020-02-01', 0], 
['2020-03-01', 0], ['2020-04-01', 0], ['2020-05-01', 0], ['2020-06-01', 0]]
for idx in df.index:
	month = df['month'][idx]
	group_id = df['group_id'][idx]
	stock_id = df['stock_id'][idx]
	buy_client_num = df['buy_client_num'][idx]
	if not (group_id, stock_id) in kdf:
		kdf[group_id, stock_id] = [[month, buy_client_num]]
	else:
		kdf[group_id, stock_id].append([month, buy_client_num])


ndf_dict = {}
for rw in kdf:
	ndf = pd.DataFrame(month_list, columns=['ds', 'y'])
	for month, buy_client_num in kdf[rw]:
		#ndf = ndf.append(pd.DataFrame({'ds': month, 'y': buy_client_num}, index=[0]), ignore_index=True)
		ndf.loc[month, 'y'] = buy_client_num

	ndf.loc[(ndf['ds'] < '2020-03-01'), 'y'] = None
	if not rw[0] in ndf_dict:
		ndf_dict[rw[0]] = [[ndf['y'].sum(), rw[1]]]
	else:
		ndf_dict[rw[0]].append([ndf['y'].sum(), rw[1]])


print('check')
ret = {}
for rw in ndf_dict:
	ndf_dict[rw].sort(reverse=True)
	ret[rw] = []
	for value, stock_id in ndf_dict[rw]:
		if isCandidateStock[stock_id] == True:
			ret[rw].append(stock_id)
		if len(ret[rw]) >= 3:
			break

f = open('output_all.csv', 'wt', encoding='utf-8', newline='')
writer = csv.writer(f)

for rw in ret:
	ret[rw].sort()
	print(ret[rw])
	print()
	row = []
	row.append(rw)
	row.append(ret[rw][0])
	row.append(ret[rw][1])
	row.append(ret[rw][2])
	
	writer.writerow(row)


'''
ndf_dict = {}
for idx in df.index:
	group_id = df['group_id'][idx]
	if not group_id in ndf_dict:
		ndf_dict[group_id] = pd.DataFrame(month_list, columns=['ds', 'y'])
'''
