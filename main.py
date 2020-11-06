import os
from core.trainer import Trainer, get_args

if __name__ == '__main__':
    args = get_args()
    trainer = Trainer(args)

    if args.mode == 'train':
        trainer.train()
    else:
        trainer.test()