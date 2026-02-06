Data Science Foundations — End-to-End Data Lifecycle Project

This repository presents a structured Data Science Foundations project, covering the complete data lifecycle:

From database initialization and SQL data modeling
to exploratory data analysis, feature engineering, and classical machine learning.

The project is intentionally organized by real-world data roles, reflecting how modern data systems are built in professional environments.

🎯 Project Philosophy

Rather than approaching exercises as isolated tasks, this repository models the natural progression of a data product:

Data infrastructure

Data warehousing

Analytical exploration

Feature preparation

Model training & evaluation

Each stage builds on the previous one.

📂 Project Structure
.
├── 00_data_engineer
├── 01_data_warehouse
├── 02_data_analyst
├── 03_data_scientist_01
├── 04_data_scientist_02
├── db_init
├── src
├── scripts
├── etl
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── requirements.txt


Each directory represents a stage in the professional data workflow.

🧩 Modules Overview
00 — Data Engineer

Objective: Establish reliable and reproducible data infrastructure.

Key elements:

PostgreSQL initialization

Schema definition

Data availability checks

Docker-based reproducible environment

This stage focuses on creating a solid and production-aware foundation for downstream data processes.

01 — Data Warehouse

Objective: Transform raw datasets into structured, analysis-ready tables.

Main tasks:

Monthly data ingestion

Dataset consolidation

Deduplication strategies

SQL transformations

Creation of unified analysis tables

This stage ensures data consistency and integrity before analytical use.

02 — Data Analyst

Objective: Explore distributions and understand behavioral patterns.

Activities include:

Distribution analysis

Outlier detection

Boxplots and histograms

Frequency analysis

Clustering preparation (elbow method logic)

📊 Visual Insights
Purchase Price Distribution (ex02)

This boxplot highlights the distribution of purchase prices.

The visualization reveals:

A strong right-skewed distribution

Significant high-value outliers

Concentration of values within a lower price range

User Behavior Analysis (ex03)

These histograms focus on users whose total spending is below 225 A$, allowing clearer observation of general purchasing behavior.

Left: purchase frequency per user

Right: total spending per user

Key observations:

Most users make few purchases

Spending is concentrated in lower ranges

Clear long-tail behavior typical of transactional systems

03 — Data Scientist I

Objective: Prepare meaningful features for modeling.

Main steps:

Feature distribution analysis

Class comparison (Jedi vs Sith segmentation)

Normalization and standardization

Train/test split preparation

Preprocessing pipelines

This stage focuses on transforming raw analytical insights into model-ready datasets.

04 — Data Scientist II

Objective: Build and evaluate predictive models.

Techniques explored:

Decision Trees

K-Nearest Neighbors (KNN)

Ensemble voting strategies

Confusion matrices

Correlation heatmaps

Feature selection logic

The emphasis is on:

Model interpretability

Evaluation rigor

Bias awareness

Structured experimentation

🧠 Technical Design Decisions
✔ Clear separation of concerns

Each module corresponds to a specific data role.

✔ Reproducibility over artifacts

Plots and predictions are reproducible by executing scripts.
Generated outputs are not versioned systematically.

✔ Academic context, professional refactoring

Originally developed in an academic setting, this repository has been refactored and curated to meet professional portfolio standards.

🔁 Reproducibility & Execution

The repository does not include proprietary datasets.

However:

SQL scripts can be executed against a PostgreSQL instance.

Python scripts expect CSV inputs with documented schemas.

Visualizations and predictions are reproducible.

🐍 Python Environment Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

🐳 Docker (Optional)
docker compose up --build


This initializes the PostgreSQL service and project environment.

📌 Purpose of This Repository

This project serves as:

A structured technical portfolio

A demonstration of end-to-end data workflow understanding

A progression from Data Engineering to Data Science

A reproducible foundation for future modeling work

It reflects a production-aware mindset and a role-oriented approach to working with data.

⚠️ Disclaimer

This repository reflects a learning and consolidation process.

While the workflows are functional and structured for clarity, minor edge cases may still exist.
The focus is on conceptual rigor, structure, and reproducibility.

















