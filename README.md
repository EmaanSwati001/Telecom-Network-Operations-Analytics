# 📡 Telecom Network Operations Analytics

> **End-to-end data analytics pipeline for a fictional telecom operator — from synthetic data generation through PostgreSQL to an interactive Power BI dashboard covering 49 sites across 7 Pakistani cities.**

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Database Schema](#-database-schema)
- [Dashboard Screenshots](#-dashboard-screenshots)
- [SQL Analytics Queries](#-sql-analytics-queries)
- [Project Structure](#-project-structure)
- [How to Run](#-how-to-run)

---

## 🔍 Project Overview

This project simulates a real-world **telecom network operations analytics system** built for a fictional Pakistani telecom provider. The pipeline covers every stage of a data analytics workflow:

1. **Synthetic data generation** — 49 network sites, 106,000+ hourly performance logs, and 700 network incidents are procedurally generated using Python & Faker.
2. **Relational database** — all data is stored in a normalized PostgreSQL schema with three core tables.
3. **SQL analytics** — 10 hand-crafted analytical queries extract KPIs like average latency by city, CPU usage trends, peak traffic hours, and incident severity breakdowns.
4. **Power BI dashboard** — two interactive dashboards surface executive-level KPIs and granular site-level analysis.

**Key metrics tracked:**
- 📍 **49 sites** across Karachi, Lahore, Islamabad, Peshawar, Quetta, Faisalabad, Multan
- 📊 **106K+ performance log records** spanning 90 days of hourly telemetry
- 🚨 **700 network incidents** categorized by type, severity, and resolution status
- ⚡ **Average throughput: 319.26 Mbps** &nbsp;|&nbsp; **Average CPU: 42.70%**

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Database** | PostgreSQL 15 |
| **ORM / DB Driver** | SQLAlchemy + psycopg2 |
| **Data Generation** | Python 3, Faker |
| **Analytics (SQL)** | PostgreSQL SQL |
| **Visualization** | Microsoft Power BI Desktop |
| **Version Control** | Git / GitHub |

---

## ✨ Features

- 🏗️ **Automated data generation pipeline** — three independent Python scripts populate all three database tables from scratch with realistic, city-aware telemetry data
- 🌆 **City-aware simulation** — Karachi simulated as the busiest city (highest CPU & throughput), Islamabad with better latency; peak hours (18:00–22:00) reflected in all metrics
- ⚠️ **Realistic outage simulation** — 1% random outage probability per hourly log entry, producing critical CPU spikes, latency surges, and packet loss events
- 🔢 **Tri-level status classification** — logs automatically classified as `Healthy`, `Warning`, or `Critical` based on latency and packet loss thresholds
- 📊 **10 analytical SQL queries** covering site counts, city-level averages, traffic peaks, incident distributions, and throughput analysis
- 📈 **Two Power BI dashboards** — Executive Overview and Site-Level Analysis with cross-filtering capabilities
- 🔍 **Incident management** — 700 incidents across 6 types (Power Failure, Fiber Cut, Hardware Failure, Network Congestion, Software Bug, Planned Maintenance) with severity & resolution status

---

## 🗄 Database Schema

The database `telecom_analytics` contains three normalized tables:

### `sites` — Network Site Registry

| Column | Type | Description |
|---|---|---|
| `site_id` | SERIAL PRIMARY KEY | Auto-incremented unique site identifier |
| `site_code` | VARCHAR | Human-readable code, e.g. `KAR-001` |
| `city` | VARCHAR | City where the site is deployed |
| `region` | VARCHAR | Administrative region (Punjab, Sindh, KPK, etc.) |
| `latitude` | FLOAT | Geographic latitude |
| `longitude` | FLOAT | Geographic longitude |
| `installation_date` | DATE | Date the site was commissioned |
| `site_type` | VARCHAR | `Macro`, `Micro`, or `Small Cell` |

### `performance_logs` — Hourly Telemetry

| Column | Type | Description |
|---|---|---|
| `log_id` | SERIAL PRIMARY KEY | Auto-incremented log identifier |
| `site_id` | INTEGER (FK → sites) | Associated site |
| `log_time` | TIMESTAMP | UTC timestamp of the reading |
| `cpu_usage` | FLOAT | CPU utilization % |
| `memory_usage` | FLOAT | Memory utilization % |
| `latency_ms` | FLOAT | Network latency in milliseconds |
| `packet_loss` | FLOAT | Packet loss percentage |
| `throughput_mbps` | FLOAT | Network throughput in Mbps |
| `network_status` | VARCHAR | `Healthy` / `Warning` / `Critical` |

### `incidents` — Network Incident Log

| Column | Type | Description |
|---|---|---|
| `incident_id` | SERIAL PRIMARY KEY | Auto-incremented incident identifier |
| `site_id` | INTEGER (FK → sites) | Affected site |
| `incident_type` | VARCHAR | Power Failure, Fiber Cut, Hardware Failure, Network Congestion, Software Bug, Planned Maintenance |
| `severity` | VARCHAR | `Low` / `Medium` / `High` / `Critical` |
| `start_time` | TIMESTAMP | Incident start datetime |
| `end_time` | TIMESTAMP | Incident end datetime (duration: 30–600 min) |
| `status` | VARCHAR | `Open` / `In Progress` / `Resolved` |

### Entity Relationships

```
sites (site_id PK)
  ├── performance_logs (site_id FK)  — 1 site : many logs
  └── incidents (site_id FK)         — 1 site : many incidents
```

---

## 📸 Dashboard Screenshots

### Executive Dashboard — Real-time Performance & Incident Monitoring

KPI cards, average CPU by city, incident type breakdown, network status distribution, incident severity donut chart, and CPU trend over time.

![Executive Dashboard](screenshots/executive_dashboard.png.png)

---

### Site Analysis Dashboard — Drill-Down View

Filterable by city, region, and site type. Shows incident breakdown by type and severity, site inventory table, and performance distribution.

![Site Analysis Dashboard](screenshots/site_analysis.png.png)

---

## 🔎 SQL Analytics Queries

Ten analytical queries are stored in `sql_queries/` and can be loaded directly into Power BI or run via psql:

| # | Query File | Purpose |
|---|---|---|
| 01 | `01_total_sites.sql` | Total number of network sites |
| 02 | `02_sites_per_city.sql` | Sites deployed per city |
| 03 | `03_avg_cpu.sql` | Average CPU utilization across all sites |
| 04 | `04_avg_latency_by_city.sql` | Average latency broken down by city |
| 05 | `05_network_status_distribution.sql` | Count of Healthy / Warning / Critical log entries |
| 06 | `06_top_10_highest_latency_sites.sql` | Top 10 worst-performing sites by latency |
| 07 | `07_incident_count_by_type.sql` | Incident volume per incident type |
| 08 | `08_incident_severity_distribution.sql` | Incidents grouped by severity level |
| 09 | `09_average_throughput.sql` | Average network throughput in Mbps |
| 10 | `10_peak_traffic_hours.sql` | Hourly traffic patterns to identify peak load windows |

---

## 📁 Project Structure

```
Telecom Network Operations Analytics/
├── database/
│   └── schema.sql                        # DDL: CREATE TABLE for all 3 tables
│
├── data_generation/
│   ├── generate_sites.py                 # Populates 49 sites across 7 cities
│   ├── generate_logs.py                  # Generates 90 days of hourly performance logs
│   └── generate_incidents.py             # Generates 700 network incidents
│
├── analytics/
│   ├── calculate_kpis.py                 # KPI calculation logic
│   └── outage_prediction.py              # Outage prediction analytics
│
├── sql_queries/
│   ├── 01_total_sites.sql
│   ├── 02_sites_per_city.sql
│   ├── 03_avg_cpu.sql
│   ├── 04_avg_latency_by_city.sql
│   ├── 05_network_status_distribution.sql
│   ├── 06_top_10_highest_latency_sites.sql
│   ├── 07_incident_count_by_type.sql
│   ├── 08_incident_severity_distribution.sql
│   ├── 09_average_throughput.sql
│   └── 10_peak_traffic_hours.sql
│
├── dashboard/                            # Power BI .pbix file(s)
├── screenshots/                          # Dashboard screenshots
│   ├── executive_dashboard.png.png
│   └── site_analysis.png.png
│
└── exports/                              # CSV / Excel exports of query results
```

---

## 🚀 How to Run

### Prerequisites

- Python 3.9+
- PostgreSQL 15+ (running locally or via Docker)
- pgAdmin 4 (optional — for GUI inspection)
- Power BI Desktop (Windows, free) — to view the dashboards

### 1. Clone the Repository

```bash
git clone https://github.com/EmaanSwati001/Telecom-Network-Operations-Analytics.git
cd Telecom-Network-Operations-Analytics
```

### 2. Install Python Dependencies

```bash
pip install sqlalchemy psycopg2-binary faker
```

### 3. Set Up the Database

In pgAdmin or `psql`, create the database:

```sql
CREATE DATABASE telecom_analytics;
```

Then apply the schema:

```bash
psql -U postgres -d telecom_analytics -f database/schema.sql
```

> **Note:** All scripts connect to `postgresql+psycopg2://postgres:pgadmin4@localhost:5432/telecom_analytics`.  
> Update the connection string in each script if your PostgreSQL credentials differ.

### 4. Generate Synthetic Data

Run the three scripts **in order** — sites must exist before logs and incidents can reference them:

```bash
# Step 1: Generate 49 network sites (runs in seconds)
python data_generation/generate_sites.py

# Step 2: Generate ~106K hourly performance logs (may take 1-2 min)
python data_generation/generate_logs.py

# Step 3: Generate 700 network incidents
python data_generation/generate_incidents.py
```

Each script prints a ✅ confirmation on success.

### 5. Run SQL Analytics Queries

Execute any query against `telecom_analytics`:

```bash
psql -U postgres -d telecom_analytics -f sql_queries/04_avg_latency_by_city.sql
```

Or open and run the `.sql` files directly in **pgAdmin's Query Tool**.

### 6. Open the Power BI Dashboard

1. Launch **Power BI Desktop**
2. Go to **Home → Get Data → PostgreSQL database**
3. Server: `localhost` &nbsp;|&nbsp; Database: `telecom_analytics`
4. Load the tables: `sites`, `performance_logs`, `incidents`
5. Open the `.pbix` file from the `dashboard/` folder

---

## 👤 Author

**Emaan Swati**  
GitHub: [@EmaanSwati001](https://github.com/EmaanSwati001)

---

*Portfolio project demonstrating end-to-end data analytics skills: database design, Python ETL scripting, SQL analysis, and business intelligence dashboarding.*
