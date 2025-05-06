#!/usr/bin/env python3

import os
import sys
import csv
import pandas as pd

# ─── Definición de Features ────────────────────────────────────────────────────
FEATURES = [
    "Sensitivity", "Hability", "Strength", "Power", "Agility", "Dexterity",
    "Awareness", "Prescience", "Reactivity", "Midi-chlorien", "Slash", "Push",
    "Pull", "Lightsaber", "Survival", "Repulse", "Friendship", "Blocking",
    "Deflection", "Mass", "Recovery", "Evade", "Stims", "Sprint", "Combo",
    "Delay", "Attunement", "Empowered", "Burst", "Grasping"
]

# ─── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))            # …/ex01
CSV_PATH   = os.path.normpath(os.path.join(BASE_DIR, '..', 'ex00', 'Train_knight.csv'))
OUT_PATH   = os.path.join(BASE_DIR, 'Correlation.txt')

# ─── Helpers ───────────────────────────────────────────────────────────────────
def detect_delimiter(path):
    """Detecta ',' vs ';' con csv.Sniffer."""
    with open(path, 'r', newline='') as f:
        sample = f.read(2048)
    try:
        return csv.Sniffer().sniff(sample, delimiters=[',',';']).delimiter
    except csv.Error:
        return ','

# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    if not os.path.isfile(CSV_PATH):
        sys.exit(f"ERROR: No existe el fichero {CSV_PATH}")

    sep = detect_delimiter(CSV_PATH)
    cols = FEATURES + ['knight']

    # Leer SIN cabecera, asignar nombres
    df = pd.read_csv(CSV_PATH, sep=sep, header=None, names=cols)

    print(f"DEBUG: Cargado {os.path.basename(CSV_PATH)} con sep='{sep}'")
    print("DEBUG: Primeras filas:\n", df.head(3), "\n")

    # Mapear target Jedi->1, Sith->0
    df['knight'] = (
        df['knight']
          .astype(str)
          .str.strip()
          .map({'Jedi': 1, 'Sith': 0})
    )

    # Eliminar filas con NaN en cualquier columna
    before = len(df)
    df.dropna(subset=cols, inplace=True)
    after = len(df)
    if after < before:
        print(f"WARNING: Eliminadas {before-after} filas con NaN")

    # Cálculo de correlaciones (Pearson por defecto)
    corr = df.corr(numeric_only=True)['knight']
    corr = corr.abs().sort_values(ascending=False)

    # Determinar ancho de la columna de nombres
    max_feat_len = max(len(feat) for feat in corr.index)

    # Escribir en Correlation.txt con alineación de columnas
    with open(OUT_PATH, 'w') as f:
        for feat, val in corr.items():
            # feat alineado a la izquierda, val a la derecha con 6 decimales
            f.write(f"{feat:<{max_feat_len}}  {val:>8.6f}\n")

    print(f"Guardado coeficientes en {OUT_PATH}")

if __name__ == '__main__':
    main()
