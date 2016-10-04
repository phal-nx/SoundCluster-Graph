import soundcloud
import getpass
import pprint
import pdb
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import threading
import json
import multiprocessing.dummy
import forceatlas
from IPython import embed
from utils.helpers import *
from functools import partial
from termcolor import colored
from collections import defaultdict
import utils.db as db

sc_username = input(colored("Soundcloud Username:", "blue"))
sc_pass = getpass.getpass(colored("Password:", "blue"))

pp = pprint.PrettyPrinter(indent=4)
client = soundcloud.Client(
    client_id='8e906fb7c324fc6640fd3fc08ef9d1ff',
    client_secret='aacd3a93bdfcf1dd65ed33497f091800',
    username=sc_username,
    password=sc_pass
)
user_id = get_my_user_id(client)
my_followings = get_all_followings(client)

id_list = {follower.id: follower for follower in my_followings}
print(', '.join([colored(x.username, 'red') for x in my_followings]))

# nx Graph
G = nx.DiGraph()
G.add_nodes_from(id_list.keys(), existing=True)

# js FDG
nodes = {user.id: {'id': user.id, 'label': user.username, 'weight': 1, 'group': 2 if user.followers_count > 500 else 1} for user in my_followings}
# Neo4j Add Nodes
db.add_followings(my_followings)

links = list()
edges_list = defaultdict(list)
p = multiprocessing.dummy.Pool(5)
#mapped_followings = p.map(partial(get_all_followings(client)), my_followings)
#for curr_followings in mapped_followings:
for follower in my_followings:
    # TODO Threading
    follower_id = follower.id
    try:
        curr_followings = get_all_followings(client, follower_id)
    except:
        continue
    existing_followings = [user for user in curr_followings if user.id in id_list.keys()]
    existing_ids = [user.id for user in existing_followings]
    not_existing_followings = [user for user in curr_followings if user.id not in id_list.keys()]
    not_existing_ids = [user.id for user in not_existing_followings]

    edges_list[follower_id].extend(existing_followings)
    if existing_followings:
        #Everyone following someone else you follow
        for following in existing_followings:
            G.add_edge(follower_id, following.id)  # Nx
            edges_list[follower_id].append(following)  # Custom
            links.append({'id': '{}->{}'.format(follower_id, following.id), 'source': follower_id,
                          'target': following.id, 'value': 1})  # JS FDG
            print('{} -> {}'.format(colored(follower.username, "red"), colored(following.username, 'cyan')))
        # all non followed ppl
        G.add_nodes_from(not_existing_followings, existing=False)
        for following in not_existing_followings:
            G.add_edge(follower_id, following.id, existing=False)  # Nx
            #print('{} -> {}'.format(colored(follower.username, "cyan"), colored(following.username, 'cyan')))

# Neo4j Edges
db.add_edges(edges_list)


pos = forceatlas.forceatlas2_layout(G)


# Extract x and y positions
for uid, position in pos.items():
    # Gets the positions, multiplies by 5 then casts as an integer.
    nodes[uid]['x'], nodes[uid]['y'] = position.tolist()

nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'))
nx.draw_networkx_edges(G, pos, edgelist=existing_followings, arrows=True, width=3, edge_color='r')
nx.draw_networkx_edges(G, pos, edgelist=not_existing_followings, arrows=True, width=2, edge_color='rb')


# JS FDG
data = {"nodes": list(nodes.values()), "edges": links}
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
embed()
plt.show()