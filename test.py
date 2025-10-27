from neo4j import GraphDatabase
import openai

# Neo4j connection
driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", "umbc2024"))

# Example: Query for a student's relevant courses
def get_student_context(tx, student_name):
    query = """
    MATCH (s:Student {name: $student_name})-[:HAS_INTEREST]->(i:Interest),
          (s)-[:HAS_CGPA]->(cg:CGPA),
          (s)-[:ENROLLED_IN]->(c:Course)-[:OFFERED_IN]->(sem:Semester),
          (c)-[:TAUGHT_BY]->(p:Professor),
          (c)-[:IS_ELECTIVE]->(e:Elective)
    RETURN s.name, cg.value, i.name, c.name, sem.name, p.name, e.name
    """
    result = tx.run(query, student_name=student_name)
    return [record.data() for record in result]

with driver.session() as session:
    context = session.read_transaction(get_student_context, "Alice")

# Format context for LLM
context_str = "\n".join([
    f"Student: {row['s.name']}, CGPA: {row['cg.value']}, Interest: {row['i.name']}, "
    f"Course: {row['c.name']}, Semester: {row['sem.name']}, Professor: {row['p.name']}, Elective: {row['e.name']}"
    for row in context
])

# LLM prompt
prompt = f"""
Given the following student course selection context:
{context_str}
Suggest the best elective courses for the student, considering their interests, CGPA, semester, and professor expertise.
"""

# OpenAI GPT-4 call (replace with your API key)
openai.api_key = "YOUR_OPENAI_API_KEY"
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

print(response['choices'][0]['message']['content'])
