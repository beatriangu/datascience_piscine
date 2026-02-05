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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
    default_csv = os.path.normpath(
        os.path.join(base_dir, 'Data_scientist_1', 'ex00', 'Train_knight.csv')
    )
    default_png = os.path.join(script_dir, 'heatmap.png')

    parser = argparse.ArgumentParser(
        description="Exercise ex01: compute and display a heatmap of feature correlations"
    )
    parser.add_argument(
        '--input-csv', dest='input_csv', default=default_csv,
        help=f"Path to input CSV (default: {default_csv})"
    )
    parser.add_argument(
        '--save-png', dest='pngpath', default=default_png,
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

    # Convertir la columna 'knight' a valores numéricos
    if 'knight' in df.columns:
        mapping = {'Jedi': 1.0, 'Sith': -1.0}
        df['knight'] = df['knight'].map(mapping)
        if df['knight'].isnull().any():
            sys.exit("Error: Se encontraron valores en 'knight' que no son 'Jedi' o 'Sith'.")

    # Filtrar columnas numéricas
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        sys.exit("Error: dataset must contain al menos dos columnas numéricas.")

    # Calcular matriz de correlación
    corr = numeric_df.corr(method='pearson')

    # Crear heatmap con colormap 'Reds_r'
    plt.figure(figsize=(10, 7))
    sns.heatmap(corr, annot=False, cmap='Reds_r')
    plt.tight_layout()

    # Guardar figura en PNG
    plt.savefig(args.pngpath, format='png', bbox_inches='tight', pad_inches=0, dpi=500)
    print(f"Heatmap saved to: {args.pngpath}")

        # Mostrar figura sin bloquear y cerrar automáticamente
    plt.show(block=False)
    plt.pause(1)  # mostrar brevemente la ventana
    plt.close()








