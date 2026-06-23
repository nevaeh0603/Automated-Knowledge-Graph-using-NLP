from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from pyvis.network import Network

load_dotenv()

URI=os.getenv("NEO4J_URI")
USERNAME=os.getenv("NEO4J_USERNAME")
PASSWORD=os.getenv("NEO4J_PASSWORD")

driver= GraphDatabase.driver(URI,auth=(USERNAME, PASSWORD))

#stores triples in Neo4j
def create_relation(subject, relation, object):
    with driver.session() as session:
        query=f""" 
            MERGE (a:Entity {{name:$subject}})
            MERGE (b:Entity {{name:$object}})
            MERGE (a)-[:{relation}]->(b)
        """
        session.run(query, subject=subject, object=object)

def store_triples(triples):
    for subject, relation, object in triples:
        create_relation(subject, relation, object)

#Test Connection
def test_connection():
    with driver.session() as session:
        result=session.run("RETURN 'Connected' AS message")
        return result.single()["message"]

#Graph Stats   
def graph_stats():
    with driver.session() as session:
        nodes= session.run("""
                MATCH (n)
                RETURN count(n) AS total"""
                 ).single()["total"]
        
        relations= session.run("""
                            MATCH ()-[r]-> ()
                            RETURN count(r) AS total""").single()["total"]
        return nodes, relations

#Generate Graph
def generate_graph():
    net= Network(
        height="500px",
        width="100%",
        bgcolor="white",
        directed=True
    )

    query="""
        MATCH (a)-[r]->(b)
        RETURN a.name AS source, type(r) AS relation, b.name AS target
    """
    with driver.session() as session:
        count=0
        results= session.run(query)
        for record in results:
            source= record["source"]
            relation= record["relation"]
            target= record["target"]

            net.add_node(source, label=source)
            net.add_node(target, label=target)
            net.add_edge(source, target, label=relation)
            count+=1
            print("Total Relations Loaded: ", count)
            net.save_graph("graph.html")

            return "graph.html"