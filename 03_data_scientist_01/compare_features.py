#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import csv

# ─── Paths setup ───────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, 'ex00', 'Train_knight.csv'))
OUT_DIR = os.path.join(BASE_DIR, 'ex00', 'comparisons')
os.makedirs(OUT_DIR, exist_ok=True)

# ─── Helpers ───────────────────────────────────────────────────────────────────
def detect_delimiter(path):
    """Detect ',' vs ';' using csv.Sniffer."""
    with open(path, 'r', newline='') as f:
        sample = f.read(2048)
    try:
        return csv.Sniffer().sniff(sample, delimiters=[',', ';']).delimiter
    except csv.Error:
        return ','


def load_and_clean():
    """
    Load Train_knight.csv, map the 'knight' label, and fill missing values.

    - Detects the delimiter automatically
    - If 'knight' is missing from the header, re-reads without a header
    - Maps Jedi/Sith to 1/0, creates a string label for plots
    - Converts features to numeric and fills NaNs with column means
    """
    sep = detect_delimiter(CSV_PATH)
    df = pd.read_csv(CSV_PATH, sep=sep)

    # If there is no 'knight' column, re-read without header and assign names
    if 'knight' not in df.columns:
        FEATURES = [
            "Sensitivity", "Hability", "Strength", "Power", "Agility", "Dexterity",
            "Awareness", "Prescience", "Reactivity", "Midi-chlorien", "Slash", "Push",
            "Pull", "Lightsaber", "Survival", "Repulse", "Friendship", "Blocking",
            "Deflection", "Mass", "Recovery", "Evade", "Stims", "Sprint", "Combo",
            "Delay", "Attunement", "Empowered", "Burst", "Grasping"
        ]
        df = pd.read_csv(
            CSV_PATH,
            sep=sep,
            header=None,
            names=FEATURES + ['knight'],
            skiprows=1
        )

    # Map Knight labels to 0/1
    df['knight'] = df['knight'].astype(str).str.strip().map({'Jedi': 1, 'Sith': 0})

    # Convert numeric columns and fill NaNs
    feats = [c for c in df.columns if c != 'knight']
    df[feats] = df[feats].apply(pd.to_numeric, errors='coerce')
    df[feats] = df[feats].fillna(df[feats].mean())

    if df['knight'].isna().any():
        df['knight'].fillna(df['knight'].mode()[0], inplace=True)

    # Literal labels for legends
    df['knight_label'] = df['knight'].map({0: 'Sith', 1: 'Jedi'})
    return df


# ─── Visualizations ────────────────────────────────────────────────────────────
PALETTE = {'Sith': 'red', 'Jedi': 'blue'}


def density_plot(df, feature):
    plt.figure(figsize=(6, 4))
    ax = sns.kdeplot(
        data=df, x=feature, hue='knight_label',
        palette=PALETTE, common_norm=False, fill=True, alpha=0.5
    )
    plt.title(f'Density of {feature} by class')
    plt.xlabel(feature)
    plt.ylabel('Density')
    ax.legend(title='Class')

    filename = os.path.join(OUT_DIR, f'density_{feature}.png')
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


def box_plot(df, feature):
    plt.figure(figsize=(6, 4))
    ax = sns.boxplot(
        data=df, x='knight_label', y=feature,
        palette=PALETTE
    )
    plt.title(f'Boxplot of {feature} by class')
    plt.xlabel('Class')
    plt.ylabel(feature)
    ax.legend(['Sith', 'Jedi'], title='Class')

    filename = os.path.join(OUT_DIR, f'box_{feature}.png')
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


def violin_plot(df, feature):
    plt.figure(figsize=(6, 4))
    ax = sns.violinplot(
        data=df, x='knight_label', y=feature,
        palette=PALETTE, inner='quartile'
    )
    plt.title(f'Violin plot of {feature} by class')
    plt.xlabel('Class')
    plt.ylabel(feature)
    ax.legend(['Sith', 'Jedi'], title='Class')

    filename = os.path.join(OUT_DIR, f'violin_{feature}.png')
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


def compare_feature(df, feat):
    """Generate and save the three plots for a single feature."""
    density_plot(df, feat)
    box_plot(df, feat)
    violin_plot(df, feat)


def main():
    df = load_and_clean()
    for feat in ['Empowered', 'Stims', 'Deflection', 'Survival']:
        compare_feature(df, feat)
    print(f"Plots saved to {OUT_DIR}")


if __name__ == '__main__':
    main()
