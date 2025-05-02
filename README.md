> ⚠️ **Heads up!**  
> This project hasn’t gone through a formal review yet—expect the occasional typo, rogue bug, or mysterious SQL gremlin. Proceed at your own risk 🕵️‍♂️🛠️

# Piscine Data Science

This repository contains all solutions for the **Piscine Data Science** program at 42, organized by days and modules:

- **Day 0 – Data Engineer**  
  Set up PostgreSQL & pgAdmin, import CSVs into the database.

- **Day 1 – Data Warehouse**  
  Clean, dedupe, and merge tables (customers & items).

- **Day 2 – Data Analyst (Data Viz)**  
  Generate charts: pie charts, time series, boxplots, histograms, elbow plots.

- **Day 3 – Clustering**  
  Use the elbow method and clustering algorithms to segment customers.

---

## 🛠 Prerequisites

- Docker & Docker Compose  
- Python 3.9+  
- (Optional) Virtual environment  
- Install Python dependencies:
  ```bash
  pip install -r requirements.txt
🚀 Quick Start
Bring up services

bash
Copiar
Editar
docker-compose up -d --build
Run SQL scripts
Load all three Data Warehouse exercises in one go:

bash
Copiar
Editar
docker-compose exec db psql -U bea -d piscineds \
  -f Data_Warehouse/ex01/create_customers.sql \
  -f Data_Warehouse/ex02/remove_duplicates.sql \
  -f Data_Warehouse/ex03/fusion.sql
Verify in pgAdmin
Open http://localhost:8081 (email admin@admin.com / password admin), connect to the db server, and browse the tables.

Generate visualizations
Each Data Viz subfolder has its script:

bash
Copiar
Editar
cd Data_viz/ex00
python pie.py --input_folder /data/customer --output ./output/pie.png

cd ../ex01
python chart.py --outdir ./output

cd ../ex02
python mustache.py --start 2022-10-01 --end 2023-02-28 --outdir ./output

cd ../ex03
python Building.py --start 2022-10-01 --end 2023-02-28 --outdir ./output --bins 10
Clustering

bash
Copiar
Editar
cd Data_viz/ex04
python elbow.py --outdir ./output

cd ../ex05
python clustering.py --outdir ./output
📂 Project Structure
sql
Copiar
Editar
.
├── Data_Warehouse
│   ├── ex01  Create customers table
│   ├── ex02  Remove duplicates
│   └── ex03  Merge customers + items
├── Data_viz
│   ├── ex00  Pie chart of event_type
│   ├── ex01  Time-series charts (customers & sales)
│   ├── ex02  Boxplots (“Mustache”)
│   ├── ex03  Histograms (frequency & spending)
│   ├── ex04  Elbow method
│   └── ex05  Customer clustering
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md   ← **This file**
📖 Module Descriptions
Day 0 – Data Engineer
ex00 & ex01: Docker Compose setup (PostgreSQL + pgAdmin).

ex02: Create tables directly in PostgreSQL from customer CSVs.

ex03: Automate table creation for all CSV files, plus items.

Day 1 – Data Warehouse
ex01: Merge monthly CSV data into a single customers table.

ex02: Remove exact and near-duplicate rows, creating customers_distinct and customers_dedup.

ex03: LEFT JOIN customers with items to form customers_full.

Day 2 – Data Analyst (Data Viz)
ex00: Pie chart of event_type (use all raw data as instructed).

ex01:

Daily unique customer counts (line chart).

Total monthly sales (bar chart).

Average spend per customer per month (area + line chart).

ex02:

Boxplot of all purchase prices.

Boxplot zoomed to a common range.

Boxplot of total spending per user with IQR whiskers.

ex03: Histograms of order frequency and total spending per user.

ex04: Elbow method to find optimal number of clusters (WSS vs. k).

ex05: Apply clustering algorithms to segment customers.




