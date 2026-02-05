#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Viz - Exercise 02: My Beautiful Mustache

Generate three boxplots of purchase_price:
 1) mustache_overall.png: full distribution with outliers.
 2) mustache_common.png: common range without outliers.
 3) mustache_basket_filtered.png: average price per user (filtered 28–43),
    with outliers computed on the filtered data.
"""
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sqlalchemy import create_engine, text

# Database configuration via environment variables
DB_PARAMS = dict(
    dbname=os.getenv('POSTGRES_DB', 'piscineds'),
    user=os.getenv('POSTGRES_USER', 'bea'),
    password=os.getenv('POSTGRES_PASSWORD', 'mysecretpassword'),
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432')
)

def fetch_data(start, end):
    """
    Fetch purchase data from the database using SQLAlchemy and pandas.
    Returns a pandas DataFrame with 'price' and 'user_id' for purchase events.
    """
    sql = text(f"""
        SELECT purchase_price AS price, user_id
        FROM customers_full
        WHERE event_type='purchase'
          AND event_time BETWEEN '{start} 00:00:00' AND '{end} 23:59:59'
          AND purchase_price IS NOT NULL
          AND user_id IS NOT NULL;
    """)
    url = (
        f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}"
        f"@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
    )
    try:
        engine = create_engine(url)
        print(f"Connecting to database at {DB_PARAMS['host']}:{DB_PARAMS['port']}...")
        df = pd.read_sql_query(sql, engine)
        print(f"Fetched {len(df)} rows from the database.")
        return df
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        print(f"Attempted connection with params: {DB_PARAMS}")
        raise  # Re-raise the exception


def compute_stats(df: pd.DataFrame):
    """
    Calculate descriptive statistics for overall prices and average price per user.

    Returns:
      - stats: dict with descriptive statistics for overall prices
      - all_prices: numpy array of all purchase prices
      - avg_per_user: pandas Series of average purchase price per user
    """
    if df.empty or 'price' not in df.columns:
        print("Warning: No data or 'price' column available for statistics.")
        return {}, np.array([]), pd.Series(dtype=float)

    prices = df['price']

    # Calculate overall statistics
    stats = prices.describe(percentiles=[.25, .5, .75]).to_dict()

    # Calculate average price per user
    if 'user_id' not in df.columns:
        print("Warning: 'user_id' column not found. Cannot calculate average price per user.")
        avg_per_user = pd.Series(dtype=float)
    else:
        # Calculate the mean price for each user
        avg_per_user = df.groupby('user_id')['price'].mean()

    return stats, prices.values, avg_per_user


def plot_box(
    data, ax, title, xlabel, facecolor, edgecolor,
    showfliers, xlim=None, whis=1.5
):
    """Generate and style a horizontal box plot on a given axes (ax)."""
    # Ensure data is a numpy array for plotting
    if not isinstance(data, np.ndarray):
        data_np = np.array(data)
    else:
        data_np = data

    if data_np.size == 0:
        print(f"Warning: No data points to plot for '{title}'. Skipping.")
        ax.set_visible(False)  # Hide the axis if no data
        return

    # Define consistent styling properties
    boxprops = dict(facecolor=facecolor, edgecolor=edgecolor)
    whiskerprops = dict(color=edgecolor)
    capprops = dict(color=edgecolor)
    medianprops = dict(color=edgecolor, linewidth=2)  # Median line color and thickness

    # Styling for outliers (fliers)
    flierprops = dict(
        marker="o",
        markersize=5,
        markerfacecolor=edgecolor,
        markeredgecolor=edgecolor,
    )

    ax.boxplot(
        data_np,
        vert=False,            # Horizontal box plot
        patch_artist=True,     # Fill with color
        showfliers=showfliers, # Show/hide outliers
        whis=whis,             # Whiskers length
        boxprops=boxprops,
        whiskerprops=whiskerprops,
        capprops=capprops,
        medianprops=medianprops,
        flierprops=flierprops,
    )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_yticks([])  # Hide Y-axis ticks for single box plots

    if xlim is not None:
        ax.set_xlim(xlim)

    ax.grid(axis='x', linestyle='--', alpha=0.7)


def main():
    parser = argparse.ArgumentParser(
        description="Exercise 02: My Beautiful Mustache (boxplots)"
    )
    parser.add_argument('--start', default='2022-10-01',
                        help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end',   default='2023-02-28',
                        help='End date (YYYY-MM-DD)')
    parser.add_argument('--outdir', default='.',
                        help='Output directory for PNGs')
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.outdir, exist_ok=True)

    # 1) Fetch data
    df = fetch_data(args.start, args.end)

    if df.empty:
        print("No purchase data found in the specified date range. Cannot calculate stats or generate plots.")
        return

    # 2) Compute statistics and get data arrays
    stats, all_prices, avg_per_user = compute_stats(df)

    if all_prices.size == 0:
        print("No valid prices found after fetching. Cannot generate plots.")
        return

    print("\n--- Purchase Price Descriptive Statistics (Overall) ---")
    for k, v in stats.items():
        print(f"{k.capitalize():>6}: {v:.6f}")
    print("-----------------------------------------------------\n")

    print("\n--- Debug: Overall Purchase Prices Data Range ---")
    if all_prices.size > 0:
        print(f"Count: {all_prices.size}")
        print(f"Min: {np.min(all_prices):.4f}, Max: {np.max(all_prices):.4f}")
        print(
            f"Q1: {np.percentile(all_prices, 25):.4f}, "
            f"Median: {np.percentile(all_prices, 50):.4f}, "
            f"Q3: {np.percentile(all_prices, 75):.4f}"
        )
    else:
        print("No overall purchase price data.")
    print("-------------------------------------------------\n")

    print("\n--- Debug: Average Price Per User Data Range ---")
    if avg_per_user.size > 0:
        # Convert to numpy array for debug prints
        avg_per_user_np = avg_per_user.values
        print(f"Count: {avg_per_user_np.size}")
        print(f"Min: {np.min(avg_per_user_np):.4f}, Max: {np.max(avg_per_user_np):.4f}")
        print(
            f"Q1: {np.percentile(avg_per_user_np, 25):.4f}, "
            f"Median: {np.percentile(avg_per_user_np, 50):.4f}, "
            f"Q3: {np.percentile(avg_per_user_np, 75):.4f}"
        )
    else:
        print("No average price per user data.")
    print("------------------------------------------------\n")

    # 3) Generate box plots matching the expected examples

    # Box Plot 1: Overall purchase price (outliers shown)
    print("Generating Box Plot 1 (Overall Purchase Price Distribution)...")
    fig1, ax1 = plt.subplots(figsize=(8, 3))
    plot_box(
        all_prices, ax1,
        'Overall Purchase Price Distribution', 'Price (A$)',
        facecolor='lightgray', edgecolor='black', showfliers=True,
        xlim=(-70, 350), whis=1.5
    )
    fig1.tight_layout()
    fig1.savefig(os.path.join(args.outdir, 'mustache_overall.png'))
    print(f"Saved box plot: {os.path.join(args.outdir, 'mustache_overall.png')}")
    plt.close(fig1)

    # Box Plot 2: Common purchase price range (outliers hidden)
    print("Generating Box Plot 2 (Purchase Price Common Range)...")
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    plot_box(
        all_prices, ax2,
        'Purchase Price Distribution (Common Range)', 'Price (A$)',
        facecolor='lightgreen', edgecolor='darkgreen', showfliers=False,
        xlim=(-1, 13), whis=1.5
    )
    fig2.tight_layout()
    fig2.savefig(os.path.join(args.outdir, 'mustache_common.png'))
    print(f"Saved box plot: {os.path.join(args.outdir, 'mustache_common.png')}")
    plt.close(fig2)

    # Box Plot 3: Average price per user (filtered to 28–43 A$)
    # Outliers are computed within the filtered subset.
    if avg_per_user.size > 0:
        print("Generating Box Plot 3 (Average Purchase Price Per User Distribution - Filtered)...")

        # Filter average price per user to the target range (28 to 43)
        filtered_avg_price = avg_per_user[
            (avg_per_user >= 28) & (avg_per_user <= 43)
        ]

        if filtered_avg_price.empty:
            print("Warning: No average purchase prices found within the 28–43 range after filtering. Skipping Box Plot 3.")
        else:
            fig3, ax3 = plt.subplots(figsize=(8, 3))

            plot_box(
                filtered_avg_price.values, ax3,
                'Average Purchase Price Per User Distribution (Filtered 28–43 A$)', 'Price (A$)',
                facecolor='lightblue', edgecolor='darkblue', showfliers=True,
                xlim=None, whis=1.5
            )

            # Set x-axis limits based on the filtered data range + padding
            min_price_filtered = filtered_avg_price.min()
            max_price_filtered = filtered_avg_price.max()

            # Add 5% padding on both sides
            ax3.set_xlim(
                min_price_filtered - (max_price_filtered - min_price_filtered) * 0.05,
                max_price_filtered + (max_price_filtered - min_price_filtered) * 0.05
            )

            # Handle the edge case where the filtered set contains a single value
            if min_price_filtered == max_price_filtered:
                ax3.set_xlim(min_price_filtered - 1, max_price_filtered + 1)

            # Use integer ticks within the xlim range
            ax3.xaxis.set_major_locator(ticker.AutoLocator())
            ax3.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

            # Fallback for narrow ranges or too few ticks
            x_min, x_max = ax3.get_xlim()
            if x_max - x_min < 10 or len(ax3.get_xticks()) < 5:
                start_tick = int(np.floor(x_min / 2)) * 2
                end_tick = int(np.ceil(x_max / 2)) * 2
                manual_ticks = np.arange(start_tick, end_tick + 2, step=2)

                manual_ticks = manual_ticks[
                    (manual_ticks >= x_min - 1) & (manual_ticks <= x_max + 1)
                ]

                ax3.set_xticks(np.unique(np.round(manual_ticks).astype(int)))

            fig3.tight_layout()
            fig3.savefig(os.path.join(args.outdir, 'mustache_basket_filtered.png'))
            print(f"Saved box plot: {os.path.join(args.outdir, 'mustache_basket_filtered.png')}")
            plt.close(fig3)
    else:
        print("Skipping Box Plot 3: No average price data available (no users with purchases).")

    print(f"\nExercise 02 box plots generated successfully in: {args.outdir}")


if __name__ == '__main__':
    main()
