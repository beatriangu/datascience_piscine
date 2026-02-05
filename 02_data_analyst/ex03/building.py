#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Viz - Exercise 03: Highest Building

- Connects to PostgreSQL using SQLAlchemy and environment variables.
- Fetches purchase event data (using the 'purchase_price' column),
  then computes purchase frequency and total spending per user.
- Filters to keep only users whose total spending is below 225 (as required).
- Generates two histograms with specific axis limits, ticks, and bar separation:
  1) Purchase frequency per user (x-axis 0–40, ticks 0,10,20,30,40;
     y-axis 0–70000, ticks 0,10000,...,60000).
  2) Total spending per user (filtered below 225), in turquoise
     (x-axis 0–200, ticks 0,50,100,150,200; y-axis configured as requested).
- Uses a whitegrid-like style and a light grey background.
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError  # Specific exception handling


# --- Database connection parameters from environment variables ---
DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB", "piscineds"),
    "user": os.getenv("POSTGRES_USER", "bea"),
    "password": os.getenv("POSTGRES_PASSWORD", "mysecretpassword"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
}


def get_engine():
    """Create a SQLAlchemy engine using psycopg2."""
    url = (
        f"postgresql+psycopg2://{DB_PARAMS['user']}:{DB_PARAMS['password']}"
        f"@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
    )
    try:
        engine = create_engine(url)
        # Attempt to connect to validate credentials/host/port/dbname
        with engine.connect():
            print("Database connection successful!")
        return engine
    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")
        print(f"Please check database parameters: {DB_PARAMS}")
        raise  # Stop execution if the connection fails


def fetch_metrics(start, end):
    """
    Return a DataFrame with:
      - user_id
      - purchase_count: number of purchases within the date range
      - total_spending: sum of purchase_price within the date range (filtered < 225)

    Note: The < 225 filter is applied at the SQL level via HAVING.
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
        GROUP BY user_id
        HAVING SUM(purchase_price::numeric) < 225;
    """)
    engine = get_engine()
    try:
        df = pd.read_sql_query(query, engine)
        print(f"Fetched {len(df)} rows for users with total spending < 225.")
        return df
    except SQLAlchemyError as e:
        print(f"Error fetching data from database: {e}")
        raise


def plot_histograms(df, outdir):
    """
    Draw two side-by-side histograms (seaborn style):
      - purchase_count (frequency)
      - total_spending (monetary value, already filtered < 225)

    Axes, ticks, and bar separation are configured according to the requirements.
    """
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Light grey background for both plots
    axes[0].set_facecolor('lightgrey')
    axes[1].set_facecolor('lightgrey')

    # --- Histogram 1: Purchase frequency (Chart 1) ---
    frequency_data = df['purchase_count']

    # X-axis limits and ticks (0 to 40, step 10)
    xlim_freq = (0, 40)
    xticks_freq = np.arange(0, 41, 10)

    # Y-axis limits and ticks (ticks to 60000, limit to 70000 for padding)
    ylim_freq = (0, 70000)
    yticks_freq = np.arange(0, 60001, 10000)

    # Bins for 5 bars across 0–40 (0, 8, 16, 24, 32, 40)
    bins_freq = np.arange(0, 41, 8)

    sns.histplot(
        frequency_data,
        bins=bins_freq,
        kde=False,
        color='steelblue',
        ax=axes[0],
        element='bars',
        shrink=0.9,  # Add separation between bars
    )
    axes[0].set_xlabel('Order Frequency per User')
    axes[0].set_ylabel('Number of Users')
    axes[0].set_title('Distribution of Purchase Counts (< 225 A$ Total Spending)')
    axes[0].set_xlim(xlim_freq)
    axes[0].set_xticks(xticks_freq)
    axes[0].set_ylim(ylim_freq)
    axes[0].set_yticks(yticks_freq)

    # --- Histogram 2: Total spending (Chart 2) ---
    monetary_data = df['total_spending']

    # X-axis limits and ticks (0 to 200, step 50)
    xlim_monetary = (0, 200)
    xticks_monetary = np.arange(0, 201, 50)

    # Y-axis limits and ticks (configured as requested in the original script)
    ylim_monetary = (0, 80000)
    yticks_monetary = np.arange(0, 80001, 5000)

    # Bins aligned with tick intervals (0–50, 50–100, 100–150, 150–200)
    bins_monetary = np.arange(0, 201, 50)

    axes[1].hist(
        monetary_data,
        bins=bins_monetary,
        color='turquoise',
        edgecolor='black',
        rwidth=0.9,  # Add separation between bars
    )
    axes[1].set_xlabel('Total Spending (A$) per User')
    axes[1].set_ylabel('Number of Users')
    axes[1].set_title('Distribution of Total Spending (< 225 A$)')
    axes[1].set_xlim(xlim_monetary)
    axes[1].set_xticks(xticks_monetary)
    axes[1].set_ylim(ylim_monetary)
    axes[1].set_yticks(yticks_monetary)

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
        # fetch_metrics already applies the < 225 total_spending filter
        df = fetch_metrics(args.start, args.end)

        if df.empty:
            print("No purchase data found in the specified date range with total spending < 225. Cannot generate plots.")
            return

        plot_histograms(df, args.outdir)
        print(f"\nExercise 03 histograms generated successfully in: {args.outdir}")

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")


if __name__ == '__main__':
    main()
