from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URI=os.getenv("NEO4J_URI")
USERNAME=os.getenv("NEO4J_USERNAME")
PASSWORD=os.getenv("NEO4J_PASSWORD")

driver= GraphDatabase.driver(URI,auth=(USERNAME, PASSWORD))

def create_node(tx):
    query=""" 
    CREATE (a: PERSON {name: 'Roald Dahl'})
    CREATE (b: BOOK {name: "The BFG"})
    CREATE (a)-[:WROTE]->(b)
    RETURN a,b
    """
    tx.run(query)

with driver.session() as session:
    session.execute_write(create_node)
    
print("Node created Successfully")
driver.close()