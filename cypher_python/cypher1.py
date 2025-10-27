import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import pandas as pd

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(user, password))


with driver.session() as session:
    result = session.run("MATCH (n:Nurse) RETURN n LIMIT 5")
    df = pd.DataFrame([record["n"] for record in result])
print(df)




query = """
MATCH (n:Nurse)
RETURN n.nurse_id AS nurse_id, n.first_name AS first_name, n.last_name AS last_name, n.age AS age, n.full_time AS full_time
LIMIT 10
"""
with driver.session() as session:
    result = session.run(query)
    df = pd.DataFrame([record.data() for record in result])
print(df)
