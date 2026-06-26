from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

engine = create_engine(
    "postgresql+psycopg2://postgres:pgadmin4@localhost:5432/telecom_analytics"
)

incident_types = [
    "Power Failure",
    "Fiber Cut",
    "Network Congestion",
    "Hardware Failure",
    "Software Bug",
    "Planned Maintenance"
]

severity_levels = ["Low", "Medium", "High", "Critical"]

with engine.connect() as conn:
    sites = conn.execute(
        text("SELECT site_id FROM sites")
    ).fetchall()

with engine.begin() as conn:

    query = text("""
        INSERT INTO incidents
        (
            site_id,
            incident_type,
            severity,
            start_time,
            end_time,
            status
        )

        VALUES
        (
            :site_id,
            :incident_type,
            :severity,
            :start_time,
            :end_time,
            :status
        )
    """)

    data = []

    for _ in range(700):

        site = random.choice(sites)[0]

        start = fake.date_time_between(
            start_date="-90d",
            end_date="now"
        )

        duration = random.randint(30, 600)

        end = start + timedelta(minutes=duration)

        data.append({

            "site_id": site,
            "incident_type": random.choice(incident_types),
            "severity": random.choice(severity_levels),
            "start_time": start,
            "end_time": end,
            "status": random.choice(
                ["Resolved", "Open", "In Progress"]
            )

        })

    conn.execute(query, data)

print("✅ Incidents inserted successfully!")