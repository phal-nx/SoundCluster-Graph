from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "letmein"))


def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db


def add_followings(followings):
    """
    Nodes
    """
    db = get_db()
    for following_id, following in followings.items():
        query = "CREATE ({user_id}: User { {properties})".format(song_id = following_id, properties = following )
        results = db.run(query)
    return results


def add_edges(edges_list):
    """
    Nodes
    """
    db = get_db()
    for source, target in edges_list.items():
        query = 42 #"CREATE ({user_id}: User { {properties})".format(song_id = following_id, properties = following )
        results = db.run(query)
    return results


"""
Edges
"""
CREATE
  (Keanu)-[:ACTED_IN {roles:['Neo']}]->(TheMatrix),
  (Carrie)-[:ACTED_IN {roles:['Trinity']}]->(TheMatrix),
  (Laurence)-[:ACTED_IN {roles:['Morpheus']}]->(TheMatrix),
  (Hugo)-[:ACTED_IN {roles:['Agent Smith']}]->(TheMatrix),
  (AndyW)-[:DIRECTED]->(TheMatrix),
  (LanaW)-[:DIRECTED]->(TheMatrix),
  (JoelS)-[:PRODUCED]->(TheMatrix)