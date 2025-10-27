#!/usr/bin/env python3
"""
Nurse Well-being Knowledge Graph Data Generator

Generates node and relationship CSVs and Neo4j Cypher file for import.
Includes structured and unstructured nurse survey data, peer reviews,
team info, interventions, clinics, families, incidents, and comments.
"""

import random
import uuid
import csv
import os
from faker import Faker

# =============================================================================
#                                       CONFIGURATION
# =============================================================================

OUTPUT_DIR = "nurse_kg_data_v1"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_NURSES = 500
NUM_CLINICS = 20
NUM_INCIDENTS = 700
NUM_COMMENTS = 1500
NUM_TEAMS = 12
NUM_INTERVENTIONS = 10
NUM_FAMILIES = 300

departments = ["Emergency", "ICU", "Outpatient", "Pediatrics", "Surgical", "Oncology", "General Medicine", "Maternity"]
clinic_types = ["Hospital", "Clinic", "Community Center", "Long-term Care"]
intervention_types = [
    "Counseling", "Resilience Training", "Peer Review", "Staffing Policy", "Recognition Program",
    "Wellness Program", "Flexible Scheduling", "Supervisor Check-In", "Mental Health App", "Yoga Sessions"
]

fake = Faker(['en_US'])

# =============================================================================
#                              NODE GENERATION FUNCTIONS
# =============================================================================

def generate_clinics(n=NUM_CLINICS):
    return [{
        "clinic_id": str(uuid.uuid4()),
        "clinic_name": fake.company(),
        "clinic_type": random.choice(clinic_types),
        "location": fake.city(),
    } for _ in range(n)]

def generate_families(n=NUM_FAMILIES):
    return [{
        "family_id": str(uuid.uuid4()),
        "family_type": random.choice(["Single", "Single Parent", "Married", "Married with Children", "Extended"]),
        "num_dependents": random.randint(0, 5),
    } for _ in range(n)]

def generate_teams(n=NUM_TEAMS):
    return [{
        "team_id": str(uuid.uuid4()),
        "team_name": fake.bs().title(),
        "department": random.choice(departments),
    } for _ in range(n)]

def generate_interventions(n=NUM_INTERVENTIONS):
    return [{
        "intervention_id": str(uuid.uuid4()),
        "type": random.choice(intervention_types),
        "description": fake.sentence(nb_words=15),
        "scope": random.choice(["Department", "Hospital", "System"])
    } for _ in range(n)]

def generate_nurses(n, clinics, families, teams):
    nurses = []
    for _ in range(n):
        team = random.choice(teams)
        family = random.choice(families)
        clinic = random.choice(clinics)
        nurses.append({
            "nurse_id": str(uuid.uuid4()),
            "clinic_id": clinic["clinic_id"],
            "team_id": team["team_id"],
            "family_id": family["family_id"],
            "name": fake.name(),
            "age": random.randint(22, 65),
            "gender": random.choice(["Female", "Male", "Other"]),
            "ethnicity": fake.random_element(["White", "Black", "Asian", "Hispanic", "Other"]),
            "department": team["department"],
            "years_experience": random.randint(1, 39),
            "shift_type": random.choice(["Day", "Night", "Rotating", "Weekend"]),
            "marital_status": family["family_type"],
            "num_dependents": family["num_dependents"],
            "has_chronic_disease": random.choice([True, False, False]),
            "resilience_score": random.randint(1, 5),
            "peer_recognition": random.randint(1, 5),
            "job_satisfaction": random.randint(1, 5),
            "burnout_score": random.randint(1, 5),
            "stress_score": random.randint(1, 5),
            "physical_health": random.randint(1, 5),
            "mental_health": random.randint(1, 5),
            "violence_experience": random.choice([True, False, False]),
            "support_access": random.choice([True, False]),
            "financial_insecurity": random.choice([True, False]),
            "work_life_balance": random.randint(1, 5)
        })
    return nurses

