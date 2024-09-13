#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 10:42:34 2020

@author: navid
"""



import matplotlib.pyplot as plt
import numpy as np


d = np.loadtxt('result.txt')

n_p = 100
n_q = 30

x = np.arange(0,n_p)
y = np.arange(0,n_q)
z = np.zeros((n_p,n_q))
k = 0
for i in x:
    for j in y:
        z[i,j] = d[k,3]
        k+=1
        
z2 = np.transpose(z)
plt.figure(figsize=(20,11))
plt.contour(np.linspace(0,1,100),np.linspace(0,1/3,30),z2,levels=np.linspace(0,1,70),cmap='Greens',vmin=0 , vmax=1)
plt.xticks([0,1/3,2/3,1],[0 , r'1/3' , r'2/3' , 1],fontsize=40)
plt.yticks([1/6,1/3],[r'1/6' , r'1/3'],fontsize=40)
plt.ylabel(r'$q$', fontsize=40,rotation=0,labelpad=30)
plt.xlabel(r'$p$',fontsize=40,labelpad=1)
cbar = plt.colorbar(ticks=[0,0.2,0.4,0.6,0.8,1])
cbar.ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1], fontsize=20)  # vertically oriented colorbar
cbar.ax.set_ylabel(r'$\langle R \rangle $', fontsize =30)
plt.savefig('phase2.png')


k = 0
for i in x:
    for j in y:
        z[i,j] = d[k,4]
        k+=1
        
z2 = np.transpose(z)
plt.figure(figsize=(20,11))
plt.contourf(x,y,z2,levels=np.linspace(0,1,50),cmap='BuGn',vmin=0 , vmax=1)
plt.xticks([0,(n_p-1)/2,n_p-1],[0,0.5,1],fontsize=40)
plt.yticks([(n_q-1)/2,n_q-1],[r'1/6' , r'1/3'],fontsize=40)
plt.ylabel(r'$q$', fontsize=40,rotation=0,labelpad=30)
plt.xlabel(r'$p$',fontsize=40,labelpad=1)
cbar = plt.colorbar(ticks=[0,0.2,0.4,0.6,0.8,1])
cbar.ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1], fontsize=20)  # vertically oriented colorbar
cbar.ax.set_ylabel(' Prob. of Win ', fontsize =30)
plt.savefig('win_prob.png')


k = 0
for i in x:
    for j in y:
        z[i,j] = d[k,5]
        k+=1
        
z2 = np.transpose(z)
plt.figure(figsize=(20,11))
plt.contourf(x,y,z2,levels=np.linspace(0,1,11),cmap='BuGn',vmin=0 , vmax=1)
plt.xticks([0,(n_p-1)/2,n_p-1],[0,0.5,1],fontsize=40)
plt.yticks([(n_q-1)/2,n_q-1],[r'1/6' , r'1/3'],fontsize=40)
plt.ylabel(r'$q$', fontsize=40,rotation=0,labelpad=30)
plt.xlabel(r'$p$',fontsize=40,labelpad=1)
cbar = plt.colorbar(ticks=[0,0.2,0.4,0.6,0.8,1])
cbar.ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1], fontsize=20)  # vertically oriented colorbar
cbar.ax.set_ylabel(' Prob. of lose ', fontsize =30)
plt.savefig('lose_prob.png')



k = 0
for i in x:
    for j in y:
        z[i,j] = d[k,6]
        k+=1
        
z2 = np.transpose(z)
plt.figure(figsize=(20,11))
plt.contourf(x,y,z2,levels=np.linspace(0,1,11),cmap='BuGn',vmin=0 , vmax=1)
plt.xticks([0,(n_p-1)/2,n_p-1],[0,0.5,1],fontsize=40)
plt.yticks([(n_q-1)/2,n_q-1],[r'1/6' , r'1/3'],fontsize=40)
plt.ylabel(r'$q$', fontsize=40,rotation=0,labelpad=30)
plt.xlabel(r'$p$',fontsize=40,labelpad=1)
cbar = plt.colorbar(ticks=[0,0.2,0.4,0.6,0.8,1])
cbar.ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1], fontsize=20)  # vertically oriented colorbar
cbar.ax.set_ylabel(' Prob. of draw ', fontsize =30)
plt.savefig('draw_prob.png')

n_p = int(100)
n_q = int(30)
p,q = np.meshgrid(np.linspace(0,1,n_p),np.linspace(0,1/3,n_q))

# =============================================================================
# ES = -1+3*q+2/3*p -2*p*q
# EP = 1-3*q-2/3*p +2*p*q 
# ER = p/3
# =============================================================================

alpha = np.zeros((n_p,n_q))
beta = np.zeros((n_p,n_q))
gama = np.zeros((n_p,n_q))

k = 0
for i in x:
    for j in y:
        alpha[i,j] = d[k,4]
        beta[i,j] = d[k,5]
        gama[i,j] = d[k,6]
        k+=1

alpha = alpha.T
beta = beta.T
gama = gama.T



ES = (1-p)*(3*q-1) + p*(alpha + beta/2 + gama*(3*q-1))
EP = (1-p)*(1-3*q) + p*(alpha + beta/2 + gama*(1-3*q))
ER = p*(alpha + beta/2)*np.ones((n_q,n_p))

optimal = np.zeros((n_q,n_p))
for i in range(n_q):
    for j in range(n_p):
        win = 0
        lose = 0
        draw = 0
        for k in [ER[i,j],ES[i,j],EP[i,j]]:
            if k == np.max([ER[i,j],ES[i,j],EP[i,j]]):
                win = k
            elif k == np.min([ER[i,j],ES[i,j],EP[i,j]]):
                lose = k
            else:
                draw = k
                
        optimal[i,j] = win*alpha[i,j] + lose*beta[i,j] + draw*gama[i,j]
        
        
        
plt.figure(figsize=(20,11))
plt.contourf(p,q,optimal,levels=np.linspace(0,1,6),cmap='BuGn',vmin=0 , vmax=1)
plt.xticks([0,0.5,1],fontsize=40)
plt.yticks([1/6,1/3],[r'1/6' , r'1/3'],fontsize=40)
plt.ylabel(r'$q$', fontsize=40,rotation=0,labelpad=30)
plt.xlabel(r'$p$',fontsize=40,labelpad=1)
cbar = plt.colorbar(ticks=[0,0.2,0.4,0.6,0.8,1])
cbar.ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1], fontsize=20)  # vertically oriented colorbar
cbar.ax.set_ylabel(r'$\langle R \rangle$', fontsize =30)
plt.savefig('analytical.png')


x=np.linspace(0,1,100)
plt.plot(x,((3*x-2)/(6*(x-1))),color='green')
plt.plot(x,((1-3*x)/(3*(1-x))),color='green')
plt.ylim(0,1/3)

plt.plot(x,1/3*((1-3*x)/(1-x)),color='green')
plt.plot(x,1/3*(x/(2*x-2)+1),color='green')
plt.plot(x,-1/3*(2*x/(1-x)-1),color='green')




#plot for constant q values
#qs = [0 , 1/12 , 1/6, 1/4 ,1/3]
plt.figure(figsize=(14,13))
plt.plot(np.linspace(0,1,100) , z2[0] ,  label = r'$q=0$')
plt.plot(np.linspace(0,1,100) , z2[7] ,  label = r'$q=1/12$')
plt.plot(np.linspace(0,1,100) , z2[15] ,  label = r'$q=1/6$')
plt.plot(np.linspace(0,1,100) , z2[23] ,  label = r'$q=1/4$')
plt.plot(np.linspace(0,1,100) , z2[29] ,  label = r'$q=1/3$')
plt.legend(fontsize=30)
plt.xticks([0,1/3,2/3,1],[0 , r'1/3' , r'2/3' , 1],fontsize=40)
plt.yticks(fontsize=40)
plt.xlabel('p',fontsize=40)
plt.ylabel('R',fontsize=40)