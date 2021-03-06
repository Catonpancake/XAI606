from __future__ import print_function
import argparse
import numpy as np
import torch
import os

## Module
from dataLoader import get_datapath, DataSegmentationLoader
from utils import *
from models import UNet
from train import train

parser = argparse.ArgumentParser(description='Pytorch Brain Tumor Segmentation UNet')

parser.add_argument('--in_channel', default=3, type=int,
                    help='perturbation magnitude')
parser.add_argument('--out_channel', default=1, type=int,
                    help='perturbation magnitude')
parser.add_argument('--epochs', default=1, type=int,
                    help='perturbation magnitude')
parser.add_argument('--nfold', default=5, type=int,
                    help='perturbation magnitude')
parser.set_defaults(argument=True)


def seed_everything(seed: int = 42):
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed)
    
def main():    
    # Import Data
    global args
    args = parser.parse_args()    
    
    #Use GPU
    device = 'cuda'  if torch.cuda.is_available() else 'cpu'
    if torch.cuda.is_available():
        print(f'CUDA is available. Your device is {device}.')
    else:
        print(f'CUDA is not available. Your device is {device}. It can take long time training in CPU.')    
    
    #Fix Seed
    random_state = 42
    seed_everything(random_state)            
    
    #Dataload
    image, mask = get_datapath('./data/', random_state)

    dataloader = DataSegmentationLoader(image, mask)

    model = UNet(in_channels=args.in_channel, out_channels=args.out_channel).to(device)
    loss = DiceLoss()
    train(dataloader, model, loss, device, args.epochs, args.nfold)

if __name__ == '__main__':
    main()