def generate_incidents(n, clinics):
    return [{
        "incident_id": str(uuid.uuid4()),
        "clinic_id": random.choice(clinics)["clinic_id"],
        "department": random.choice(departments),
        "type": random.choice([
            "Equipment Failure", "Staff Shortage", "Patient Aggression", "Critical Decision",
            "Policy Change", "Breaks Missed", "Teamwork Success", "Bullying",
            "Error Reported", "Patient Death", "Praise Received"
        ]),
        "severity": random.randint(1, 5),
        "date": fake.date_this_year(),
    } for _ in range(n)]

def generate_comments(n, incidents, nurses):
    return [{
        "comment_id": str(uuid.uuid4()),
        "incident_id": random.choice(incidents)["incident_id"],
        "nurse_id": random.choice(nurses)["nurse_id"],
        "text": fake.sentence(nb_words=random.randint(10, 20)) + " " + random.choice([
            "Felt stressed and unsupported.", "Team pulled together and handled the crisis.",
            "Peer review highlighted strengths in leadership.", "Struggled communicating with management.",
            "Appreciated supervisor's recognition.", "Difficult shift but grateful for colleagues.",
            "Needed more support from peer team.", "Peer feedback: manages patient loads well."
        ]),
    } for _ in range(n)]

def generate_peer_ratings(nurses, teams):
    ratings = []
    for team in teams:
        members = [n for n in nurses if n['team_id'] == team['team_id']]
        for n1 in members:
            peers = [n2 for n2 in members if n1['nurse_id'] != n2['nurse_id']]
            sample_peers = random.sample(peers, min(3, len(peers)))
            for n2 in sample_peers:
                ratings.append({
                    "from_nurse_id": n1['nurse_id'],
                    "to_nurse_id": n2['nurse_id'],
                    "rating": random.randint(1, 5),
                    "review_comment": random.choice([
                        "Excellent teamwork.", "Needs to improve time management.",
                        "Great under pressure.", "Supportive to colleagues.",
                        "Effective leader.", "Could communicate more proactively."
                    ])
                })
    return ratings



# =============================================================================
#                         EXTENSIONS: NEW RESEARCH-BASED FIELDS
# =============================================================================

def enrich_nurse_with_research_factors(nurses):
    """Add psychological, behavioral, and workload-related factors."""
    positions = ["Staff Nurse", "Charge Nurse", "Administrator", "Educator/Researcher", "APRN"]
    substance_types = ["None", "Nicotine", "Alcohol", "Caffeine", "Energy Drinks", "Prescription Misuse"]

    for n in nurses:
        n.update({
            # Psychological distress & intention to leave
            "position_type": random.choice(positions),
            "psychological_distress": random.randint(1, 5),
            "intention_to_leave": random.choice([True, False, False]),
            "intention_reason": random.choice([
                "High stress", "Low pay", "Workload imbalance", "Better opportunity", "Personal reasons"
            ]),

            # Substance use & workload
            "substance_use": random.choices(substance_types, k=random.randint(1, 2)),
            "wsi_score": random.randint(1, 10),
            "workload_intensity": random.randint(1, 5),

            # Health-promoting schedules
            "preferred_shift_length": random.choice(["8-hour", "12-hour"]),
            "rest_hours_between_shifts": random.randint(8, 14),
            "sleep_quality": random.randint(1, 5),
            "fatigue_score": random.randint(1, 5),
            "autonomy_in_schedule": random.randint(1, 5),

            # Depression and suicide risk
            "depression_score": random.randint(1, 5),
            "suicide_risk_flag": random.choice([True, False, False, False]),
            "support_utilized": random.choice([True, False]),

            # Workplace and social environment
            "doctor_nurse_relationship": random.randint(1, 5),
            "patient_conflict_score": random.randint(1, 5),
            "income_satisfaction": random.randint(1, 5),
            "respect_perception": random.randint(1, 5),
            "work_family_conflict": random.randint(1, 5),
        })
    return nurses


