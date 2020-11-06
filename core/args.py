import torch
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--epoch', type=int, default = 30)
    parser.add_argument('-b', '--batch_size', type=int, default=1)
    parser.add_argument('-m', '--mode', type=str, default='train', choices=['train', 'test'])
    parser.add_argument('-c', '--ckpt', type=str, default='checkpoint.pt')
    args = parser.parse_args()
    args.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    return args
