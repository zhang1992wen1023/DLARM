from __future__ import print_function
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
import torchvision
import torchvision.transforms as transforms
import os
import argparse
from torchvision import datasets,transforms, utils
from torch.utils.data import Dataset, DataLoader
from skimage import io, transform
import os
import torch
import time
import argparse
import random
import shutil
import sys
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import warnings
warnings.filterwarnings("ignore")

plt.ion()   
start = time.time()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
PATH = os.environ.get("DATASET_10SET", None)

epochs = 10

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
valset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)

trainset_loader = torch.utils.data.DataLoader(trainset, batch_size=4, shuffle=True, num_workers=4)
validationset_loader = torch.utils.data.DataLoader(valset, batch_size=4, shuffle=False, num_workers=4)

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

cfg = {
    'VGG11': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG13': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG16': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'VGG19': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
    }

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def adjust_learning_rate(optimizer, epoch, args):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    lr = args.lr * (0.1 ** (epoch // 30))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


class VGG(nn.Module):
    def __init__(self, vgg_name):
        super(VGG, self).__init__()
        self.features = self._make_layers(cfg[vgg_name])
        self.classifier = nn.Linear(25088, 4096)
        self.classifier1 = nn.Linear(4096, 4096)
        self.classifier2 = nn.Linear(4096, 10)
        self.relu = nn.ReLU(True)
        self.dropout = nn.Dropout() 

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.classifier1(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.classifier2(out)
        return out

    def _make_layers(self, cfg):
        layers = []
        in_channels = 3
        for x in cfg:
            if x == 'M':
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                layers += [nn.Conv2d(in_channels, x, kernel_size=3, padding=1), nn.BatchNorm2d(x), nn.ReLU(inplace=True)]
                in_channels = x
        layers += [nn.AvgPool2d(kernel_size=1, stride=1)]
        return nn.Sequential(*layers)


loss_fc = torch.nn.CrossEntropyLoss().to(device)
vgg = VGG('VGG11').to(device)
optimizer = torch.optim.Adam(vgg.parameters(), lr=1e-4)

for i in range(epochs):
    since = time.time()
    vgg.train()
    running_loss = 0.0
    for j, (input, targets) in enumerate(trainset_loader):
        input, targets = input.to(device), targets.to(device)
        input = torch.autograd.Variable(input)
        optimizer.zero_grad()
        train = vgg(input)
        targets = torch.autograd.Variable(targets)
        loss = loss_fc(train, targets)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if j % 100 == 99:
            print('[%d, %5d] training average loss: %.3f' %(i + 1, j + 1, running_loss / 100))
            running_loss = 0.0
    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    end = time.time()
    vgg.eval()
    class_correct = list(0.0001 for r in range(10))
    class_total = list(0.0001 for t in range(10))
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()
    running_loss = 0.0
    with torch.no_grad():
        end1 = time.time()
        for k, (images, labels) in enumerate(validationset_loader):
            images, labels = images.to(device), labels.to(device)
            images = torch.autograd.Variable(images)
	    labels = torch.autograd.Variable(labels)
            validate = vgg(images)
            loss = loss_fc(validate, labels)
            acc1, acc5 = accuracy(validate, labels, topk=(1, 5))
            losses.update(loss.item(), images.size(0))
            top1.update(acc1[0], images.size(0))
            top5.update(acc5[0], images.size(0))
            batch_time.update(time.time() - end1)
            end1 = time.time()
            labels = torch.autograd.Variable(labels)
            _, predicted = torch.max(validate, 1)
            c = (predicted == labels).squeeze()
            for m in range(labels.size(0)):
                label = labels[m]
                class_correct[label] += c[m].item()
                class_total[label] += 1
            running_loss += loss.item()
            if k % 16 == 15:
                print('[%d, %5d] validation average loss: %.3f' %(i + 1, k + 1, running_loss / 16))
                running_loss = 0.0
                print('Test: [{0}/{1}]\t'
                    'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                    'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                    'Acc@1 {top1.val:.3f} ({top1.avg:.3f})\t'
                    'Acc@5 {top5.val:.3f} ({top5.avg:.3f})'.format(k, len(validationset_loader), batch_time=batch_time, loss=losses, top1=top1, top5=top5))
    print(' * Acc@1 {top1.avg:.3f} Acc@5 {top5.avg:.3f}'.format(top1=top1, top5=top5))
    for k in range(10):
        print('Accuracy of %5s : %2d %%' % (classes[k], 100 * class_correct[k] / class_total[k]))

    validation_time = time.time() - end
    print('Validation complete in {:.0f}m {:.0f}s'.format(validation_time // 60, validation_time % 60))

totaltime = time.time() - start
print('Total execution complete in {:.0f}m {:.0f}s'.format(totaltime // 60, totaltime % 60))
configuration = totaltime - validation_time
configuration = configuration - time_elapsed
print('Configuration complete in {:.0f}m {:.0f}s'.format(configuration // 60, configuration % 60))