def generate_misinformation_posts(n=200):
    """Generate synthetic health misinformation posts for LLM–KG integration."""
    topics = ["Vaccines", "Mental Health", "Pain Management", "Nutrition", "Substance Use"]
    return [{
        "post_id": str(uuid.uuid4()),
        "topic": random.choice(topics),
        "text": fake.sentence(nb_words=25),
        "credibility_score": round(random.uniform(0, 1), 2)
    } for _ in range(n)]


def generate_nurse_post_engagement(nurses, posts):
    """Connect nurses to misinformation posts."""
    relations = []
    for _ in range(len(nurses) // 2):
        n = random.choice(nurses)
        p = random.choice(posts)
        relations.append({
            "nurse_id": n["nurse_id"],
            "post_id": p["post_id"],
            "engagement_type": random.choice(["commented", "shared", "flagged", "ignored"])
        })
    return relations




# =============================================================================
#                             RELATIONSHIP GENERATION
# =============================================================================

def generate_relationships(nurses, incidents, comments, interventions):
    return {
        "nurse_intervention": [{"nurse_id": n["nurse_id"], "intervention_id": random.choice(interventions)["intervention_id"]} for n in nurses],
        "nurse_family": [{"nurse_id": n["nurse_id"], "family_id": n["family_id"]} for n in nurses],
        "nurse_incident": [{"nurse_id": random.choice(nurses)["nurse_id"], "incident_id": random.choice(incidents)["incident_id"]} for _ in range(NUM_INCIDENTS)],
        "comment_incident": [{"comment_id": c["comment_id"], "incident_id": c["incident_id"]} for c in comments],
        "nurse_clinic": [{"nurse_id": n["nurse_id"], "clinic_id": n["clinic_id"]} for n in nurses],
        "incident_clinic": [{"incident_id": i["incident_id"], "clinic_id": i["clinic_id"]} for i in incidents],
        "nurse_team": [{"nurse_id": n["nurse_id"], "team_id": n["team_id"]} for n in nurses],
    }

# =============================================================================
#                                CSV WRITING
# =============================================================================

def write_csv(filename, data):
    if not data:
        print(f"Warning: No data to write for {filename}")
        return
    with open(os.path.join(OUTPUT_DIR, filename), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"Wrote {filename} with {len(data)} records")

# =============================================================================
#                                MAIN
# =============================================================================

def main():
    clinics = generate_clinics()
    families = generate_families()
    teams = generate_teams()
    interventions = generate_interventions()
    nurses = generate_nurses(NUM_NURSES, clinics, families, teams)
    nurses = enrich_nurse_with_research_factors(nurses)  # <---- NEW LINE
    incidents = generate_incidents(NUM_INCIDENTS, clinics)
    comments = generate_comments(NUM_COMMENTS, incidents, nurses)
    peer_ratings = generate_peer_ratings(nurses, teams)

    posts = generate_misinformation_posts()               # <---- NEW ENTITY
    nurse_post_engagement = generate_nurse_post_engagement(nurses, posts)

    relationships = generate_relationships(nurses, incidents, comments, interventions)
    relationships["peer_ratings"] = peer_ratings
    relationships["nurse_post_engagement"] = nurse_post_engagement  # <---- NEW REL

    # Write nodes
    write_csv("clinics.csv", clinics)
    write_csv("families.csv", families)
    write_csv("teams.csv", teams)
    write_csv("interventions.csv", interventions)
    write_csv("nurses.csv", nurses)
    write_csv("incidents.csv", incidents)
    write_csv("comments.csv", comments)
    write_csv("peer_ratings.csv", peer_ratings)
    write_csv("misinformation_posts.csv", posts)          # <---- NEW NODE CSV

    # Write relationships
    for name, rel_data in relationships.items():
        write_csv(f"{name}.csv", rel_data)

    print(f"All enriched files generated under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
