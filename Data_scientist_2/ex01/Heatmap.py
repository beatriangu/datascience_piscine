#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heatmap.py: Calculate and plot a correlation heatmap for numerical features in Train_knight.csv.
Defaults to using Train_knight.csv located in ../ex00 and saving heatmap.png.

Usage:
    python Heatmap.py [--input-csv PATH] [--save-png PATH]
"""
import os
import argparse
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def parse_args():
    # Determine script directory and default CSV path in sibling Data_scientist_1/ex00
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))  # .../piscine_datascience
    default_csv = os.path.normpath(os.path.join(base_dir, 'Data_scientist_1', 'ex00', 'Train_knight.csv'))
    default_png = os.path.join(script_dir, 'heatmap.png')

    parser = argparse.ArgumentParser(
        description="Exercise ex01: compute and display a heatmap of feature correlations"
    )
    parser.add_argument(
        '--input-csv',
        dest='input_csv',
        default=default_csv,
        help=f"Path to input CSV (default: {default_csv})"
    )
    parser.add_argument(
        '--save-png',
        dest='pngpath',
        default=default_png,
        help=f"Path to save the heatmap PNG (default: {default_png})"
    )
    return parser.parse_args()

def load_data(path):
    if not os.path.isfile(path):
        sys.exit(f"Error: file not found: '{path}'")
    try:
        return pd.read_csv(path)
    except Exception as e:
        sys.exit(f"Error loading '{path}': {e}")

def main():
    args = parse_args()
    print(f"Loading data from: {args.input_csv}")
    df = load_data(args.input_csv)

    # Filter numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        sys.exit("Error: dataset must contain at least two numeric columns.")

    # Compute correlation matrix
    corr = numeric_df.corr(method='pearson')

    # Plot heatmap
    plt.figure(figsize=(10, 8))
    # Set overall font sizing (optional)
    sns.set(font_scale=1.0)
    heatmap = sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 5},  # smaller annotation font
        cmap='coolwarm',
        vmin=-1,
        vmax=1,
        linewidths=0.30,
        cbar_kws={"shrink": 0.8}
    )
    heatmap.set_title('Heatmap of Pearson Correlation Coefficients', pad=16)
    plt.tight_layout()

    # Save figure
    plt.savefig(args.pngpath, dpi=150)
    print(f"Heatmap saved to: {args.pngpath}")

if __name__ == '__main__':
    main()




