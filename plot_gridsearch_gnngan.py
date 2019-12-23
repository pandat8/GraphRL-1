import tarfile
import os
import torch
import numpy as np
import torch
import matplotlib.pyplot as plt
from collections import OrderedDict
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


l, p = np.loadtxt('./results/logs/log_supervise_gnngan_gridsearch_mindegree_ER_small20graphs_train.txt', delimiter=' ', usecols=(7, 9), unpack=True)
l= np.reshape(l,(41,41))
print(l)
p= np.reshape(p,(41,41))

a1_all = np.linspace(-5, 5, 41)
a2_all = np.linspace(-5, 5, 41)

# Z = []
for a2 in range(-20, 21, 1):
    a2 /= 4

    for a1 in range(-20, 21, 1):
        a1 /= 4

        # z = (1 - w1 / 2 + w1 ** 5 + w2 ** 3) * np.exp(-w1 ** 2 - w2 ** 2)
        # Z.append(z)


plt.close()
A1, A2 = np.meshgrid(a1_all, a2_all)

p=p/12593.35
l=np.log(l)


A1 = A1[0:40, 12:29]
A2 = A2[0:40, 12:29]
l =  l[0:40,12:29]
p =  p[0:40,12:29]

fig = plt.figure(figsize=(10,6))
ax = Axes3D(fig)
surf = ax.plot_surface(A1, A2, l, rstride=1, cstride=1, cmap='rainbow')
# plt.title('Averaged KL loss')

# ax.set_zlim(0.9, 1.30)
# ax.set_ybound(-5,0)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=8)
# print(ax.azim)
# ax.view_init(azim=-90)

plt.xlabel('a1')
plt.ylabel('a2')
ax.set_zlabel('Loss (in log scale)')

plt.show()


fig = plt.figure(figsize=(10,6))
ax = Axes3D(fig)
surf = ax.plot_surface(A1, A2, p, rstride=1, cstride=1, cmap='rainbow'
                       )
# cmap=cm.coolwarm, linewidth=0, antialiased=False

# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

# ax.set_zlim(0.9, 1.30)
# ax.set_ylim(-5,-1)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=8)
plt.xlabel('a1')
plt.ylabel('a2')
ax.set_zlabel('Normalized Fill-in')
# plt.title('Averaged fill-in ratio between gnn and min_degree')

plt.show()

A1 = A1[0:28, 4:13]
A2 = A2[0:28, 4:13]
l =  l[0:28,4:13]
p =  p[0:28,4:13]



# plt.clf()
# fig = plt.figure()
# Cf = plt.contourf(W1, W2, l, 5, levels=[ np.log(i/10000) for i in range(1,50,10)], alpha=.75, cmap=plt.cm.hot, extend='both')
# C = plt.contour(W1, W2, l,5,levels=[ np.log(i/10000) for i in range(1,50,10)], colors='black', linewidth=.5, extend='both')
# plt.clabel(C, inline=1, fontsize=9)
# fig.colorbar(Cf, shrink=0.5, aspect=8)
# plt.title('Averaged KL loss')
# plt.xlabel('W1')
# plt.ylabel('W2')
#
# plt.show()
#
# plt.clf()
#
# plt.clf()
# fig = plt.figure()
# Cf = plt.contourf(W1, W2, p,7, levels=[ 1.0000001,1.001,1.05,1.1,1.2,1.3], alpha=.75, cmap=plt.cm.hot,  extend='both') # levels=[ i/100 for i in range(100,110,1)],
# C = plt.contour(W1, W2, p,7, levels=[1.0000001,1.001,1.05,1.1,1.2,1.3], colors='black', linewidth=.5, extend='both')
# fig.colorbar(Cf, shrink=0.5, aspect=8)
# plt.clabel(C, inline=1, fontsize=9)
# plt.xlabel('W1')
# plt.ylabel('W2')
# plt.title('Averaged fill-in ratio between gnn and min_degree')
# plt.show()







# def untar(input_dir, output_dir):
#     for path, directories, files in os.walk(input_dir):
#         for f in files:
#
#             if f.endswith(".tar.gz"):
#                 index_of_dot = f.index('.')
#                 f_name_without_extension = f[:index_of_dot]
#
#                 tar = tarfile.open(os.path.join(path, f), 'r:gz')
#                 for member in tar.getmembers():
#
#                     if member.name.endswith(f_name_without_extension+'.mtx'):  # skip if the TarInfo is not files
#                         member.name = os.path.basename(member.name)  # remove the path by reset it
#                         tar.extract(member, output_dir)  # extract
#                 tar.close()
#
#
#
# if __name__ == '__main__':
#     untar('./data/UFSM/ss_large/ss_large_source/', './data/UFSM/ss_large/ss_large_set/')