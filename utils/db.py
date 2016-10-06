from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
from utils.helpers import *
from termcolor import colored
from collections import defaultdict
import soundcloud


gdb = GraphDatabase("http://localhost:7474", username="neo4j", password="letmein")


def add_followings(followings):
    """
    :param followings: List of soundcloud user objects
    :return Nothing:
    """
    results = list()
    user = gdb.labels.create('User')
    new_followings = list()
    for following in followings:
        new_followings.append(gdb.nodes.create(name=following.obj['username'], **following.obj))
    # new_followings = [db.nodes.create(name=following.obj['username'], **following.obj) for following in followings]
    user.add(*new_followings)


def put_followers_in_db(sc_username, sc_pass):
    client = soundcloud.Client(
        client_id='8e906fb7c324fc6640fd3fc08ef9d1ff',
        client_secret='aacd3a93bdfcf1dd65ed33497f091800',
        username=sc_username,
        password=sc_pass
    )
    my_user = get_my_user(client)
    user_id = my_user.id
    my_followings = get_all_followings(client)
    id_list = {follower.id: follower for follower in my_followings}
    print(', '.join([colored(x.username, 'red') for x in my_followings]) + ' added to database')

    # Neo4j Add Nodes
    add_followings(my_followings)

    edges_list = defaultdict(list)
    # API call to get all followers for edges
    for follower in my_followings:
        follower_id = follower.id
        try:
            curr_followings = get_all_followings(client, follower_id)
        except:
            continue
        existing_followings = [user for user in curr_followings if user.id in id_list.keys()]
        existing_ids = [user.id for user in existing_followings]

        # Do something with non existing followings
        not_existing_followings = [user for user in curr_followings if user.id not in id_list.keys()]
        not_existing_ids = [user.id for user in not_existing_followings]

        # Draw edges between all people in graph already
        edges_list[follower_id].extend(existing_followings)
        if existing_followings:
            # Everyone following someone else you follow
            for following in existing_followings:
                edges_list[follower_id].append(following)  # Custom
                print('{} -> {} added to database'.format(colored(follower.username, "red"),
                                                          colored(following.username, 'cyan')))
                add_edge(follower_id, following.id)


def add_edge(sid, tid):
    """
    :param sid: source id of the node
    :param tid:  target id of the node
    :return:
    """
    query = "MATCH (t:User {{id: {sid} }}), (p:User {{id: {tid} }}) " \
        "MERGE (p)-[r:FOLLOWS]->(t) " \
        "RETURN p, r, t".format(sid=sid, tid=tid)
    result = gdb.query(q=query, returns=(client.Node, client.Relationship, client.Node))
    return result

def add_edges(edges_list):
    """
    Edges
    """
    #embed()
    for source, targets in edges_list.items():
        for target in targets:
            add_edge(source, target.id)
