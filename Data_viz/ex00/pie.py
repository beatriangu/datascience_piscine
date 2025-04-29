"""
Data Viz - Exercise 00: American Apple Pie

Guide: Read the monthly CSVs (Oct ’22 – Feb ’23) and generate a pie chart
showing the percentage of each event type.
"""
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


def load_data(folder_path):
    """Load all customer CSVs from the given folder into a single DataFrame."""
    # Patterns for files from Oct 2022 to Feb 2023
    pattern_2022 = os.path.join(folder_path, 'data_2022_*.csv')
    pattern_2023 = os.path.join(folder_path, 'data_2023_*.csv')
    files = sorted(glob.glob(pattern_2022) + glob.glob(pattern_2023))
    dfs = []
    for fp in files:
        df = pd.read_csv(fp, parse_dates=['event_time'])
        dfs.append(df)
    if not dfs:
        raise FileNotFoundError(f"No CSV files found in folder: {folder_path}")
    return pd.concat(dfs, ignore_index=True)


def plot_pie(df, output_path):
    """Create, save, and display a pie chart of event type distribution."""
    counts = df['event_type'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(
        counts,
        labels=counts.index,
        autopct='%1.1f%%',
        startangle=90
    )
    # plt.title('Event Type Distribution (Oct 2022 - Feb 2023)')
    plt.axis('equal')  # Ensure the pie is circular
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()  # Display the chart interactively
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Generate a pie chart of event types')
    parser.add_argument(
        '--input_folder',
        default='/Users/bea/Documents/PROYECTOS42/piscine_datascience/customer',
        help='Folder path where the customer CSVs are located'
    )
    parser.add_argument(
        '--output',
        default='pie_chart.png',
        help='Output file path for the pie chart (PNG)'
    )
    args = parser.parse_args()

    # Load data and generate pie chart
    df = load_data(args.input_folder)
    plot_pie(df, args.output)
    print(f"Pie chart saved to {args.output}")


if __name__ == '__main__':
    main()



