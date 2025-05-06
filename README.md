⚠️ Heads up!

This project hasn’t gone through a formal review yet—expect the occasional typo, rogue bug, or mysterious SQL gremlin. Proceed at your own risk 🕵️‍♂️🛠️

Piscine Data Science

This repository contains the solutions for the Piscine Data Science program at 42, organized by days and modules.

Modules

Day 0 – Data Engineer: Set up PostgreSQL & pgAdmin, import CSVs.

Day 1 – Data Warehouse: Clean, deduplicate, and merge tables (customers & items).

Day 2 – Data Analyst (Viz): Charts and visualizations (histograms, boxplots, time series, pie charts, Elbow Method, K-Means).

Day 3 – Data Scientist: Machine learning and model development (ex00: Histogram).

🛠 Prerequisites

Docker & Docker Compose

Python 3.9+

(Optional) Virtual environment

Install dependencies:

pip install -r requirements.txt

🚀 Quick Start

Start services

docker-compose up -d --build

Run Data Warehouse SQL

docker-compose exec db psql -U bea -d piscineds \
  -f Data_Warehouse/ex01/create_customers.sql \
  -f Data_Warehouse/ex02/remove_duplicates.sql \
  -f Data_Warehouse/ex03/fusion.sql

Verify in pgAdmin: http://localhost:8081 (admin@admin.com / admin)

Run Data Viz scripts (Day 2)

cd Data_viz
python ex00/pie.py --input_folder /data/customer --output ./ex00/output/pie.png
python ex01/chart.py --outdir ./ex01/output
python ex02/mustache.py --start 2022-10-01 --end 2023-02-28 --outdir ./ex02/output
python ex03/Building.py --start 2022-10-01 --end 2023-02-28 --outdir ./ex03/output
python ex04/elbow.py --start 2022-10-01 --end 2023-02-28 --outdir ./ex04/output
python ex05/clustering.py --start 2022-10-01 --end 2023-02-28 --outdir ./ex05/output --n_clusters 4

Run Data Scientist script (Day 3)

cd ../Data_scientist_1/ex00
python histogram.py --train Train_knight.csv --test Test_knight.csv --output Histogram.png

📂 Project Structure

.
├── Data_Warehouse/          # Day 1
│   ├── ex01/                # Create customers table
│   ├── ex02/                # Remove duplicates
│   └── ex03/                # Merge tables
├── Data_viz/                # Day 2
│   ├── ex00/                # Pie chart
│   ├── ex01/                # Time-series charts
│   ├── ex02/                # Boxplots (“Mustache”)
│   ├── ex03/                # Histograms (orders & spending)
│   ├── ex04/                # Elbow Method
│   └── ex05/                # K-Means Clustering
├── Data_scientist_1/        # Day 3
│   └── ex00/                # Histogram (knights’ skills & target)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

Day 2 – Data Viz Exercises

ex00: Pie Chart – Breakdown of event_type (Data_viz/ex00/pie.py).ex01: Time-Series – Daily unique customers, monthly sales, avg. spend (ex01/chart.py).ex02: Boxplots – Price distributions (ex02/mustache.py).ex03: Histograms – Order frequency & spending (ex03/Building.py).ex04: Elbow Method – WCSS vs. K clusters (ex04/elbow.py).ex05: K-Means Clustering – Customer segmentation (ex05/clustering.py).

Day 3 – Data Scientist (ex00: Histogram)

Directory: Data_scientist_1/ex00/

Description: Generate a combined histogram of knights’ features (skills) and the target “knight” (Force side) using Train_knight.csv and Test_knight.csv.

Output: Save figure as Histogram.*.




