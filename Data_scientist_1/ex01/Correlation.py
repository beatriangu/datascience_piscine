#!/usr/bin/env python3

import pandas as pd
import os
import sys

# Correlation script for ex01
target_file = os.path.join('..', 'ex00', 'Train_knight.csv')
if not os.path.isfile(target_file):
    sys.exit(f"ERROR: no se encontró '{target_file}'")

# Detect delimiter: choose ';' if more semicolons than commas in first non-empty line
def detect_delimiter(path):
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                return ';' if line.count(';') > line.count(',') else ','
    return ','

delim = detect_delimiter(target_file)

# Read CSV, handling missing header for 'knight' column
try:
    df = pd.read_csv(target_file, sep=delim, low_memory=False)
except Exception as e:
    sys.exit(f"ERROR leyendo '{target_file}': {e}")

# If 'knight' not in columns, reload skipping first row and assigning names
FEATURES = [
    "Sensitivity", "Hability", "Strength", "Power", "Agility", "Dexterity",
    "Awareness", "Prescience", "Reactivity", "Midi-chlorien", "Slash", "Push",
    "Pull", "Lightsaber", "Survival", "Repulse", "Friendship", "Blocking",
    "Deflection", "Mass", "Recovery", "Evade", "Stims", "Sprint", "Combo",
    "Delay", "Attunement", "Empowered", "Burst", "Grasping"
]
expected_cols = FEATURES + ['knight']
if 'knight' not in df.columns or not set(expected_cols).issubset(df.columns):
    try:
        df = pd.read_csv(
            target_file,
            sep=delim,
            header=None,
            skiprows=1,
            names=expected_cols,
            low_memory=False
        )
    except Exception as e:
        sys.exit(f"ERROR recargando '{target_file}' con nombres asignados: {e}")
    # Validate again
    if 'knight' not in df.columns:
        sys.exit("ERROR: tras reasignar nombres no se encontró la columna 'knight'.")

# Convert all columns to numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
# Drop rows without a valid knight value
df = df.dropna(subset=['knight'])

# Compute correlation
corr_with_knight = df.corr()['knight']
# Sort descending
corr_sorted = corr_with_knight.sort_values(ascending=False)

# Print results
def main():
    for feature, value in corr_sorted.items():
        print(f"{feature:<12} {value:.6f}")

if __name__ == '__main__':
    main()



