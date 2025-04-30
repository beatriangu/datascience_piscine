#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Viz - Exercise 02: My Beautiful Mustache (English - SQLAlchemy)

– Connects to PostgreSQL using SQLAlchemy and environment variables.
– Fetches purchase event data (using 'purchase_price' column) for the specified date range.
– Calculates descriptive statistics for purchase prices.
– Calculates average purchase price per user.
– Generates three box plots based on PDF Subject examples (Exercise 02):
    1. Overall purchase price distribution (Image 8 style) in light gray/black, with outliers.
    2. Purchase price distribution focusing on a common range (Image 9 style) in green, without outliers.
    3. Average purchase price per user distribution (Filtered 28-43 A$) in blue, with outliers (calculated on filtered data).
"""
import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker # Import ticker for explicit tick control
from sqlalchemy import create_engine, text # Import text for explicit SQL string


# --- Database connection parameters - Read from Environment Variables ---
# This makes the script work correctly when run inside the Docker container
# or locally if env vars are set (e.g., via .env file or export)
DB_PARAMS = {
    "dbname":    os.getenv("POSTGRES_DB", "piscineds"), # Default to piscineds if not set
    "user":      os.getenv("POSTGRES_USER", "bea"),     # Default to bea if not set
    "password":  os.getenv("POSTGRES_PASSWORD", "mysecretpassword"), # Default if not set
    "host":      os.getenv("DB_HOST", "localhost"),    # Use DB_HOST env var, default to localhost
    "port":      os.getenv("DB_PORT", "5432"),         # Use DB_PORT env var, default to 5432
}


def fetch_data(start_date_str, end_date_str):
    """
    Fetches purchase data from the database using SQLAlchemy and pandas.
    Returns a pandas DataFrame.
    """
    # === >>> SQL Query with Corrected Column Name <<< ===
    # Selecting 'purchase_price' instead of 'price' from customers_full
    # Aliased as 'price' for consistency in Python code.
    query = text(f"""
        SELECT
            purchase_price AS price, -- <<< Corrected column name here, aliased as 'price' for consistency in Python
            user_id,
            event_time
        FROM customers_full
        WHERE event_type = 'purchase'
          AND event_time >= '{start_date_str} 00:00:00' -- Include start of day
          AND event_time <= '{end_date_str} 23:59:59'   -- Include end of day
          AND purchase_price IS NOT NULL -- Use purchase_price here too
          AND user_id IS NOT NULL;
    """)
    # === >>> End SQL Query <<< ===

    # Create SQLAlchemy engine
    # Using f-string for connection URL
    db_url = f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
    try:
        engine = create_engine(db_url)
        print(f"Connecting to database at {DB_PARAMS['host']}:{DB_PARAMS['port']}...")

        # Use the engine to read data into a pandas DataFrame
        # Use the text() construct for the query
        df = pd.read_sql_query(query, engine, parse_dates=['event_time'])

        print(f"Fetched {len(df)} rows from the database.")
        return df

    except Exception as e:
        print(f"Error fetching data from database: {e}")
        # Print DB_PARAMS for debugging connection issues
        print(f"Attempted connection with params: {DB_PARAMS}")
        raise # Re-raise the exception


def compute_stats(df: pd.DataFrame):
    """
    Calculates descriptive statistics and returns data arrays for plotting.
    Returns:
      - stats: dictionary of descriptive statistics for overall prices
      - all_prices: numpy array of all purchase prices
      - avg_per_user: numpy array of average purchase price per user
    """
    if df.empty or 'price' not in df.columns:
        print("Warning: No data or 'price' column available for statistics and plotting.")
        return {}, np.array([]), np.array([])

    prices = df['price'] # This column is now correctly named 'price' due to the SQL alias

    # Calculate overall statistics
    stats = prices.describe(percentiles=[.25, .5, .75]).to_dict()

    # Calculate average price per user
    # Ensure user_id exists and is suitable for grouping
    if 'user_id' not in df.columns:
         print("Warning: 'user_id' column not found. Cannot calculate average price per user.")
         avg_per_user = pd.Series(dtype=float) # Return empty Series
    else:
        # Group by user_id and calculate the mean price for each user
        # The SQL query already filters for non-null user_id and price
        avg_per_user = df.groupby('user_id')['price'].mean()


    return stats, prices.values, avg_per_user.values # Return numpy arrays


def plot_box(data, ax, title, xlabel, facecolor, edgecolor,
             showfliers, xlim=None):
    """Generates and styles a horizontal box plot onto a given axes (ax)."""
    if not isinstance(data, np.ndarray): # Ensure data is numpy array
        data_np = np.array(data)
    else:
        data_np = data

    if data_np.size == 0:
         print(f"Warning: No data points to plot for '{title}'. Skipping.")
         ax.set_visible(False) # Hide the axis if no data
         return

    # Define consistent styling properties
    boxprops = dict(facecolor=facecolor, edgecolor=edgecolor)
    whiskerprops = dict(color=edgecolor)
    capprops = dict(color=edgecolor)
    medianprops = dict(color=edgecolor, linewidth=2) # Median line color and thickness

    # Styling for outliers (fliers)
    flierprops = dict(marker="o", markersize=5, markerfacecolor=edgecolor, markeredgecolor=edgecolor)

    # Use plt.boxplot directly with the provided data
    ax.boxplot(data_np,
               vert=False, # Horizontal box plot
               patch_artist=True, # Fill with color
               showfliers=showfliers, # Show/hide outliers
               boxprops=boxprops,
               whiskerprops=whiskerprops,
               capprops=capprops,
               medianprops=medianprops,
               flierprops=flierprops
              )


    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_yticks([]) # Hide Y-axis ticks for single box plots

    if xlim is not None: # Use is not None check for xlim
        ax.set_xlim(xlim)

    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Saving logic is in main, not here


def main():
    parser = argparse.ArgumentParser(
        description="Exercise 02: My Beautiful Mustache (boxplots)")
    parser.add_argument('--start', default='2022-10-01',
                        help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end',   default='2023-02-28',
                        help='End date (YYYY-MM-DD)')
    parser.add_argument('--outdir', default='.',
                        help='Output directory for PNGs')
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.outdir, exist_ok=True)

    # 1. Fetch data
    df = fetch_data(args.start, args.end)

    if df.empty:
        print("No purchase data found in the specified date range. Cannot calculate stats or generate plots.")
        return

    # 2. Compute statistics and get data arrays
    stats, all_prices, avg_per_user = compute_stats(df)

    if all_prices.size == 0:
         print("No valid prices found after fetching. Cannot generate plots.")
         return

    print("\n--- Purchase Price Descriptive Statistics ---")
    for k, v in stats.items():
        print(f"{k.capitalize():>6}: {v:.6f}")
    print("-------------------------------------------\n")


    print("\n--- Debug: Overall Purchase Prices Data Range ---")
    if all_prices.size > 0:
        print(f"Count: {all_prices.size}")
        print(f"Min: {np.min(all_prices):.4f}, Max: {np.max(all_prices):.4f}")
        print(f"Q1: {np.percentile(all_prices, 25):.4f}, Median: {np.percentile(all_prices, 50):.4f}, Q3: {np.percentile(all_prices, 75):.4f}")
    else:
        print("No overall purchase price data.")
    print("-------------------------------------------------\n")

    print("\n--- Debug: Average Price Per User Data Range ---")
    if avg_per_user.size > 0:
        avg_per_user_np = np.array(avg_per_user) # Ensure it's a numpy array
        print(f"Count: {avg_per_user_np.size}")
        print(f"Min: {np.min(avg_per_user_np):.4f}, Max: {np.max(avg_per_user_np):.4f}")
        print(f"Q1: {np.percentile(avg_per_user_np, 25):.4f}, Median: {np.percentile(avg_per_user_np, 50):.4f}, Q3: {np.percentile(avg_per_user_np, 75):.4f}")
    else:
        print("No average price per user data.")
    print("------------------------------------------------\n")


    # 3. Generate Box plots matching PDF Examples

    # Box Plot 1: Overall Purchase Price (Image 8 style) - Light Gray/Black, Outliers shown
    print("Generating Box Plot 1 (Overall Purchase Price Distribution)...")
    fig1, ax1 = plt.subplots(figsize=(8, 3))
    plot_box(
        all_prices, ax1,
        'Overall Purchase Price Distribution', 'Price (A$)',
        facecolor='lightgray', edgecolor='black', showfliers=True,
        xlim=(-70, 350),
    )
    fig1.tight_layout()
    fig1.savefig(os.path.join(args.outdir, 'mustache_boxplot_overall_price.png'))
    print(f"Saved box plot: {os.path.join(args.outdir, 'mustache_boxplot_overall_price.png')}")
    plt.close(fig1)


    # Box Plot 2: Purchase Price Common Range (Image 9 style) - Green, Outliers hidden
    print("Generating Box Plot 2 (Purchase Price Common Range)...")
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    plot_box(
        all_prices, ax2,
        'Purchase Price Distribution (Common Range)', 'Price (A$)',
        facecolor='lightgreen', edgecolor='darkgreen', showfliers=False,
        xlim=(-1, 13),
    )
    fig2.tight_layout()
    fig2.savefig(os.path.join(args.outdir, 'mustache_boxplot_iqr.png'))
    print(f"Saved box plot: {os.path.join(args.outdir, 'mustache_boxplot_iqr.png')}")
    plt.close(fig2)


    # Box Plot 3: Average Price Per User (Filtered Range) - Blue
    # Using the filtering approach as requested
    if avg_per_user.size > 0:
        print("Generating Box Plot 3 (Average Purchase Price Per User Distribution - Filtered)...")

        # Convert to pandas Series for easy filtering
        avg_per_user_series = pd.Series(avg_per_user)

        # Filter the data to the desired range (28 to 43)
        filtered_avg_price = avg_per_user_series[
            (avg_per_user_series >= 28) & (avg_per_user_series <= 43)
        ]

        if filtered_avg_price.empty:
            print("Warning: No average purchase prices found within the 28-43 range. Skipping Box Plot 3.")
        else:
            fig3, ax3 = plt.subplots(figsize=(8, 3))

            # Define styling for outliers (fliers)
            flierprops = dict(marker="o", markersize=5, markerfacecolor='darkblue', markeredgecolor='darkblue')

            # Use plt.boxplot directly with the filtered data
            # Outliers are calculated based on the *filtered* data in this approach
            ax3.boxplot(filtered_avg_price,
                        vert=False,
                        patch_artist=True,
                        showfliers=True, # Show outliers within the filtered range
                        boxprops=dict(facecolor='lightblue', edgecolor='darkblue'),
                        whiskerprops=dict(color='darkblue'),
                        capprops=dict(color='darkblue'),
                        medianprops=dict(color='darkblue', linewidth=2),
                        flierprops=flierprops
                       )

            ax3.set_title('Average Purchase Price Per User Distribution (Filtered 28-43 A$)')
            ax3.set_xlabel('Price (A$)')
            ax3.set_yticks([]) # Hide Y-axis ticks

            # Set x-ticks based on the min and max of the filtered data, with a step of 2
            # Ensure ticks are integers and within a reasonable range
            min_price_filtered = int(filtered_avg_price.min())
            max_price_filtered = int(filtered_avg_price.max())
            tick_values = np.arange(min_price_filtered, max_price_filtered + 1, step=2)

            # Adjust ticks if the step is too large for the range or if only one tick
            if tick_values.size < 2 and max_price_filtered > min_price_filtered:
                 # If range is small but > 0, create a few ticks
                 tick_values = np.linspace(min_price_filtered, max_price_filtered, num=min(3, max_price_filtered - min_price_filtered + 1)) # Max 3 ticks for small range
                 tick_values = np.unique(np.round(tick_values).astype(int)) # Ensure unique integers
            elif tick_values.size == 0 and min_price_filtered == max_price_filtered:
                 tick_values = [min_price_filtered] # Handle single point case

            ax3.set_xticks(tick_values)

            # Set x-axis limits slightly wider than the filtered data range for padding
            ax3.set_xlim(min_price_filtered - 1, max_price_filtered + 1)


            ax3.grid(axis='x', linestyle='--', alpha=0.7)
            fig3.tight_layout()
            fig3.savefig(os.path.join(args.outdir, 'mustache_boxplot_avg_price_per_user_filtered.png'))
            print(f"Saved box plot: {os.path.join(args.outdir, 'mustache_boxplot_avg_price_per_user_filtered.png')}")
            plt.close(fig3)
    else:
         print("Skipping Box Plot 3: No average price data available (no users with purchases).")


    print(f"\nExercise 02 box plots generated successfully in: {args.outdir}")


if __name__ == '__main__':
    main()