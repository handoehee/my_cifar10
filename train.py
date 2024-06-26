import os
import argparse
import torch
import torchvision
from models.vgg import vgg11_bn
import torch.nn as nn
import torch.optim as optim
import time
import numpy as np

def train(opt):
    epochs = opt.epochs
    batch_size = opt.batch_size
    name = opt.name
    # Train dataset
    transforms = torchvision.transforms.ToTensor()
    train_dataset = torchvision.datasets.CIFAR10('./data', train=True, download=True, 
                                                    transform=transforms)
    classes = ('plane', 'car', 'bird', 'cat','deer', 'dog', 'frog', 'horse', 'ship', 'truck')                                                
    
    num_workers = min([os.cpu_count(), batch_size])
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size,
                             shuffle=True, num_workers=num_workers, drop_last=False)
    for i, (imgs, targets) in enumerate(train_dataloader):
        print('batch idx=%d/%d' % (i, len(train_dataloader)-1))
        
    # Network model
    model = vgg11_bn()
    
    # Loss function and optimizer
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    
    start_epoch, end_epoch = (0, epochs)
    for epoch in range(start_epoch, end_epoch):
        print('epoch: %d/%d' % (epoch, end_epoch-1))
        t0 = time.time()
        epoch_loss = train_one_epoch(train_dataloader, model, loss_fn, optimizer)
        t1 = time.time()
        print('loss=%.4f (took %.2f sec)\n' % (epoch_loss, t1-t0))

def train_one_epoch(train_dataloader, model, loss_fn, optimizer):
    model.train()
    losses = [] 
    for i, (imgs, targets) in enumerate(train_dataloader):
        optimizer.zero_grad()   # zeros the paramter gradients
        preds = model(imgs)     # forward
        loss = loss_fn(preds, targets) # calculates the iteration loss  
        loss.backward()         # backward
        optimizer.step()        # update weights
        # print the iteration loss every 100 iterations
        if i % 100 == 0:
            print('\t iteration: %d/%d, loss=%.4f' % (i, len(train_dataloader)-1, loss))    
        losses.append(loss.item())
    return torch.tensor(losses).mean().item()

    pass # debug checkpoint

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=10, help='target epochs')
    parser.add_argument('--batch-size', type=int, default=64, help='batch size')
    parser.add_argument('--name', default='handoehee', help='name for the run')

    opt = parser.parse_args()

    train(opt)
