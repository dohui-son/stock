import torch
import torch.nn as nn
import torch.nn.functional as F

from .args import get_args
from .model import Stock
from .dataloader import StockLoader

import pandas as pd

class Trainer():
    def __init__(self, args):
        self.args = args

        self.loader = StockLoader(args)
        self.model = Stock(args)
        self.loss = nn.MSELoss()
        self.optim = torch.optim.Adam(self.model.parameters())

    def train(self):
        for epoch in range(self.args.epoch):
            for i in range(len(self.loader.data_loader)):
                group_info, month_info, day_info, label = self.loader.next_batch()
                
                pred = self.model(group_info, month_info, day_info)

                loss = self.loss(pred, label)
                loss.backward()
                self.optim.step()
            print(f'{epoch}:{loss}')
            
            torch.save(self.model.state_dict(), 'checkpoint.pt')

    def test(self):
        trade = pd.read_csv('data/trade_train.csv')
        stocks = pd.read_csv('data/stocks.csv')
        share = pd.unique(stocks['종목번호'])
        group = pd.unique(trade['그룹번호'])
        self.model.load_state_dict(torch.load(self.args.ckpt))

        csv_file = []
        pred = []
        for i in range(len(self.loader.data_loader)):
            group_info, month_info, day_info, label = self.loader.next_batch()
            pred.append(self.model(group_info, month_info, day_info)[0][-1])
            if i%1087 == 1086:
                result = torch.cat(pred, dim=0)
                result = torch.topk(result,k=3)
                csv_file.append([group[i//1087], share[result[1][0]], share[result[1][1]], share[result[1][2]]])
                pred = []

        df = pd.DataFrame(csv_file, columns=['그룹명', '종목번호1', '종목번호2', '종목번호3'])
        df.to_csv('result.csv')

        