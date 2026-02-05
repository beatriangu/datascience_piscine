#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
variances.py: Compute and plot cumulative variance percentages for features in Train_knight.csv.
Defaults to using Train_knight.csv located in Data_scientist_1/ex00 and saving variances.png in current directory.

Turn-in directory : ex02/
Files to turn in    : variances.*
Allowed functions   : All

Exercise 02:
  • Calculate the variance of each skill (feature)
  • Add up the variances to see how many components are needed to reach 90%
  • Display a graph representing the addition of your variances

For example:
Variances (Percentage):
[4.48960353e+01 1.84721038e+01 9.18338543e+00 ...]
Cumulative Variances (Percentage):
[ 44.89603531  63.36813909  72.55152452 ...]
7
"""
import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def parse_args():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Base project directory is two levels up (piscine_datascience)
    base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
    # Default CSV in Data_scientist_1/ex00
    default_csv = os.path.normpath(
        os.path.join(base_dir, 'Data_scientist_1', 'ex00', 'Train_knight.csv')
    )
    default_png = os.path.join(script_dir, 'variances.png')

    parser = argparse.ArgumentParser(
        description='Exercise 02: compute variances and plot cumulative percentages'
    )
    parser.add_argument(
        '--input-csv', '-i',
        dest='input_csv',
        default=default_csv,
        help=f'Path to input CSV (default: {default_csv})'
    )
    parser.add_argument(
        '--save-png', '-o',
        dest='save_png',
        default=default_png,
        help=f'Path to save the output plot PNG (default: {default_png})'
    )
    return parser.parse_args()


def load_data(path):
    if not os.path.isfile(path):
        sys.exit(f"Error: file not found: '{path}'")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        sys.exit(f"Error reading '{path}': {e}")
    if 'knight' in df.columns:
        df = df.drop(columns=['knight'])
    return df


def compute_variances(df):
    variances = df.var(axis=0)
    sorted_variances = variances.sort_values(ascending=False)
    total_var = sorted_variances.sum()
    variance_pct = (sorted_variances / total_var) * 100
    cumulative_pct = np.cumsum(variance_pct.values)
    return variance_pct.values, cumulative_pct


def main():
    args = parse_args()
    print(f"Loading data from: {args.input_csv}")
    df = load_data(args.input_csv)

    variance_pct, cumulative_pct = compute_variances(df)

    np.set_printoptions(precision=8, suppress=False)
    print('Variances (Percentage):')
    print(variance_pct)
    print('\nCumulative Variances (Percentage):')
    print(cumulative_pct)

    n90 = int(np.argmax(cumulative_pct >= 90) + 1)
    print(f"\nNumber of components to reach 90%: {n90}")

    fig, ax = plt.subplots(figsize=(10, 6))
    components = np.arange(1, len(cumulative_pct) + 1)
    # Continuous line without markers
    ax.plot(components, cumulative_pct, linestyle='-')
    ax.axhline(90, color='red', linestyle='--', linewidth=1)
    ax.set_xlabel('Number of Components')
    ax.set_ylabel('Cumulative Variance (%)')
    ax.set_title('Cumulative Variance Explained by Components')
    # Y-axis from 70 to 104
    ax.set_ylim(70, 104)
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(args.save_png, dpi=500, bbox_inches='tight', pad_inches=0)
    print(f"Plot saved to: {args.save_png}")
    plt.show()

if __name__ == '__main__':
    main()




