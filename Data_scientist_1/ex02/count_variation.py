#!/usr/bin/env python3

import os
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt

# ─── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))                  # ex02/
DATA_DIR   = os.path.normpath(os.path.join(BASE_DIR, '..', 'ex00'))      # ex00/
TRAIN_CSV  = os.path.join(DATA_DIR, 'Train_knight.csv')
TEST_CSV   = os.path.join(DATA_DIR, 'Test_knight.csv')

# ─── Columnas y Features ──────────────────────────────────────────────────────
FEATURES = [
    "Sensitivity", "Hability", "Strength", "Power", "Agility", "Dexterity",
    "Awareness", "Prescience", "Reactivity", "Midi-chlorien", "Slash", "Push",
    "Pull", "Lightsaber", "Survival", "Repulse", "Friendship", "Blocking",
    "Deflection", "Mass", "Recovery", "Evade", "Stims", "Sprint", "Combo",
    "Delay", "Attunement", "Empowered", "Burst", "Grasping"
]
COLUMNS = FEATURES + ["knight"]

# Escogemos las dos variables top a graficar
FEATURE_X = "Empowered"
FEATURE_Y = "Stims"

# ─── Utilidades ────────────────────────────────────────────────────────────────
def detect_delimiter(path):
    """Detecta ',' o ';' mediante csv.Sniffer."""
    with open(path, 'r', newline='') as f:
        sample = f.read(2048)
    try:
        return csv.Sniffer().sniff(sample, delimiters=[',',';']).delimiter
    except csv.Error:
        return ','

def load_data(path):
    """
    Carga el CSV SIN CABECERA con nombres fijos COLUMNS,
    mapea 'Jedi'→1 / 'Sith'→0, y devuelve sólo X, Y y knight sin NaNs.
    """
    if not os.path.isfile(path):
        sys.exit(f"ERROR: File not found: {path}")
    sep = detect_delimiter(path)
    df = pd.read_csv(path, sep=sep, header=None, names=COLUMNS)
    # Mapear knight
    df["knight"] = df["knight"].astype(str).str.strip().map({"Jedi":1, "Sith":0})
    # Seleccionar y limpiar
    df = df[[FEATURE_X, FEATURE_Y, "knight"]].dropna()
    return df

# ─── Graficado ─────────────────────────────────────────────────────────────────
def plot_scatter(df, prefix, xlim, ylim):
    """
    Genera dos archivos:
    - {prefix}_separated.png  (coloreado por clase)
    - {prefix}_mixed.png      (todos en gris)
    """
    x = df[FEATURE_X].values
    y = df[FEATURE_Y].values
    labels = df["knight"].astype(int).values

    # Separado
    plt.figure(figsize=(6,4))
    for cls, color, label in [(1,'tab:blue','Jedi'), (0,'tab:red','Sith')]:
        mask = (labels == cls)
        plt.scatter(x[mask], y[mask], c=color, s=10, label=label)
    plt.xlabel(FEATURE_X)
    plt.ylabel(FEATURE_Y)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{prefix}_separated.png")
    plt.close()

    # Mezclado
    plt.figure(figsize=(6,4))
    plt.scatter(x, y, c='gray', s=10)
    plt.xlabel(FEATURE_X)
    plt.ylabel(FEATURE_Y)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.tight_layout()
    plt.savefig(f"{prefix}_mixed.png")
    plt.close()

# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    # Carga datos
    df_train = load_data(TRAIN_CSV)
    df_test  = load_data(TEST_CSV)

    # Calcular límites comunes para ambos plots
    xmin = min(df_train[FEATURE_X].min(), df_test[FEATURE_X].min())
    xmax = max(df_train[FEATURE_X].max(), df_test[FEATURE_X].max())
    ymin = min(df_train[FEATURE_Y].min(), df_test[FEATURE_Y].min())
    ymax = max(df_train[FEATURE_Y].max(), df_test[FEATURE_Y].max())
    xgap = (xmax - xmin) * 0.05
    ygap = (ymax - ymin) * 0.05
    xlim = (xmin - xgap, xmax + xgap)
    ylim = (ymin - ygap, ymax + ygap)

    # Generar y guardar gráficos
    plot_scatter(df_train, 'train', xlim, ylim)
    plot_scatter(df_test,  'test',  xlim, ylim)

    print("Generated:", 
          ["train_separated.png","train_mixed.png","test_separated.png","test_mixed.png"])

if __name__ == '__main__':
    main()

