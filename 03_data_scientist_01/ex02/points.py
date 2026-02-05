#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def find_csv_dir():
    """
    Search for the directory containing Train_knight.csv and Test_knight.csv:
      1) ex02/ex00 (inside the current folder)
      2) ../ex00    (sibling folder at the same level)
    Returns:
        Path to the directory if found.
    Raises:
        FileNotFoundError if neither location contains both CSVs.
    """
    script_dir = Path(__file__).resolve().parent  # e.g. .../Data_scientist_1/ex02
    candidates = [
        script_dir / "ex00",
        script_dir.parent / "ex00"
    ]
    for d in candidates:
        if (d / "Train_knight.csv").exists() and (d / "Test_knight.csv").exists():
            return d
    raise FileNotFoundError(f"Could not find Train_knight.csv and Test_knight.csv in any of: {candidates!r}")

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize DataFrame column names:
      - strip whitespace
      - convert to lowercase
      - replace spaces and hyphens with underscores
    Returns:
        A new DataFrame copy with normalized column names.
    """
    df = df.copy()
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(' ', '_')
          .str.replace('-', '_')
    )
    return df

def load_datasets():
    """
    Load the Train and Test datasets:
      1) Locate the ex00 directory.
      2) Read the header line from Test_knight.csv to get feature names.
      3) Load df_test using the default header.
      4) Load df_train without header, adding a 'knight' column.
      5) Normalize column names in both DataFrames.
    Returns:
        Tuple of (df_train, df_test).
    """
    csv_dir = find_csv_dir()
    test_csv = csv_dir / "Test_knight.csv"
    train_csv = csv_dir / "Train_knight.csv"

    # Read the first line of Test to get the feature names
    header = test_csv.open("r", encoding="utf-8").readline().strip().split(",")

    # Load test DataFrame with its built-in header
    df_test = pd.read_csv(test_csv)

    # Load train DataFrame without header, append 'knight'
    df_train = pd.read_csv(train_csv, header=None, names=header + ['knight'], skiprows=1)

    # Apply column-name normalization to both
    df_test = normalize_columns(df_test)
    df_train = normalize_columns(df_train)

    return df_train, df_test

def plot_jedi_info(df_test: pd.DataFrame):
    """
    Plot two scatter plots for the Test set (all Knights, no class separation):
      1) Stims vs. Empowered
      2) Deflection vs. Push
    Saves:
        jedi_stims_empowered.jpg
        jedi_deflection_push.jpg
    """
    # Stims vs. Empowered
    plt.figure()
    plt.scatter(
        df_test['empowered'], df_test['stims'],
        alpha=0.4, color='green', label='Knight'
    )
    plt.xlabel('Empowered')
    plt.ylabel('Stims')
    plt.legend()
    plt.savefig('jedi_stims_empowered.jpg', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close()

    # Deflection vs. Push
    plt.figure()
    plt.scatter(
        df_test['push'], df_test['deflection'],
        alpha=0.4, color='green', label='Knight'
    )
    plt.xlabel('Push')
    plt.ylabel('Deflection')
    plt.xlim(0.3, 3.9)
    plt.ylim(0.007, 0.082)
    plt.legend()
    plt.savefig('jedi_deflection_push.jpg', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close()

def plot_knight_info(df_train: pd.DataFrame):
    """
    Plot two scatter plots for the Train set, separated by class:
      1) Stims vs. Empowered for Jedi (blue) and Sith (red)
      2) Deflection vs. Push for Jedi (blue) and Sith (red)
    Saves:
        knight_stims_empowered.jpg
        knight_deflection_push.jpg
    """
    if 'knight' not in df_train.columns:
        print(
            "ERROR: 'knight' column not found. Available columns:",
            df_train.columns.tolist(),
            file=sys.stderr
        )
        return

    # Standardize class labels to lowercase and strip whitespace
    df_train['knight'] = df_train['knight'].astype(str).str.strip().str.lower()
    jedi = df_train[df_train['knight'] == 'jedi']
    sith = df_train[df_train['knight'] == 'sith']

    if jedi.empty or sith.empty:
        print(
            f"WARNING: Empty class data—Jedi({len(jedi)}), Sith({len(sith)})",
            file=sys.stderr
        )

    # Stims vs. Empowered by class
    plt.figure()
    plt.scatter(jedi['empowered'], jedi['stims'], alpha=0.4, color='blue', label='Jedi')
    plt.scatter(sith['empowered'], sith['stims'], alpha=0.4, color='red',  label='Sith')
    plt.xlabel('Empowered')
    plt.ylabel('Stims')
    plt.legend()
    plt.savefig('knight_stims_empowered.jpg', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close()

    # Deflection vs. Push by class
    plt.figure()
    plt.scatter(jedi['push'], jedi['deflection'], alpha=0.4, color='blue', label='Jedi')
    plt.scatter(sith['push'], sith['deflection'], alpha=0.4, color='red',  label='Sith')
    plt.xlabel('Push')
    plt.ylabel('Deflection')
    plt.legend()
    plt.savefig('knight_deflection_push.jpg', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close()

def main():
    """
    Main execution:
      1) Load train and test DataFrames.
      2) Print first few records and column lists for verification.
      3) Generate and save the required scatter plots.
    """
    df_train, df_test = load_datasets()

    print("Train — first few records:")
    print(df_train.head(), "\nColumns:", df_train.columns.tolist(), "\n")
    print("Test  — first few records:")
    print(df_test.head(),  "\nColumns:", df_test.columns.tolist(), "\n")

    plot_jedi_info(df_test)
    plot_knight_info(df_train)

if __name__ == '__main__':
    main()










