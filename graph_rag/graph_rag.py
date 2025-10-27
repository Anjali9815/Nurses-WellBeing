from neo4j import GraphDatabase
import requests  # or Google's official SDK for Gemini
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import pandas as pd

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


driver = GraphDatabase.driver(uri, auth=(user, password))


# Gemini API call placeholder
def gemini_generate(prompt):
    url = "https://your-realm-specific-gemini-api-url"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {
        "model": "gemini-2.0-flash-exp",
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]



def graph_rag_query(user_question):
    # Translate user question to Cypher or select Cypher query template
    cypher_query = """
    MATCH (n:Nurse)-[:WORKED]->(s:Shift)
    WHERE s.shift_type = 'Night'
    RETURN n.first_name, n.last_name, s.date, s.hours LIMIT 10
    """
    with driver.session() as session:
        result = session.run(cypher_query)
        graph_context = "\n".join(str(record.data()) for record in result)

    # Build prompt for Gemini
    prompt = f"Graph data:\n{graph_context}\nQuestion: {user_question}\nAnswer:"
    answer = gemini_generate(prompt)
    return answer

def format_result_as_text(records):
    lines = []
    for r in records:
        nurse = r.get("n.first_name", "") + " " + r.get("n.last_name", "")
        date = r.get("s.date", "")
        hours = r.get("s.hours", "")
        lines.append(f"Nurse {nurse} worked a shift on {date} lasting {hours} hours.")
    return "\n".join(lines)


# Example Usage
user_query = "Who worked night shifts recently?"
print(format_result_as_text(graph_rag_query(user_query)))
