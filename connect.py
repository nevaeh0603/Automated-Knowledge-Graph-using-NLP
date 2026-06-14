from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URI=os.getenv("NEO4J_URI")
USERNAME=os.getenv("NEO4J_USERNAME")
PASSWORD=os.getenv("NEO4J_PASSWORD")

driver= GraphDatabase.driver(URI,auth=(USERNAME, PASSWORD))

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

def close_connection():
    driver.close()