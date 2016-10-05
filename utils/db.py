from neo4j.v1 import GraphDatabase, basic_auth
from IPython import embed
from flask import g
import yaml

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "letmein"))


def get_db():
    return driver.session()
    #if not hasattr(g, 'neo4j_db'):
    #    g.neo4j_db = driver.session()
    #return g.neo4j_db


def add_followings(followings):
    """
    Nodes
    """
    db = get_db()
    results = list()
    for following in followings:
        query = "CREATE (n: User { {properties} } )".format(properties=yaml.dump(following.obj))
        """query = "CREATE (n: User {{ city:'{city}', comments_count:{comments_count}, " \
                "description:'{description}', discogs_name:'{discogs_name}', first_name:'{first_name}', followers_count:" \
                "{followers_count}, followings_count:{followings_count}, full_name:'{full_name}', id:{id}," \
                "kind:'{kind}', last_modified:'{last_modified}', last_name:'{last_name}', likes_count:{likes_count}," \
                "myspace_name:'{myspace_name}', online: '{online}', permalink: '{permalink}', permalink_url: '{permalink_url}'," \
                "plan:'{plan}', playlist_count: {playlist_count}, public_favorites_count: {public_favorites_count}," \
                "resposts_count: {reposts_count}, track_count: {track_count}, uri: '{uri}', name: '{username}', website: '{website}'," \
                "website_title:'{website_title}' }})".format(**following.obj)
        """
        results.append(db.run(query))
    embed()
    return results


def add_edges(edges_list):
    """
    Edges
    """
    db = get_db()
    for source, target in edges_list.items():
        query = "({source})-[:FOLLOWS]->({target})".format(source=source, target=target)
        results = db.run(query)
    return results


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