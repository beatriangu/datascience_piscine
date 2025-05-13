#!/usr/bin/env python3

import os
import sys
import csv
import pandas as pd

# ─── Definition of feature columns ──────────────────────────────────────────────
FEATURES = [
    "Sensitivity", "Hability", "Strength", "Power", "Agility", "Dexterity",
    "Awareness", "Prescience", "Reactivity", "Midi-chlorien", "Slash", "Push",
    "Pull", "Lightsaber", "Survival", "Repulse", "Friendship", "Blocking",
    "Deflection", "Mass", "Recovery", "Evade", "Stims", "Sprint", "Combo",
    "Delay", "Attunement", "Empowered", "Burst", "Grasping"
]

# ─── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # …/ex01
CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'ex00', 'Train_knight.csv'))
OUT_PATH = os.path.join(BASE_DIR, 'Correlation.txt')

# ─── Helper to detect CSV delimiter ─────────────────────────────────────────────
def detect_delimiter(path):
    """Detects whether the CSV uses comma or semicolon as delimiter."""
    with open(path, 'r', newline='') as f:
        sample = f.read(2048)
    try:
        return csv.Sniffer().sniff(sample, delimiters=[',', ';']).delimiter
    except csv.Error:
        return ','

# ─── Main routine ───────────────────────────────────────────────────────────────
def main():
    # Check that the input file exists
    if not os.path.isfile(CSV_PATH):
        sys.exit(f"ERROR: File not found: {CSV_PATH}")

    sep = detect_delimiter(CSV_PATH)
    cols = FEATURES + ['knight']

    # Read CSV, detect whether it has a header row
    df = pd.read_csv(CSV_PATH, sep=sep)
    if 'knight' not in df.columns:
        # No header present: read without header, assign column names, skip the first data row
        df = pd.read_csv(CSV_PATH, sep=sep, header=None, names=cols, skiprows=1)
    else:
        # Header present: keep only the columns we care about
        df = df[cols]

    print(f"DEBUG: Loaded {os.path.basename(CSV_PATH)} with sep='{sep}'")
    print("DEBUG: First rows:\n", df.head(3), "\n")

    # Map target: 'Jedi' -> 1, 'Sith' -> 0
    df['knight'] = (
        df['knight']
          .astype(str)
          .str.strip()
          .map({'Jedi': 1, 'Sith': 0})
    )

    # Convert feature columns to numeric; invalid parsing becomes NaN
    df[FEATURES] = df[FEATURES].apply(pd.to_numeric, errors='coerce')

    # Fill NaN in feature columns with each column's mean
    means = df[FEATURES].mean()
    df[FEATURES] = df[FEATURES].fillna(means)

    # If any 'knight' values are NaN, fill them with the mode
    if df['knight'].isna().any():
        mode_knight = df['knight'].mode()
        if not mode_knight.empty:
            df['knight'] = df['knight'].fillna(mode_knight[0])

    # Verify that no NaNs remain
    total_after = df.isna().sum().sum()
    if total_after > 0:
        print(f"WARNING: {total_after} NaN values remain after imputation")

    # Compute Pearson correlations and take absolute values
    corr = df.corr(numeric_only=True)['knight'].abs().sort_values(ascending=False)

    # Determine width for feature name column alignment
    max_feat_len = max(len(feat) for feat in corr.index)

    # Write results to output file with aligned formatting
    with open(OUT_PATH, 'w') as f:
        for feat, val in corr.items():
            f.write(f"{feat:<{max_feat_len}}  {val:>8.6f}\n")

    print(f"Saved correlation coefficients to {OUT_PATH}")

if __name__ == '__main__':
    main()



