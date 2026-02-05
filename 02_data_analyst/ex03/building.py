#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Viz - Exercise 03: Highest Building

– Connects to PostgreSQL using SQLAlchemy and environment variables.
– Fetches purchase event data (using 'purchase_price' column),
  calculates purchase frequency and total spending per user.
– Filters total spending to be below 225 as per requirement.
– Generates two histograms with specified axis limits, ticks, and bar separation:
  1. Purchase frequency per user (x-axis 0-40, ticks 0,10,20,30,40; y-axis 0-70000, ticks 0,10000,...60000).
  2. Total spending per user (filtered below 225), in turquoise (x-axis 0-200, ticks 0,50,100,150,200; y-axis 0-45000, ticks 0,5000,...40000).
– Uses 'whitegrid' style and light grey background.
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError # Import for specific exception handling

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
        raise # Re-raise the exception to stop execution if connection fails


def fetch_metrics(start, end):
    """
    Devuelve un DataFrame con columnas:
      - user_id
      - purchase_count: número de compras en el rango dado
      - total_spending: suma de purchase_price en el rango dado (filtrado < 225)
    """
    # Added HAVING clause to filter total_spending below 225
    query = text(f"""
        SELECT
            user_id,
            COUNT(*) AS purchase_count,
            SUM(purchase_price::numeric) AS total_spending
        FROM customers_full
        WHERE event_type = 'purchase'
          AND event_time >= '{start} 00:00:00'
          AND event_time <= '{end} 23:59:59'
          AND purchase_price IS NOT NULL -- Ensure price is not null
          AND user_id IS NOT NULL -- Ensure user_id is not null
        GROUP BY user_id
        HAVING SUM(purchase_price::numeric) < 225; -- Filter groups based on total spending
    """)
    engine = get_engine()
    try:
        df = pd.read_sql_query(query, engine)
        print(f"Fetched {len(df)} rows for users with total spending < 225.")
        return df
    except SQLAlchemyError as e:
        print(f"Error fetching data from database: {e}")
        raise # Re-raise the exception


def plot_histograms(df, outdir):
    """
    Dibuja dos histogramas lado a lado con estilo seaborn:
      - purchase_count (Frequency)
      - total_spending (Monetary Value, filtered < 225)
    Configures axes, ticks, and bar separation as requested.
    """
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    # fondo gris claro
    axes[0].set_facecolor('lightgrey')
    axes[1].set_facecolor('lightgrey')

    # --- Histograma de frecuencia de compras (Chart 1) ---
    frequency_data = df['purchase_count']

    # Define specific x-axis limits and ticks as requested (0 to 40, step 10)
    xlim_freq = (0, 40)
    xticks_freq = np.arange(0, 41, 10) # Includes 40

    # Define specific y-axis limits and ticks as requested (0 to 60000, step 10000), y-axis limit up to 70000 for padding
    ylim_freq = (0, 70000)
    yticks_freq = np.arange(0, 60001, 10000) # Keep y-ticks up to 60000

    # Define bins to match the desired number of bars (5 bars covering 0-40)
    # This means 5 equal intervals from 0 to 40, so bin edges are 0, 8, 16, 24, 32, 40
    bins_freq = np.arange(0, 41, 8)


    sns.histplot(
        frequency_data,
        bins=bins_freq,
        kde=False,
        color='steelblue',
        ax=axes[0],
        element='bars', # Ensure bars element is used
        shrink=0.9 # Use shrink to add separation between bars
    )
    axes[0].set_xlabel('Order Frequency per User')
    axes[0].set_ylabel('Number of Users')
    axes[0].set_title('Distribution of Purchase Counts (< 225 A$ Total Spending)')
    axes[0].set_xlim(xlim_freq) # Set x-axis limits
    axes[0].set_xticks(xticks_freq) # Set x-ticks
    axes[0].set_ylim(ylim_freq) # Set y-axis limits for padding
    axes[0].set_yticks(yticks_freq) # Set y-ticks


    # --- Histograma de gasto total (Chart 2) ---
    monetary_data = df['total_spending']

    # Define specific x-axis limits and ticks as requested (0 to 200, step 50)
    xlim_monetary = (0, 200)
    xticks_monetary = np.arange(0, 201, 50) # Includes 200

    # Define specific y-axis limits and ticks as requested (0 to 40000, step 5000), y-axis limit up to 45000 for padding
    ylim_monetary = (0, 80000)
    yticks_monetary = np.arange(0, 80001, 5000) # Keep y-ticks up to 40000

    # Define bins to match the desired x-tick intervals (0-50, 50-100, 100-150, 150-200)
    bins_monetary = np.arange(0, 201, 50)


    axes[1].hist(
        monetary_data,
        bins=bins_monetary,
        color='turquoise', # Set color to turquoise
        edgecolor='black',
        rwidth=0.9 # Add separation between bars using rwidth
    )
    axes[1].set_xlabel('Total Spending (A$) per User')
    axes[1].set_ylabel('Number of Users')
    axes[1].set_title('Distribution of Total Spending (< 225 A$)')
    axes[1].set_xlim(xlim_monetary) # Set x-axis limits
    axes[1].set_xticks(xticks_monetary) # Set x-ticks
    axes[1].set_ylim(ylim_monetary) # Set y-axis limits for padding
    axes[1].set_yticks(yticks_monetary) # Set y-ticks


    plt.tight_layout()
    output_path = os.path.join(outdir, 'building_histograms.png')
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved histogram chart: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Exercise 03: Highest Building Histograms')
    parser.add_argument('--start', default='2022-10-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', default='2023-02-28', help='End date (YYYY-MM-DD)')
    parser.add_argument('--outdir', default='.', help='Output directory')
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    try:
        # The fetch_metrics function already filters total_spending < 225
        df = fetch_metrics(args.start, args.end)

        if df.empty:
            print("No purchase data found in the specified date range with total spending < 225. Cannot generate plots.")
            return

        # Call plot_histograms without the bins argument, as bins are defined inside
        plot_histograms(df, args.outdir)

        print(f"\nExercise 03 histograms generated successfully in: {args.outdir}")

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
        # More specific error handling could be added here based on potential issues

if __name__ == '__main__':
    main()
