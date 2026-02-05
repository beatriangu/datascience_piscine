#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Viz - Exercise 04: Elbow

– Connects to PostgreSQL using SQLAlchemy and environment variables.
– Fetches purchase frequency and total spending for ALL users.
– Scales the frequency and total spending features using StandardScaler.
– Applies K-Means clustering for a range of cluster numbers (k).
– Calculates the Within-Cluster Sum of Squares (WCSS) for each k.
– Plots the WCSS against the number of clusters (the Elbow Method curve).
– Saves the Elbow Method plot to the specified output directory.
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # Often used for plotting style
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans # Correct import for KMeans

# --- Database connection parameters from environment ---
DB_PARAMS = {
    "dbname":    os.getenv("POSTGRES_DB", "piscineds"),
    "user":      os.getenv("POSTGRES_USER", "bea"),
    "password":  os.getenv("POSTGRES_PASSWORD", "mysecretpassword"),
    "host":      os.getenv("DB_HOST", "localhost"),
    "port":      int(os.getenv("DB_PORT", "5432")),
}

def get_engine():
    """Crea un SQLAlchemy engine usando psycopg2."""
    # Use psycopg2 dialect explicitly for better compatibility
    url = (
        f"postgresql+psycopg2://{DB_PARAMS['user']}:{DB_PARAMS['password']}"
        f"@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
    )
    try:
        engine = create_engine(url)
        # Attempt to connect to validate credentials/host/port/dbname
        with engine.connect() as conn:
            print("Database connection successful!")
        return engine
    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")
        print(f"Please check database parameters: {DB_PARAMS}")
        # It's better to return None or raise a custom exception here
        # For this script's simplicity, we'll print and re-raise
        raise

def fetch_all_user_metrics(start, end):
    """
    Fetches purchase frequency (purchase_count) and total spending (total_spending)
    for ALL users with at least one purchase within the given date range.
    Returns a pandas DataFrame.
    """
    # Fetching data for all users with purchases
    query = text(f"""
        SELECT
            user_id,
            COUNT(*) AS purchase_count,
            SUM(purchase_price::numeric) AS total_spending
        FROM customers_full
        WHERE event_type = 'purchase'
          AND event_time >= '{start} 00:00:00'
          AND event_time <= '{end} 23:59:59'
          AND purchase_price IS NOT NULL
          AND user_id IS NOT NULL
        GROUP BY user_id; -- No HAVING clause to get all users with purchases
    """)
    engine = get_engine()
    try:
        df = pd.read_sql_query(query, engine)
        print(f"Fetched metrics for {len(df)} unique users with purchases in the period.")
        return df
    except SQLAlchemyError as e:
        print(f"Error fetching data from database: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description='Exercise 04: Elbow Method for Clustering')
    parser.add_argument('--start', default='2022-10-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', default='2023-02-28', help='End date (YYYY-MM-DD)')
    parser.add_argument('--outdir', default='.', help='Output directory for the elbow plot')
    # Define the range of clusters to test, e.g., from 1 to 10
    parser.add_argument('--k_max', type=int, default=10, help='Maximum number of clusters to test for Elbow Method')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.outdir, exist_ok=True)

    try:
        # 1. Fetch data for all users
        df_metrics = fetch_all_user_metrics(args.start, args.end)

        if df_metrics.empty:
            print("No user metrics data found in the specified date range. Cannot perform Elbow Method.")
            return

        # Select features for clustering (Frequency and Monetary Value)
        # Ensure only numerical columns are selected for scaling and clustering
        features = df_metrics[['purchase_count', 'total_spending']]

        # Handle potential NaNs or infinite values in features, although the SQL query should prevent this
        features = features.dropna()
        if features.empty:
             print("No valid features data after dropping NaNs. Cannot perform Elbow Method.")
             return

        # 2. Scale the features
        print("Scaling features...")
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        print("Features scaled.")

        # 3. Apply K-Means for a range of k values and calculate WCSS
        print(f"Performing K-Means for k = 1 to {args.k_max}...")
        wcss = [] # List to store WCSS (Inertia) values
        # Test k from 1 up to k_max
        k_range = range(1, args.k_max + 1)

        for k in k_range:
            # Initialize KMeans with n_clusters=k
            # random_state for reproducibility
            # n_init='auto' or an integer (e.g., 10) to run algorithm multiple times with different centroids
            # Changed n_init to 'auto' which is the default in recent sklearn versions, or can use 10
            kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto', max_iter=300)

            # Fit K-Means to the scaled data
            kmeans.fit(scaled_features)

            # Append the inertia (WCSS) to the list
            wcss.append(kmeans.inertia_)
            print(f"  k={k}: WCSS = {kmeans.inertia_:.2f}")


        # 4. Plot the Elbow Curve
        print("Generating Elbow Method plot...")
        plt.figure(figsize=(8, 6))
        plt.plot(k_range, wcss) # Plot WCSS vs k, with markers at each point
        plt.title('The Elbow Method')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
        plt.xticks(k_range) # Ensure x-ticks are at each integer k value tested
        plt.grid(True) # Add grid for better readability

        # 5. Save the Plot
        output_plot_path = os.path.join(args.outdir, 'elbow.png')
        plt.savefig(output_plot_path)
        plt.close() # Close the plot figure
        print(f"Elbow method plot saved to: {output_plot_path}")

        print("\nElbow Method analysis complete.")
        print(f"Inspect '{output_plot_path}' to identify the elbow point and choose the optimal number of clusters.")


    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
        # Detailed traceback if needed:
        # import traceback
        # traceback.print_exc()


if __name__ == '__main__':
    main()