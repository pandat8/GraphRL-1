from torch.utils.data import Dataset, DataLoader
from data.graphDataset import GraphDataset
from data.SSMCDataset import SSMCDataset
from data.UFSMDataset import UFSMDataset
from data.graph import Graph

from rl.model_a2c import Model_A2C_Sparse
from rl.train_a2c_td import TrainModel_TD
from rl.train_a2c_mc import TrainModel_MC
from gcn.models_gcn import GCN_Policy_SelectNode, GCN_Sparse_Policy_SelectNode, GCN_Sparse_Memory_Policy_SelectNode
from gcn.models_gcn import GCN_Value, GCN_Sparse_Value
from gcn.train_supervised_learning import Train_SupervisedLearning

import sys
import time
import argparse
import torch
import numpy as np
import matplotlib.pyplot as plt



# Training argument setting
parser = argparse.ArgumentParser()
parser.add_argument('--nocuda', action= 'store_true', default=False, help='Disable Cuda')
parser.add_argument('--novalidation', action= 'store_true', default=False, help='Disable validation')
parser.add_argument('--seed', type=int, default=50, help='Radom seed')
parser.add_argument('--epochs', type=int, default=5000, help='Training epochs')
parser.add_argument('--lr_actor', type=float, default= 0.01, help='Learning rate of actor')
parser.add_argument('--lr_critic', type=float, default= 0.001, help='Learning rate of critic')
parser.add_argument('--wd', type=float, default=5e-4, help='Weight decay')
parser.add_argument('--dhidden', type=int, default=1, help='Dimension of hidden features')
parser.add_argument('--dinput', type=int, default=1, help='Dimension of input features')
parser.add_argument('--doutput', type=int, default=1, help='Dimension of output features')
parser.add_argument('--dropout', type=float, default=0.1, help='Dropout Rate')
parser.add_argument('--alpha', type=float, default=0.2, help='Aplha')
parser.add_argument('--nnode', type=int, default=100, help='Number of node per graph')
parser.add_argument('--ngraph', type=int, default=10, help='Number of graph per dataset')
parser.add_argument('--nnode_test', type=int, default=100, help='Number of node per graph for test')
parser.add_argument('--ngraph_test', type=int, default=100, help='Number of graph for test dataset')
parser.add_argument('--use_critic', type=bool, default=False, help='Enable critic')

args = parser.parse_args()

np.random.seed(args.seed)
torch.manual_seed(args.seed)

args.cuda = not args.nocuda and torch.cuda.is_available()

if args.cuda:
   torch.cuda.manual_seed(args.seed)

# load data and pre-process
# train_dataset = GraphDataset(args.nnode, args.ngraph, random_seed=31)
# val_dataset = GraphDataset(args.nnode, args.ngraph, random_seed=33)
test_dataset = GraphDataset(args.nnode_test, args.ngraph_test)
train_dataset = UFSMDataset(start=18, end=22)
val_dataset = UFSMDataset(start=22, end=26)
# test_dataset = SSMCDataset()

# train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True, collate_fn=lambda x: x)
# val_loader = DataLoader(val_dataset, batch_size=1,  shuffle=True, collate_fn=lambda x: x)
# test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True, collate_fn=lambda x: x)
# test_loader = DataLoader(test_set, batch_size=1, collate_fn=lambda x: x)
# build the GCN model
actor = GCN_Sparse_Policy_SelectNode(nin=args.dinput,
                              nhidden= args.dhidden,
                              nout=args.doutput,
                              dropout=args.dropout,
                              ) # alpha=args.alpha

if args.cuda:
    actor.load_state_dict(torch.load('./results/models/gcn_policy_min_degree_pre_erg100_cuda.pth'))
    actor.cuda()
# else:
#     actor.load_state_dict(torch.load('./results/models/gcn_memory_policy_min_degree_pre_erg100.pthh'))

epoch = 0
# # test pretrained policy model
# train_sl = Train_SupervisedLearning(model=actor, test_dataset=test_dataset, use_cuda = args.cuda)
# features = np.ones([args.nnode,args.dinput], dtype=np.float32) # initialize the features for training set
# print('test stated')
# time_start = time.time()
# ratio, av_ratio, max_ratio, min_ratio, ratio_g2r, av_ratio_g2r, max_ratio_g2r, min_ratio_g2r = train_sl.test()
# time_end = time.time()
# print('test finished')
# print('Test time: {:.4f}'.format(time_end-time_start))
#
# # save/plot test results
# if args.cuda:
#     text_file = open("test/results/pretrain_mindegree_gcn_memory_ERG100_cuda.txt", "w")
# else:
#     text_file = open("test/results/pretrain_mindegree_gcn_memory_ERG100.txt", "w")
# text_file.write('\n Pretrained-model Test result: test_gcn_learn_mindegree\n')
# text_file.write('DataSet: GraphDataset\n')
# text_file.write('average ratio {:.4f} \n'.format(av_ratio))
# text_file.write('max ratio {:.4f}\n'.format(max_ratio))
# text_file.write('min ratio {:.4f}\n'.format(min_ratio))
# text_file.write('average ratio graph2random {:.4f}\n'.format(av_ratio_g2r))
# text_file.write('max ratio graph2random {:.4f}\n'.format(max_ratio_g2r))
# text_file.write('min ratio graph2random {:.4f}\n'.format(min_ratio_g2r))
# text_file.close()
#
# if args.cuda:
#     plt.switch_backend('agg')
#     plt.hist(ratio, bins=32)
#     plt.title('histogram: graph2mindegree ratio of Erdos-Renyi graph')
#     plt.savefig('./test/results/histogram_gnn2mindegree_gcn_memory_erg100_cuda.png')
#     plt.clf()
#     #
#     plt.hist(ratio_g2r, bins=32)
#     plt.title('graph2random_ratio_CrossEntropy Erdos-Renyi graph')
#     plt.savefig('./test/results/histogram_gnn2random_gcn_memory_erg100_cuda.png')
#     plt.clf()
# else:
#     plt.hist(ratio, bins= 32)
#     plt.title('histogram: graph2mindegree ratio of Erdos-Renyi graph')
#     plt.savefig('./test/results/histogram_gnn2mindegree_gcn_memory_erg100.png')
#     plt.clf()
#     #
#     plt.hist(ratio_g2r, bins= 32)
#     plt.title('graph2random_ratio_CrossEntropy Erdos-Renyi graph')
#     plt.savefig('./test/results/histogram_gnn2random_gcn_memory_erg100.png')
#     plt.clf()
#     #

# option of critic
critic = None
if args.use_critic:
    critic = GCN_Sparse_Value(nin=args.dinput,
                              nhidden=args.dhidden,
                              nout=args.doutput,
                              dropout=args.dropout,
                              ) # alpha=args.alpha

model_a2c = Model_A2C_Sparse(actor=actor,
                             epsilon=0, # non-pretrain:0.02
                             use_critic= args.use_critic,
                             use_cuda= args.cuda,
                             critic= critic)
if args.cuda:
   model_a2c.cuda()

# train RL-model
train_a2c = TrainModel_MC(model_a2c,
                          train_dataset,
                          val_dataset,
                          weight_d = args.wd,
                          use_cuda=args.cuda)
print('Training started')
time_start = time.time()
train_a2c.train_and_validate(n_epochs=args.epochs,
                             lr_actor=args.lr_actor,
                             lr_critic=args.lr_critic,
                             use_critic = args.use_critic
                             )
print('Training finished')
print('Training time: {:.4f}'.format(time.time()-time_start))





