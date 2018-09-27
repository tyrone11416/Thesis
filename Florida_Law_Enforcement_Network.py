import networkx as nx
import matplotlib.pyplot as plt
import csv

mFileName = "Florida_Law_Enforcement_Network.csv"
plt.figure(figsize=(20, 14))
G = nx.Graph()
counter = 0


def VisualizeGraph():
    nx.draw(G, center=1581, node_color='blue', with_labels=True)
    plt.savefig('Florida_Law_Enforcement_Network.png')
    plt.show()



def LoadData(file):
    global counter
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)


        state=""
        oldstate=""
        state_counter=0
        county_counter=0
        region_counter=0
        local_counter=0

        region=""
        oldregion=""

        county=""
        oldcounty=""

        local=""
        oldlocal=""

        for row in reader:

            #Print the data (for debugging purposes - comment out.)
            print(row['state'], row['station_name'], row['county'], row['local'])

            #This is quick and dirty just to prove you can do it.
            state = row['state']

            #state Level.
            # if its a new state make a new top node.
            if state != oldstate:
                G.add_node(counter, weight=0.4, time='2pm', name=state)
                G.add_edge(0, counter)
                print(G.nodes[counter]) #print out node attributes to console.
                state_counter = counter
                counter = counter + 1
                oldstate=state

            region = row['region']
            if region != oldregion:
                G.add_node(counter, weight=0.4, time='2pm', name=region)
                G.add_edge(state_counter, counter)
                region_counter = counter
                counter = counter + 1
                oldregion=region

            county = row['county']
            if county != oldcounty:
                G.add_node(counter, weight=0.4, time='2pm', name=county)
                G.add_edge(region_counter, counter)
                county_counter = counter
                counter = counter + 1
                oldcounty=county


            #local Level
            G.add_node(counter, weight=0.7, time='12pm', name=row['local'])
            print(G.nodes[counter]) #print out node attributes to console.
            G.add_edge(county_counter, counter, weight=4.7 )
            local_counter = counter
            counter = counter + 1


def main():
     global counter
     G.add_node(counter, time='1pm', node_color='yellow', name="DNeX")
     counter = counter + 1

     print("Loading Data from file.... ", mFileName)
     LoadData(mFileName)
     VisualizeGraph()



if __name__== "__main__":
    main()