#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feature_Selection.py: Detect and remove multicollinearity via Variance Inflation Factor (VIF) and Tolerance using sklearn.

Turn-in directory : ex03/
Files to turn in    : Feature_Selection.*
Allowed functions   : All

This script:
 • Loads Train_knight.csv from Data_scientist_1/ex00
 • Computes and displays the VIF and Tolerance for each numeric feature
 • Iteratively removes features with VIF > 5 until all remaining features have VIF <= 5
 • Displays the final selected features and their VIFs and Tolerances

Usage:
    python Feature_Selection.py [--input-csv PATH]
"""
import os
import sys
import argparse
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def parse_args():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
    default_csv = os.path.normpath(
        os.path.join(base_dir, 'Data_scientist_1', 'ex00', 'Train_knight.csv')
    )
    parser = argparse.ArgumentParser(
        description="Exercise 03: feature selection via VIF and Tolerance"
    )
    parser.add_argument(
        '--input-csv', '-i',
        dest='input_csv',
        default=default_csv,
        help=f"Path to input CSV (default: {default_csv})"
    )
    return parser.parse_args()


def load_data(path):
    if not os.path.isfile(path):
        sys.exit(f"Error: file not found: '{path}'")
    df = pd.read_csv(path)
    if 'knight' in df.columns:
        df = df.drop(columns=['knight'])
    return df


def compute_vif(df):
    """
    Compute VIF and Tolerance for each feature in DataFrame df using sklearn LinearRegression.
    Returns a DataFrame with columns ['feature', 'VIF', 'Tolerance'].
    """
    features = df.columns.tolist()
    X = df.values
    vif_data = []
    for i, feature in enumerate(features):
        y = X[:, i]
        X_other = np.delete(X, i, axis=1)
        model = LinearRegression()
        model.fit(X_other, y)
        r2 = model.score(X_other, y)
        vif = 1.0 / (1.0 - r2) if r2 < 1.0 else np.inf
        tol = (1.0 - r2) if r2 < 1.0 else 0.0
        vif_data.append((feature, vif, tol))
    vif_df = pd.DataFrame(vif_data, columns=['feature', 'VIF', 'Tolerance'])
    return vif_df


def select_by_vif(df, threshold=5.0):
    """
    Iteratively remove features with VIF > threshold.
    Returns the list of selected features and their final VIF DataFrame.
    """
    features = df.columns.tolist()
    iteration = 1
    while True:
        vif_df = compute_vif(df[features])
        max_vif = vif_df['VIF'].max()
        if max_vif <= threshold:
            break
        drop_feature = vif_df.sort_values('VIF', ascending=False)['feature'].iloc[0]
        print(f"Iteration {iteration}: Dropping '{drop_feature}' with VIF={max_vif:.2f}")
        features.remove(drop_feature)
        iteration += 1
    final_vif = compute_vif(df[features])
    return features, final_vif


def main():
    args = parse_args()
    print(f"Loading data from: {args.input_csv}")
    df = load_data(args.input_csv)

    # Initial VIF and Tolerance
    initial_vif = compute_vif(df)
    print("\nInitial VIF and Tolerance:")
    print(initial_vif.to_string(index=False, float_format='%.2f'))

    # Feature selection
    selected_features, final_vif = select_by_vif(df)
    print("\nSelected features (VIF <= 5):")
    print(selected_features)
    print("\nFinal VIF and Tolerance:")
    print(final_vif.to_string(index=False, float_format='%.2f'))

if __name__ == '__main__':
    main()


