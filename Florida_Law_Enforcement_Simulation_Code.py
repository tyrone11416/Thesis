#!/usr/bin/env python
# encoding: utf-8
# Modified slightly from the gist at:
# http://timotheepoisot.fr/2012/05/18/networkx-metapopulations-python/
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import csv

Agencies = 1  # Number of patches
Infected = 0.0001  # Probability of Infection
Susceptible = 0.0001  # Probability of being Susceptible
Initial_Infection = 0.001  # Probability that a patch will be infected at the beginning
P_init_local = 0.005  # made this high to weight the edge of the graph to start


n_size = []

G = nx.Graph()
plt.figure(figsize=(20, 15))
Time = [0]
mFileName = "Florida_Law_Enforcement_Network.csv"
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
    node = G.add_node(p_top, time='1pm', name="N-DEx")
    counter = counter + 1
    n_size.append(10000)

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
            # Print the data (for debugging purposes - comment out.)
            # print(row['state'], row['state_infection'], row['region'], row['region_infection'], row['county'],
            # row['county_infection'], row['local'], row['local_infection'])

            # This is quick and dirty just to prove you can do it.
            state = row['state']
            # state Level.
            # if its a new state make a new top node.
            if state != oldstate:
                # Stat = 1 if np.random.uniform() < state_infection else 0
                Stat = 1 if np.random.uniform() < float(row['state_infection']) else 0
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                p_state = patch(Stat, Pos)
                G.add_node(p_state, name=state)
                G.add_edge(p_top, p_state, weight=.25)
                state_counter = counter
                counter = counter + 1
                oldstate = state
                n_size.append(int(row['state_node_size']))

            region = row['region']
            if region != oldregion:
                # Stat = 1 if np.random.uniform() < region_infection else 0
                Stat = 1 if np.random.uniform() < float(row['region_infection']) else 0
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                p_reg = patch(Stat, Pos)
                G.add_node(p_reg, name=region)
                G.add_edge(p_state, p_reg, weight=.25)
                region_counter = counter
                counter = counter + 1
                oldregion = region
                n_size.append(int(row['region_node_size']))

            county = row['county']
            if county != oldcounty:
                # Stat = 1 if np.random.uniform() < county_infection else 0
                Stat = 1 if np.random.uniform() < float(row['county_infection']) else 0
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                p_count = patch(Stat, Pos)
                G.add_node(p_count, name=county)
                G.add_edge(p_reg, p_count, weight=.25)
                county_counter = counter
                counter = counter + 1
                oldcounty = county
                n_size.append(int(row['county_node_size']))

            local = row['local']
            if local != oldlocal:
                Stat = 1 if np.random.uniform() < float(row['local_infection']) else 0
                Pos = (np.random.uniform() * 10 - 5, np.random.uniform() * 10 - 5)
                # local Level
                p_loc = patch(Stat, Pos)
                G.add_node(p_loc, name=local)
                G.add_edge(p_count, p_loc, weight=.25)
                local_counter = counter
                counter = counter + 1
                n_size.append(int(row['local_node_size']))


def Status():
    for n in G.nodes():
        return n
    output = Status()
    file = open(output.txt, "w")
    file.write('output')
    file.close()


def Simulate(Infection):
    for timestep in range(1000):
        Status()
        ## Check for infections
        for n in G.nodes():
            if n.status == 1 and np.random.uniform() < Infected:
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

    degree = nx.degree_centrality(G)
    print(degree)
    bw_centrality = nx.betweenness_centrality(G, weight=10)
    print(bw_centrality)

    plt.title('Initial Infection Status', fontsize=30)
    nx.draw(G, center=1581, node_size=(n_size), node_color=occup, with_labels=False, cmap=plt.cm.plasma,
            vmin=0, vmax=1)
    plt.savefig('beginning_infection/Florida_Law_Enforcement_network_start_infection.png')
    plt.show()

    Infection = [np.sum([n.status for n in G]) / float(Agencies)]
    Simulate(Infection)
    plt.figure(figsize=(20, 15))
    plt.title('Post Simulation Infection Status', fontsize=30)
    nx.draw(G, center=1581, node_size=(n_size), node_color=[n.status for n in G], with_labels=False,
            cmap=plt.cm.plasma, vmin=0, vmax=1)
    plt.savefig('end_infection/Florida_Law_Enforcement_network_end_infection.png')
    plt.show()

    # line plot
    plt.title('Node Infection over Time', fontsize=15)
    plt.plot(Time, Infection)
    plt.xlabel('TIME')
    plt.ylabel('INFECTED')
    # Customize the major grid
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    # Customize the minor grid
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.savefig('infection_timeplot/Florida_Law_Enforcement_network_plot.pdf')
    plt.tight_layout()
    plt.show()

    data = [np.sum([n.status for n in G]) / float(Agencies)]
    print(nx.info(G))
    print(nx.degree_histogram(G))
    density = nx.density(G)
    print("Network density:", density)
    print('Initial Node Infection =', sum(occup))
    print('Nodes Infected =', sum(data))







if __name__ == "__main__":
    main()