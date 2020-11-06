import torch
from torchvision import transforms
from torch.utils.data import Dataset

import os
import numpy as np
import pandas as pd
import random
import pickle

class StockDataset(Dataset):
    def __init__(self, args):
        self.args = args

        if os.path.isfile('data/data.pkl'):
            with open('data/data.pkl', 'rb') as f:
                self.data = pickle.load(f)
        else:
            trade = pd.read_csv('data/trade_train.csv')
            stocks = pd.read_csv('data/stocks.csv')
            pidak = pd.read_csv('data/KospiKosdaq.csv')
            large_class = pd.read_csv('data/large_class.csv', encoding='CP949')
            medium_class = pd.read_csv('data/medium_class.csv', encoding='CP949')
            small_class = pd.read_csv('data/small_class.csv', encoding='CP949')

            # print(stocks['기준일자'])
            share = pd.unique(stocks['종목번호'])
            group = pd.unique(trade['그룹번호'])
            print(share, group)
            
            df = trade.copy()
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

            ans_month = {}
            # for data in ret:
            #     tup_id = data.pop(0)[0]
            #     data.pop(0)
            #     ans_month[tup_id] = data
            col = ['sell', 'buy']
            for data in ret:
                tup_id = data.pop(0)[0]
                # cdf = pd.DataFrame(data, columns=col)
                ans_month[tup_id] = data
                #print(cdf)

            # for tup_id in ans_month:
            #     print(tup_id)
            #     print(ans_month[tup_id])


            sdf = stocks.copy()
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
                    dateToidx[date] = j
                    idxTodate[j] = date
                    j += 1

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
                ans[stock_id] = data[:-4]

            self.data = []
            for i in range(len(group)):
                group_pidak = pidak.iloc[i][1]  
                for j in range(len(share)):
                    group_large = large_class.iloc[i+1][stocks[stocks['종목번호']==share[j]].iloc[0]['표준산업구분코드_대분류']]
                    group_medium = medium_class.iloc[i+1][stocks[stocks['종목번호']==share[j]].iloc[0]['표준산업구분코드_중분류']]
                    group_small = small_class.iloc[i+1][stocks[stocks['종목번호']==share[j]].iloc[0]['표준산업구분코드_소분류']]
                    group_info = [group_pidak, group_large, group_medium, group_small]
                    group_info = torch.tensor(group_info).float().to(self.args.device)
                    try:
                        month_info = ans_month[(group[i],share[j])]
                    except:
                        month_info = torch.zeros(12, 2)
                    month_info = torch.tensor(month_info).float().to(self.args.device)
                    day_info = ans[share[j]]
                    day_info = torch.tensor(day_info).float().to(self.args.device).view(11, -1, 2)
                    self.data.append((group_info, month_info[:11], day_info, month_info[1:,1:]))

            with open('data/data.pkl', 'wb') as f:
                pickle.dump(self.data, f)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):        
        return self.data[i]

class StockLoader(object):
    def __init__(self, args):
        super().__init__()

        dataset = StockDataset(args)

        if args.mode == 'train':
            self.data_loader = torch.utils.data.DataLoader(
                dataset, batch_size=args.batch_size, shuffle=True)
        else:
            self.data_loader = torch.utils.data.DataLoader(
                dataset, batch_size=args.batch_size)

        self.data_iter = self.data_loader.__iter__()

    def next_batch(self):
        try:
            batch = self.data_iter.__next__()
        except StopIteration:
            self.data_iter = self.data_loader.__iter__()
            batch = self.data_iter.__next__()

        return batch


if __name__ == '__main__':
    from args import get_args 
    args = get_args()

    loader = StockLoader(args)

    a, b, c = loader.next_batch()
    print(a.shape, b.shape, c.shape)