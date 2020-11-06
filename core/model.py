import torch
import torch.nn as nn
import torch.nn.functional as F

class Stock(nn.Module):
    def __init__(self, args, day_hidden_size=10, mon_hidden_size=20):
        super().__init__()

        self.args = args
        self.day_hidden_size = day_hidden_size
        self.mon_hidden_size = mon_hidden_size

        self.price = nn.RNN(2, self.day_hidden_size)
        self.group = nn.Sequential(
            nn.Linear(4, self.mon_hidden_size),
            nn.ReLU(),
        )
        self.person_cnt = nn.RNN(2 + self.day_hidden_size, self.mon_hidden_size)
        self.final = nn.Linear(self.mon_hidden_size, 1)

    def forward(self, group_info, month_info, day_info):
        month_info = month_info.permute(1, 0, 2)
        day_info = day_info.permute(1, 2, 0, 3)

        day_embedding = []
        for i in range(month_info.shape[0]):
            tmp = torch.randn(1, group_info.shape[0], self.day_hidden_size).to(self.args.device)
            day_embedding.append(self.price(day_info[i], tmp)[0][-1])
        day_embedding = torch.stack(day_embedding)

        month_info = torch.cat([month_info, day_embedding], dim=2)
        group_info = self.group(group_info).unsqueeze(0)

        person = self.person_cnt(month_info, group_info)[0]
        person = self.final(person).permute(1,0,2)
        return person


if __name__ == '__main__':
    from args import get_args
    args = get_args()

    group_info = torch.randn(args.batch_size, 4).to(args.device)
    month_info = torch.randn(args.batch_size, 11, 2).to(args.device)
    day_info = torch.randn(args.batch_size, 11, 24, 2).to(args.device)
    model = Stock(args).to(args.device)
    
    res = model(group_info, month_info, day_info)
    print(res.shape)