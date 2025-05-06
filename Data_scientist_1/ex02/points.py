#!/usr/bin/env python3

import os
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt

# ─── Rutas ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))             # ex02/
DATA_DIR   = os.path.normpath(os.path.join(BASE_DIR, '..', 'ex00')) # ex00/
TRAIN_CSV  = os.path.join(DATA_DIR, 'Train_knight.csv')
TEST_CSV   = os.path.join(DATA_DIR, 'Test_knight.csv')

# ─── Features & Columnas ───────────────────────────────────────────────────────
FEATURES = [
    "Sensitivity", "Hability", "Strength", "Power", "Agility", "Dexterity",
    "Awareness", "Prescience", "Reactivity", "Midi-chlorien", "Slash", "Push",
    "Pull", "Lightsaber", "Survival", "Repulse", "Friendship", "Blocking",
    "Deflection", "Mass", "Recovery", "Evade", "Stims", "Sprint", "Combo",
    "Delay", "Attunement", "Empowered", "Burst", "Grasping"
]
COLUMNS = FEATURES + ["knight"]

# Las dos que vamos a graficar
FEATURE_X = "Empowered"
FEATURE_Y = "Stims"

# ─── Utilidad: detectar separador ───────────────────────────────────────────────
def detect_delimiter(path):
    """Detecta ',' o ';' con csv.Sniffer."""
    with open(path, 'r', newline='') as f:
        sample = f.read(4096)
    try:
        return csv.Sniffer().sniff(sample, delimiters=[',',';']).delimiter
    except csv.Error:
        return ','

# ─── Carga los datos sin cabecera y limpia ─────────────────────────────────────
def load_data(path):
    """
    Lee el CSV sin esperar cabecera real:
      - sep: ',' o ';' automáticamente
      - header=None con names=COLUMNS
      - mapea Jedi→1 / Sith→0
      - devuelve df[[FEATURE_X,FEATURE_Y,'knight']].dropna()
    """
    if not os.path.isfile(path):
        sys.exit(f"ERROR: File not found: {path}")
    sep = detect_delimiter(path)
    df = pd.read_csv(path, sep=sep, header=None, names=COLUMNS)
    # Mapeo target
    df["knight"] = df["knight"].astype(str).str.strip().map({"Jedi":1, "Sith":0})
    # Selección y limpieza
    df = df[[FEATURE_X, FEATURE_Y, "knight"]].dropna()
    return df

# ─── Dibuja los dos scatter (separado y mezclado) ──────────────────────────────
def plot_scatter(df, prefix, xlim, ylim):
    x = df[FEATURE_X].values
    y = df[FEATURE_Y].values
    labels = df["knight"].astype(int).values

    # Separado
    plt.figure(figsize=(6,4))
    for cls, color, label in [(1,'tab:blue','Jedi'), (0,'tab:red','Sith')]:
        mask = labels == cls
        plt.scatter(x[mask], y[mask], c=color, s=10, label=label)
    plt.xlabel(FEATURE_X); plt.ylabel(FEATURE_Y)
    plt.xlim(xlim); plt.ylim(ylim)
    plt.legend(); plt.tight_layout()
    plt.savefig(f"{prefix}_separated.png"); plt.close()

    # Mezclado
    plt.figure(figsize=(6,4))
    plt.scatter(x, y, c='gray', s=10)
    plt.xlabel(FEATURE_X); plt.ylabel(FEATURE_Y)
    plt.xlim(xlim); plt.ylim(ylim)
    plt.tight_layout()
    plt.savefig(f"{prefix}_mixed.png"); plt.close()

# ─── Función principal ─────────────────────────────────────────────────────────
def main():
    # 1) Cargo train/test
    df_train = load_data(TRAIN_CSV)
    df_test  = load_data(TEST_CSV)

    # 2) Límites comunes (5% margen)
    xmin = min(df_train[FEATURE_X].min(), df_test[FEATURE_X].min())
    xmax = max(df_train[FEATURE_X].max(), df_test[FEATURE_X].max())
    ymin = min(df_train[FEATURE_Y].min(), df_test[FEATURE_Y].min())
    ymax = max(df_train[FEATURE_Y].max(), df_test[FEATURE_Y].max())
    xgap, ygap = (xmax - xmin)*0.05, (ymax - ymin)*0.05
    xlim, ylim = (xmin-xgap, xmax+xgap), (ymin-ygap, ymax+ygap)

    # 3) Genero y guardo
    plot_scatter(df_train, 'train', xlim, ylim)
    plot_scatter(df_test,  'test',  xlim, ylim)

    print("Generated files:", 
          ["train_separated.png","train_mixed.png","test_separated.png","test_mixed.png"])

if __name__ == "__main__":
    main()



