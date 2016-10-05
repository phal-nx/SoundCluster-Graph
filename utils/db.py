from neo4jrestclient.client import GraphDatabase
from IPython import embed
from flask import g
import yaml

db = GraphDatabase("http://localhost:7474", username="neo4j", password="letmein")




def add_followings(followings):
    """
    Nodes
    """
    results = list()
    user = db.labels.create('User')
    new_followings = list()
    for following in followings:
        new_followings.append(db.nodes.create(name=following.obj['username'], **following.obj))
    # new_followings = [db.nodes.create(name=following.obj['username'], **following.obj) for following in followings]

    user.add(*new_followings)
    return results


def add_edges(edges_list):
    """
    Edges
    """
    embed()
    for source, target in edges_list.items():
        id_index = db.nodes.indexes.create("id")
        try:
            src = next(id_index['id'][source])
        except StopIteration:
            print("stop iteration")
            continue
        except:
            raise
        for tgt in target:
            trget = id_index.get('id')[tgt.id] # Figure out indexing
            src.relationships.create("Follows", next(trget))


"""
Edges

CREATE
  (Keanu)-[:ACTED_IN {roles:['Neo']}]->(TheMatrix),
  (Carrie)-[:ACTED_IN {roles:['Trinity']}]->(TheMatrix),
  (Laurence)-[:ACTED_IN {roles:['Morpheus']}]->(TheMatrix),
  (Hugo)-[:ACTED_IN {roles:['Agent Smith']}]->(TheMatrix),
  (AndyW)-[:DIRECTED]->(TheMatrix),
  (LanaW)-[:DIRECTED]->(TheMatrix),
  (JoelS)-[:PRODUCED]->(TheMatrix)
"""