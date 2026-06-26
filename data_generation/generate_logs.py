from sqlalchemy import create_engine, text
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

engine = create_engine(
    "postgresql+psycopg2://postgres:pgadmin4@localhost:5432/telecom_analytics"
)

# Get all site IDs
with engine.connect() as conn:
    result = conn.execute(text("SELECT site_id, city FROM sites"))
    sites = result.fetchall()

start_date = datetime.now() - timedelta(days=90)

records = []

for site in sites:

    site_id = site[0]
    city = site[1]

    current = start_date

    while current <= datetime.now():

        hour = current.hour

        # Base values
        cpu = random.uniform(20, 50)
        memory = random.uniform(30, 60)
        latency = random.uniform(15, 40)
        packet_loss = random.uniform(0, 1)
        throughput = random.uniform(150, 300)

        # Peak hours
        if 18 <= hour <= 22:
            cpu += random.uniform(20, 35)
            memory += random.uniform(15, 25)
            latency += random.uniform(10, 30)
            throughput += random.uniform(200, 500)

        # Karachi = busiest
        if city == "Karachi":
            cpu += 10
            throughput += 150

        # Islamabad = better latency
        if city == "Islamabad":
            latency -= 5

        # Random outage
        if random.random() < 0.01:
            cpu = random.uniform(90,100)
            latency = random.uniform(200,300)
            packet_loss = random.uniform(5,10)

        status = "Healthy"

        if latency > 120 or packet_loss > 3:
            status = "Warning"

        if latency > 220 or packet_loss > 7:
            status = "Critical"

        records.append({

            "site_id": site_id,
            "log_time": current,
            "cpu_usage": round(cpu,2),
            "memory_usage": round(memory,2),
            "latency_ms": round(latency,2),
            "packet_loss": round(packet_loss,2),
            "throughput_mbps": round(throughput,2),
            "network_status": status

        })

        current += timedelta(hours=1)

print(f"Generated {len(records)} records")

with engine.begin() as conn:

    query = text("""

        INSERT INTO performance_logs
        (
            site_id,
            log_time,
            cpu_usage,
            memory_usage,
            latency_ms,
            packet_loss,
            throughput_mbps,
            network_status
        )

        VALUES
        (
            :site_id,
            :log_time,
            :cpu_usage,
            :memory_usage,
            :latency_ms,
            :packet_loss,
            :throughput_mbps,
            :network_status
        )

    """)

    conn.execute(query, records)

print("✅ Performance logs inserted successfully!")