#!/usr/bin/env python
# encoding: utf-8
# Modified slightly from the gist at:
# http://timotheepoisot.fr/2012/05/18/networkx-metapopulations-python/
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import csv
import random
Agencies = 1 # Number of patches
Infected = 0.25  # Probability of Infection
Susceptible = 0.25  # Probability of being Susceptible
Initial_Infection = 0.25  # Probability that a patch will be infected at the beginning
P_init_local = 0.50  # made this high to weight the edge of the graph to start

local_infection = random.uniform(0.01, 0.45)
county_infection = random.uniform(0.01, 0.25)
region_infection = 0.01
state_infection = 0.001

G = nx.Graph()
Time = [0]
mFileName = "Region_and_County_Example.csv"
counter = 0


class patch:
    def __init__(self, status=0, pos=0):
        self.status = status

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

    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        state = ""
        oldstate = ""
        state_counter = 0
        county_counter = 0
        region_counter = 0
        local_counter = 0
        region = ''
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
                Stat = 1 if np.random.uniform() < state_infection else 0
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                p_state = patch(Stat, Pos)
                G.add_node(p_state)
                G.add_edge(p_top, p_state)
                state_counter = counter
                counter = counter + 1
                oldstate = state

            region = row['region']
            if region != oldregion:
                Stat = 1 if np.random.uniform() < region_infection else 0
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                p_reg = patch(Stat, Pos)
                G.add_node(p_reg)
                G.add_edge(p_state, p_reg)
                region_counter = counter
                counter = counter + 1
                oldregion = region


            county = row['county']
            if county != oldcounty:
                Stat = 1 if np.random.uniform() < county_infection else 0
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                p_count = patch(Stat, Pos)
                G.add_node(p_count)
                G.add_edge(p_reg, p_count)
                county_counter = counter
                counter = counter + 1
                oldcounty = county

            local = row['local']
            if local != oldlocal:
                Stat = 1 if np.random.uniform() < local_infection else 0
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                # local Level
                p_loc = patch(Stat, Pos)
                G.add_node(p_loc)
                G.add_edge(p_count, p_loc)
                local_counter = counter
                counter = counter + 1



def Simulate(Infection):
    for timestep in range(2000):
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

    nx.draw(G, center=1581, node_color=occup, with_labels=True, cmap=plt.cm.plasma, vmin=0, vmax=1)
    plt.savefig('region_county_network_start_infection.png')
    plt.show()

    Infection = [np.sum([n.status for n in G]) / float(Agencies)]
    Simulate(Infection)
    nx.draw(G, center=1581, node_color=[n.status for n in G], with_labels=False, cmap=plt.cm.plasma, vmin=0, vmax=1)
    plt.savefig('region_county_network_end_infection.png')
    plt.tight_layout()
    plt.show()

    plt.plot(Time, Infection, 'g-')
    plt.xlabel('TIME')
    plt.ylabel('INFECTION')
    plt.savefig('region_county_network_plot.png')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()