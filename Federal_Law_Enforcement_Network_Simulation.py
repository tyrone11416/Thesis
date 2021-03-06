#!/usr/bin/env python
# encoding: utf-8
# Modified slightly from the gist at:
# http://timotheepoisot.fr/2012/05/18/networkx-metapopulations-python/
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import csv
import random
import statistics


Agencies = 100 # Number of patches
Infected = 0.25  # Probability of Infection
Susceptible = 0.25  # Probability of being Susceptible
Initial_Infection = 0.25  # Probability that a patch will be infected at the beginning
P_init_local = 0.50  # made this high to weight the edge of the graph to start

n_size = []

local_infection = random.uniform(0.01, 0.45)
county_infection = random.uniform(0.01, 0.25)
region_infection = 0.01
state_infection = 0.001


G = nx.Graph()
plt.figure(figsize=(20, 15))
Time = [0]
mFileName = "Florida_Law_Enforcement_Network.csv"
counter = 0


class patch:
    def __init__(self, status=0, pos=0, name=""):
        self.status = status
        self.name = name
        self.pos = pos

    def __str__(self):
        return (str(self.status))


def LoadData(file):
    # Ty way. or the high way.
    global counter
    Stat = 1 if np.random.uniform() < Initial_Infection else 0
    Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
    p_top = patch(Stat, counter)
    node = G.add_node(p_top)
    counter = counter + 1
    n_size.append(5000)


    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        state = ""
        oldstate = ""
        state_counter = 0
        county_counter = 0
        region_counter = 0
        local_counter = 0
        region = ""
        oldregion = ""
        county = ""
        oldcounty = ""
        local = ""
        oldlocal = ""
        p_state = ""
        p_reg = ""
        p_count = ""

        for row in reader:
            # This is quick and dirty just to prove you can do it.
            state = row['state']
            # state Level.

            # if its a new state make a new top node.
            if state != oldstate:
                #Stat = 1 if np.random.uniform() < state_infection else 0
                Stat = float(row['state_infection'])
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                p_state = patch(Stat, Pos)
                G.add_node(p_state)
                G.add_edge(p_top, p_state, weight=.25)
                state_counter = counter
                counter = counter + 1
                oldstate = state
                n_size.append(int(row['state_node_size']))

            region = row['region']
            if region != oldregion:
                #Stat = 1 if np.random.uniform() < region_infection else 0
                Stat = float(row['region_infection'])
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                p_reg = patch(Stat, Pos)
                G.add_node(p_reg)
                G.add_edge(p_state, p_reg, weight=.25)
                region_counter = counter
                counter = counter + 1
                oldregion = region
                n_size.append(int(row['region_node_size']))


            county = row['county']
            if county != oldcounty:
                #Stat = 1 if np.random.uniform() < county_infection else 0
                Stat = float(row['county_infection'])
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                p_count = patch(Stat, Pos)
                G.add_node(p_count, weight=1)
                G.add_edge(p_reg, p_count, weight=.25)
                county_counter = counter
                counter = counter + 1
                oldcounty = county
                n_size.append(int(row['county_node_size']))

            local = row['local']
            if local != oldlocal:
                Stat = float(row['local_infection'])
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                # local Level
                p_loc = patch(Stat, Pos)
                G.add_node(p_loc, weight=0.4)
                G.add_edge(p_count, p_loc, weight=.25)
                local_counter = counter
                counter = counter + 1
                n_size.append(int(row['local_node_size']))



def Simulate(Infection):
    for timestep in range(50):
        ## Check for infections
        for n in G.nodes():
            if (n.status == 1 and np.random.uniform() < Infected):
                n.status = 1
        ## Check for Agencies that are infected
        for n in G.nodes():
            if n.status == 0:
                neighb = G[n]  # That's it, a list of the neighbors
                for nei in neighb:
                    if nei.status == 0:
                        if np.random.uniform() < Susceptible:
                            nei.status = 1

                            break

        Time.append(timestep + 1)
        Infection.append(np.sum([n.status for n in G]) / float(Agencies))


def main():
    print("Loading Data from file.... ", mFileName)
    LoadData(mFileName)
    pos = {}
    for n in G.nodes():
        pos[n] = n.pos
        occup = [n.status for n in G]

    print(nx.info(G))
    print(nx.degree_histogram(G))
    density = nx.density(G)
    print("Network density:", density)
    degree = nx.degree_centrality(G)
    print(degree)
    bw_centrality = nx.betweenness_centrality(G, weight=10)
    print(bw_centrality)


    

    nx.draw(G, center=1581, node_size=(n_size), node_color=occup, with_labels=True, cmap=plt.cm.plasma,
            vmin=0, vmax=1)
    plt.savefig('Federal_Law_Enforcement_network_start_infection.pdf')
    plt.show()

    Infection = [np.sum([n.status for n in G]) / float(Agencies)]
    Simulate(Infection)
    plt.figure(figsize=(20, 15))
    nx.draw(G, center=1581, node_size=(n_size), node_color=[n.status for n in G], with_labels=False,
            cmap=plt.cm.plasma, vmin=0, vmax=1)
    plt.savefig('Federal_Law_Enforcement_network_end_infection.png')
    plt.show()

    plt.plot(Time, Infection, 'g-')
    plt.xlabel('TIME')
    plt.ylabel('INFECTION')
    plt.savefig('Federal_Law_Enforcement_network_plot.png')
    plt.tight_layout()
    plt.show()

    data = [np.sum([n.status for n in G]) / float(Agencies)]
    m = statistics.mean(data)
    print(statistics.mean(data))


if __name__ == "__main__":
    main()