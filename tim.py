#!/usr/bin/env python
# encoding: utf-8

# Modified slightly from the gist at:
# http://timotheepoisot.fr/2012/05/18/networkx-metapopulations-python/

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

Patches = 100   # Number of patches
P_ext = 0.01    # Probability of extinction (e)
P_col = 0.014   # Probability of colonization (c)
P_init = 0.02   # Probability that a patch will be occupied at the beginning
Distance = 1.4  # An arbitrary parameter to determine which patches are connected

G = nx.Graph()
Time = [0]

class patch:
	def __init__(self,status=0,pos=(0,0)):
		self.status = status
		self.pos = pos
	def __str__(self):
		return(str(self.status))


def LoadData():
    for i in range(Patches):
        Stat = 1 if np.random.uniform() < P_init else 0
        Pos  = (np.random.uniform()*10-5,np.random.uniform()*10-5)
        G.add_node(patch(Stat,Pos))
    
    for p1 in G.nodes():
        for p2 in G.nodes():
            Dist = np.sqrt((p1.pos[1]-p2.pos[1])**2+(p1.pos[0]-p2.pos[0])**2)
            if Dist <= Distance:
                G.add_edge(p1,p2)


def Simulate(Occupancy):
    for timestep in range(2000):
        ## Check for extinctions
        for n in G.nodes():
            if (n.status == 1 and np.random.uniform() < P_ext):
                n.status = 0
        ## Check for invasions
        for n in G.nodes():
            if n.status == 1:
                neighb = G[n] # That's it, a list of the neighbors
                for nei in neighb:
                    if nei.status == 0:
                        if np.random.uniform() < P_col:
                            nei.status = 1
                            break
        Time.append(timestep+1)
        Occupancy.append(np.sum([n.status for n in G])/float(Patches))


LoadData()

pos = {}
for n in G.nodes():
    pos[n] = n.pos

occup = [n.status for n in G]   
nx.draw(G,node_color=occup,with_labels=False,cmap=plt.cm.Greys,pos=pos,vmin=0,vmax=1)
plt.show()

Occupancy = [np.sum([n.status for n in G])/float(Patches)]
Simulate(Occupancy)

nx.draw(G,node_color=[n.status for n in G],with_labels=False,cmap=plt.cm.Greys,pos=pos,vmin=0,vmax=1)
plt.show()

plt.plot(Time,Occupancy,'g-')
plt.show()