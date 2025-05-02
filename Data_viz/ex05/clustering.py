#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Viz - Exercise 05: Clustering

– Connects to PostgreSQL using SQLAlchemy and environment variables.
– Fetches purchase frequency and total spending for ALL users.
– Scales the frequency and total spending features.
– Applies K-Means clustering with a chosen number of clusters (e.g., 4).
– Assigns cluster labels back to the original user data.
– Analyzes cluster characteristics (average frequency, average monetary value).
– Assigns user-defined names and colors to clusters based on analysis.
– Creates graphic representations of the clusters (scatter plot, bar plots of averages)
  with specified names and colors.
– Saves the plots to the specified output directory.
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans # Import KMeans

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
        raise

def fetch_all_user_metrics(start, end):
    """
    Fetches purchase frequency (purchase_count) and total spending (total_spending)
    for ALL users with at least one purchase within the given date range.
    Returns a pandas DataFrame with 'user_id', 'purchase_count', 'total_spending'.
    """
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
        GROUP BY user_id;
    """)
    engine = get_engine()
    try:
        df = pd.read_sql_query(query, engine)
        print(f"Fetched metrics for {len(df)} unique users.")
        return df
    except SQLAlchemyError as e:
        print(f"Error fetching data from database: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description='Exercise 05: Customer Clustering')
    parser.add_argument('--start', default='2022-10-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', default='2023-02-28', help='End date (YYYY-MM-DD)')
    parser.add_argument('--outdir', default='.', help='Output directory for plots')
    # The number of clusters chosen from the Elbow Method analysis (e.g., 4)
    parser.add_argument('--n_clusters', type=int, default=4, help='Number of clusters to use for KMeans')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.outdir, exist_ok=True)

    try:
        # 1. Data Preparation: Fetch data
        df_metrics = fetch_all_user_metrics(args.start, args.end)

        if df_metrics.empty:
            print("No user metrics data found. Cannot perform clustering.")
            return

        # Select features for clustering (Frequency and Monetary Value)
        features = df_metrics[['purchase_count', 'total_spending']]

        # Handle potential NaNs or infinite values
        features = features.dropna()
        if features.empty:
             print("No valid features data after dropping NaNs. Cannot perform clustering.")
             return

        # Data Preparation: Scale features
        print("Scaling features...")
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        print("Features scaled.")

        # 2. & 3. Choose and Apply K-Means Clustering
        n_clusters = args.n_clusters # Use the number of clusters specified or default (4)
        print(f"Applying K-Means clustering with {n_clusters} clusters...")
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto', max_iter=300)

        # Fit K-Means to the scaled data
        kmeans.fit(scaled_features)
        print("K-Means clustering complete.")

        # 4. Assign Clusters to Users
        cluster_labels = kmeans.labels_

        df_clustered = df_metrics.copy() # Work on a copy
        df_clustered = df_clustered.loc[features.index].copy() # Ensure index alignment after dropna
        df_clustered['cluster'] = cluster_labels


        print(f"Assigned cluster labels to {len(df_clustered)} users.")


        # 5. Interpret and Characterize Clusters
        print("\nAnalyzing cluster characteristics...")

        # Calculate average original feature values per cluster
        cluster_summary_original = df_clustered.groupby('cluster')[['purchase_count', 'total_spending']].mean()

        print("\nAverage Original Feature Values per Cluster (Analyze this to map indices to names):")
        print(cluster_summary_original)

        # --- Assign Names and Colors ---
        # BASED ON YOUR ANALYSIS OF cluster_summary_original, map cluster indices (0, 1, 2, 3)
        # to your chosen descriptive names.
        # THIS MAPPING IS BASED ON YOUR HYPOTHETICAL ANALYSIS. VERIFY WITH YOUR DATA!
        cluster_names_map = {
             2: 'Inactive Customers',
             0: 'Standard Customers',
             3: 'Silver Customers',
             1: 'Gold Customers',
             # Ensure you have a mapping for ALL cluster indices (0, 1, ..., n_clusters-1)
        }

        # Define the color map from your chosen names to specific colors
        cluster_colors_map = {
            'Inactive Customers': 'green',
            'Standard Customers': 'blue',
            'Silver Customers': 'gray',
            'Gold Customers': 'gold', 
        }

        # Add the descriptive cluster names to the DataFrame
        df_clustered['cluster_name'] = df_clustered['cluster'].map(cluster_names_map)

        print("\nExample of users with assigned cluster names:")
        # Display sorted by cluster name for better readability
        print(df_clustered[['user_id', 'purchase_count', 'total_spending', 'cluster', 'cluster_name']].sort_values('cluster_name').head())


        # --- 6. Create Graphic Representations (Minimum 2 required) ---
        print("\nGenerating graphic representations...")
# Plot 1: Scatter plot of scaled features colored by cluster name
        plt.figure(figsize=(10, 8))
        # Use the cluster_name for hue and the cluster_colors_map for palette
        sns.scatterplot(
            x=scaled_features[:, 0], # Scaled Purchase Count
            y=scaled_features[:, 1], # Scaled Total Spending
            hue=df_clustered['cluster_name'], # Color by cluster name
            palette=cluster_colors_map, # Use the custom color map
            s=50, # Marker size for data points
            alpha=0.6, # Transparency for data points
            ax=plt.gca() # Use current axes
        )
        # Plot cluster centroids with more striking style
        # Need to get the names in the order of centroids for legend/labels if plotting names
        # For simplicity, plot centroids as generic 'Centroid' for now, colored by index palette
        # Or calculate centroid positions for each named cluster:
        centroid_names = [cluster_names_map.get(i, f'Cluster {i}') for i in sorted(cluster_names_map.keys())]
        # Get colors for centroids - could use a different palette or single striking color
        # Let's use a single striking color and larger size
        plt.scatter(
             kmeans.cluster_centers_[sorted(cluster_names_map.keys()), 0], # X-coords based on sorted indices in map
             kmeans.cluster_centers_[sorted(cluster_names_map.keys()), 1], # Y-coords based on sorted indices in map
             s=300, # <-- Increased Size of centroid markers
             c='magenta', # <-- Changed color to magenta
             marker='X', # Marker style for centroids
             edgecolor='black', # Keep edge color for definition
             label='Centroids', # Add a generic label for the legend
             zorder=5 # Ensure centroids are plotted on top
        )
        # If using named centroids legend, you might need to create custom legend entries


        plt.title('Customer Clusters (Scaled Features)')
        plt.xlabel('Scaled Purchase Count')
        plt.ylabel('Scaled Total Spending')
        plt.legend(title='Cluster') # Legend for clusters from scatterplot hue
        # Add a separate legend entry for Centroids if needed, or rely on the main legend
        # The 'label' in the centroid scatter call adds it to the legend
        plt.grid(True)
        output_scatter_path = os.path.join(args.outdir, 'Clustering_scatter_scaled.png')
        plt.savefig(output_scatter_path)
        plt.close()
        print(f"Saved scatter plot: {output_scatter_path}")

# ... (rest of the main function remains the same) ...


        # Plot 2: Bar plot of Average Original Purchase Count per Cluster
        plt.figure(figsize=(8, 6))
        # Order the bars by the desired names if needed, or use cluster index order
        # Plotting in cluster index order (0, 1, 2, 3) is default for groupby().plot()
        # Get colors in the order of cluster indices (0, 1, 2, 3)
        bar_colors_freq = [cluster_colors_map.get(cluster_names_map.get(i, f'Cluster {i}'), 'gray') for i in sorted(cluster_summary_original.index)]

        cluster_summary_original['purchase_count'].plot(kind='bar', color=bar_colors_freq, edgecolor='black', ax=plt.gca())
        plt.title('Average Purchase Count per Cluster')
        plt.xlabel('Cluster Group')
        plt.ylabel('Average Purchase Count')
        # Set x-axis labels to cluster names and rotate
        plt.xticks(ticks=np.arange(n_clusters), labels=[cluster_names_map.get(i, f'Cluster {i}') for i in sorted(cluster_summary_original.index)], rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        output_avg_freq_path = os.path.join(args.outdir, 'Clustering_avg_frequency.png')
        plt.savefig(output_avg_freq_path)
        plt.close()
        print(f"Saved average frequency bar plot: {output_avg_freq_path}")


        # Plot 3: Bar plot of Average Original Total Spending per Cluster
        plt.figure(figsize=(8, 6))
        # Get colors in the order of cluster indices (0, 1, 2, 3)
        bar_colors_monetary = [cluster_colors_map.get(cluster_names_map.get(i, f'Cluster {i}'), 'gray') for i in sorted(cluster_summary_original.index)]

        cluster_summary_original['total_spending'].plot(kind='bar', color=bar_colors_monetary, edgecolor='black', ax=plt.gca())
        plt.title('Average Total Spending per Cluster')
        plt.xlabel('Cluster Group')
        plt.ylabel('Average Total Spending (A$)')
        # Set x-axis labels to cluster names and rotate
        plt.xticks(ticks=np.arange(n_clusters), labels=[cluster_names_map.get(i, f'Cluster {i}') for i in sorted(cluster_summary_original.index)], rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        output_avg_monetary_path = os.path.join(args.outdir, 'Clustering_avg_monetary.png')
        plt.savefig(output_avg_monetary_path)
        plt.close()
        print(f"Saved average monetary bar plot: {output_avg_monetary_path}")

        print("\nExercise 05 Clustering analysis and visualization complete.")


    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
        # import traceback
        # traceback.print_exc()


if __name__ == '__main__':
    main()