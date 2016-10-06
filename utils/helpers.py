import operator
import networkx as nx
import cypher
import matplotlib.pyplot as plt
import soundcloud

def get_client(sc_username=None, sc_pass=None):
    client = soundcloud.Client(
        client_id='8e906fb7c324fc6640fd3fc08ef9d1ff',
        client_secret='aacd3a93bdfcf1dd65ed33497f091800',
        username=sc_username,
        password=sc_pass
    )
    return client

def get_all_followings(client, user_id=None):
    """
    Returns your followings if no user_id provided, else the users followings
    :param client: SC Client
    :param user_id: Optional userID to get
    :return:
    """
    # start paging through results, 200 at a time
    if user_id:
        response = client.get('/users/{}/followings'.format(user_id), limit=200,
                              linked_partitioning=1)
    else:
        response = client.get('/me/followings', limit=200,
                              linked_partitioning=1)
    followers = response.collection
    previous_result = followers
    # if there are more than 200 followers, keeps getting them
    while hasattr(previous_result, 'next_href'):
        next_followers = client.get(previous_result.next_href, limit=200, linked_partitioning=1)
        followers.extend(next_followers.collection)
        previous_result = followers
    return followers


def get_stats(g):
    """
    Generate stats based ond a graph and return a dict
    :param G: NX Graph
    :return: Dictionary of stats
    """
    degree = g.degree()
    info = nx.info(g)
    frequency_list = sorted(degree.items(), key=operator.itemgetter(1), reverse=True)
    cent = nx.degree_centrality(g)
    centrality = sorted(cent.items(), key=operator.itemgetter(1), reverse=True)
    #page = nx.pagerank(g)
    #page_rank = sorted(page.items(), key=operator.itemgetter(1), reverse=True)
    return locals()


def get_neo4_graph():
    query = "MATCH p = ()-[]-() RETURN p"
    results = cypher.run(query, conn="http://neo4j:letmein@localhost:7474")
    return results.get_graph()


def get_and_draw_neo4j_graph():
    g = get_neo4_graph()
    nx.draw(g)
    plt.show()


def get_neighbor_count():
    #Get neighbor count
    return cypher.run("MATCH (n)--(m) RETURN n.username, count(m) as neighbors",
                      conn="http://neo4j:letmein@localhost:7474")


def get_my_user(client):
    return client.get('/me')


def get_my_user_id(client):
    return client.get('/me').id


def get_neighbors(G, node):
    return G.neighbors(node)
