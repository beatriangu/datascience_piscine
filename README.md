> ⚠️ **Heads up!**
> This project hasn’t gone through a formal review yet—expect the occasional typo, rogue bug, or mysterious SQL gremlin. Proceed at your own risk 🕵️‍♂️🛠️

# Piscine Data Science

This repository contains the solutions for the **Piscine Data Science** program at 42, organized by days and modules.

---

## Modules

* **Day 0 – Data Engineer:** Set up PostgreSQL & pgAdmin, import CSVs into the database.
* **Day 1 – Data Warehouse:** Clean, deduplicate, and merge tables (customers & items).
* **Day 2 – Data Analyst (Data Viz):** Generation of data charts and visualizations. Includes histograms, boxplots, time series, pie charts, and **clustering methods (Elbow Method and K-Means)**.

---

## 🛠 Prerequisites

* Docker & Docker Compose
* Python 3.9+
* (Optional) Virtual environment
* Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Quick Start

1.  **Bring up services:**

    ```bash
    docker-compose up -d --build
    ```

2.  **Run SQL scripts:** Load the Data Warehouse exercises.

    ```bash
    docker-compose exec db psql -U bea -d piscineds \
      -f Data_Warehouse/ex01/create_customers.sql \
      -f Data_Warehouse/ex02/remove_duplicates.sql \
      -f Data_Warehouse/ex03/fusion.sql
    ```

3.  **Verify in pgAdmin:** Open `http://localhost:8081` (user `admin@admin.com` / password `admin`), connect to the database server, and explore the tables.

4.  **Generate visualizations:** Run the Python scripts for each Data Viz exercise.

    ```bash
    # Navigate to the Data_viz directory first
    # cd Data_viz/

    # Exercise 00
    python ex00/pie.py --input_folder /data/customer --output ./ex00/output/pie.png

    # Exercise 01
    python ex01/chart.py --outdir ./ex01/output

    # Exercise 02
    python ex02/mustache.py --start 2022-10-01 --end 2023-02-28 --outdir ./ex02/output

    # Exercise 03
    python ex03/Building.py --start 2022-10-01 --end 2023-02-28 --outdir ./ex03/output

    # Exercise 04 (Elbow Method)
    python ex04/elbow.py --start 2022-10-01 --end 2023-02-28 --outdir ./ex04/output

    # Exercise 05 (Clustering)
    python ex05/clustering.py --start 2022-10-01 --end 2023-02-28 --outdir ./ex05/output --n_clusters 4 # Adjust --n_clusters if needed
    ```

---

## 📂 Project Structure

```sql
.
├── Data_Warehouse/
│   ├── ex01/ # Create customers table
│   ├── ex02/ # Remove duplicates
│   └── ex03/ # Merge customers + items
├── Data_viz/
│   ├── ex00/ # Pie chart (event_type)
│   ├── ex01/ # Time-series charts (customers & sales)
│   ├── ex02/ # Boxplots (“Mustache”)
│   ├── ex03/ # Histograms (frequency & spending)
│   ├── ex04/ # Elbow method
│   └── ex05/ # Customer clustering
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md # This file
📊 Exercise Descriptions (Day 2 – Data Viz)
This section describes the Data Visualization exercises (Day 2), including customer clustering, which are part of the Day 2 of the Piscine. Each exercise generates charts that are saved in their respective output/ folder.

ex00: Pie Chart of event_type
(Data_viz/ex00/pie.py)

Generates a pie chart showing the percentage breakdown of each event type (event_type) in the raw customer data.

ex01: Time-Series Charts (Customers & Sales)
(Data_viz/ex01/chart.py)

Generates time-series plots analyzing customer behavior and sales over time:

Daily Unique Customers: A line plot showing the number of unique customers per day.

Total Monthly Sales: A bar chart illustrating the sum of total sales per month.

Average Spend per Customer/Month: An area + line chart visualizing the average amount spent per unique customer each month.

ex02: Boxplots (“Mustache”)
(Data_viz/ex02/mustache.py)

Creates styled boxplots to visualize the distribution of purchase prices:

Overall Purchase Price Distribution: Displays the distribution of all purchase prices, including outliers.

Purchase Price Distribution (Common Range): Focuses on a common range of purchase prices and typically hides outliers to show the main data concentration.

Basket Price per User: A boxplot representing the distribution of total spending per user. (Note: The specific implementation and filtering for this third boxplot may vary).

ex03: Histograms of Order Frequency & Spending
(Data_viz/ex03/Building.py)

Generates two histograms to show the distribution of customer behavior based on their purchase activity and spending. Data is filtered for users with total spending below 225 A$.

Order Frequency per User: A histogram showing how many customers made a certain number of purchases.
Total Spending per User: A histogram showing how many customers spent within specific monetary value ranges.
ex04: Elbow Method
(Data_viz/ex04/elbow.py)

Implements the Elbow Method to help determine the optimal number of clusters for customer segmentation. The script calculates the Within-Cluster Sum of Squares (WCSS) for K-Means clustering performed with a range of cluster numbers (k). The generated plot shows WCSS vs. k. The "elbow" point on this curve visually suggests a suitable number of clusters where adding more clusters provides diminishing returns in reducing within-cluster variance.

ex05: Customer Clustering
(Data_viz/ex05/clustering.py)

Performs customer segmentation using K-Means clustering based on scaled purchase frequency and total monetary value. It assigns each customer to a cluster and provides visualizations of the resulting customer groups.

The script analyzes the characteristics of each cluster (e.g., average frequency, average monetary value) to allow for meaningful interpretation and naming of the customer segments (e.g., 'New/Inactive Customers', 'Standard Customers', 'Silver Customers', 'Gold/Platinum Customers'). These names are then used in the plots along with specific colors.

Generated visualizations include:

Customer Clusters (Scaled Features): A scatter plot showing customers in the scaled feature space (frequency vs. monetary), colored by their assigned cluster name. Cluster centroids are marked.

Average Characteristics per Cluster: Bar plots illustrating the average original purchase count and average original total spending for each named cluster. These plots help in understanding the typical profile of customers within each segment.
(Note: The plot linked below shows average cluster characteristics, likely total spending, as represented by 'clustering_centroids.png' in your text).
(Another bar plot showing average purchase count per cluster is also generated by the script).

Remember to analyze the printed average cluster characteristics after the first run of clustering.py and update the cluster_names_map and cluster_colors_map dictionaries in the script based on your data's specific cluster averages before running it a second time to generate the final plots with correct names and colors.

Project Setup & Execution (Simplified)
For a simplified setup focused on the Data Viz part after prerequisites are met:

Ensure Database is Running and Loaded: Make sure your PostgreSQL database is accessible and contains the necessary customers_full table populated with data (refer to Day 0 and Day 1 exercises).
Set Environment Variables: Configure your database connection details as environment variables in your terminal session.
Run Scripts: Execute the Python scripts for each exercise within the Data_viz directory, providing the necessary arguments.
(Refer back to the "Quick Start" section for specific commands for each exercise).




