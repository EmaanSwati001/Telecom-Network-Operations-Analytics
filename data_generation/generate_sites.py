from faker import Faker
import random
from sqlalchemy import create_engine, text

fake = Faker()

engine = create_engine(
    "postgresql+psycopg2://postgres:pgadmin4@localhost:5432/telecom_analytics"
)

cities = [
    "Islamabad",
    "Lahore",
    "Karachi",
    "Peshawar",
    "Quetta",
    "Faisalabad",
    "Multan"
]

regions = {
    "Islamabad": "North",
    "Lahore": "Punjab",
    "Karachi": "Sindh",
    "Peshawar": "KPK",
    "Quetta": "Balochistan",
    "Faisalabad": "Punjab",
    "Multan": "Punjab"
}

site_types = ["Macro", "Micro", "Small Cell"]

try:
    with engine.begin() as connection:

        for city in cities:
            for i in range(1, 8):

                code = city[:3].upper() + "-" + str(i).zfill(3)

                query = text("""
                    INSERT INTO sites
                    (site_code, city, region, latitude, longitude, installation_date, site_type)
                    VALUES
                    (:site_code, :city, :region, :lat, :lon, :install_date, :site_type)
                """)

                connection.execute(
                    query,
                    {
                        "site_code": code,
                        "city": city,
                        "region": regions[city],
                        "lat": round(random.uniform(24, 35), 6),
                        "lon": round(random.uniform(67, 74), 6),
                        "install_date": fake.date_between(start_date="-8y", end_date="today"),
                        "site_type": random.choice(site_types),
                    },
                )

    print("✅ Sites inserted successfully!")

except Exception as e:
    print("❌ Error:")
    print(e)