#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def find_csv_dir():
    """
    Busca Train_knight.csv y Test_knight.csv en:
      1) ex03/ex00
      2) ../ex00  (la carpeta ex00 al mismo nivel que ex03)
    """
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir / "ex00",
        script_dir.parent / "ex00"
    ]
    for d in candidates:
        if (d / "Train_knight.csv").exists() and (d / "Test_knight.csv").exists():
            return d
    raise FileNotFoundError(f"No encontré CSV en ninguno de: {candidates!r}")


def load_datasets():
    """
    Carga y normaliza nombres de columnas para test y train.
    Train recibe además la columna 'knight'.
    Convierte todas las columnas numéricas a tipo float.
    """
    csv_dir   = find_csv_dir()
    test_csv  = csv_dir / "Test_knight.csv"
    train_csv = csv_dir / "Train_knight.csv"

    # Leer cabecera de test
    header = test_csv.open('r', encoding='utf-8').readline().strip().split(',')

    # Cargar DataFrames
    df_test  = pd.read_csv(test_csv, header=0)
    df_train = pd.read_csv(train_csv, header=None, names=header + ['knight'])

    # Normalizar nombres: quitar espacios, minúsculas y reemplazar caracteres
    def normalize_columns(df):
        df = df.copy()
        df.columns = (
            df.columns
              .str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('-', '_')
        )
        return df

    df_test = normalize_columns(df_test)
    df_train = normalize_columns(df_train)

    # Convertir columnas numéricas a float
    numeric_cols = [c for c in df_train.columns if c != 'knight']
    df_test[numeric_cols] = df_test[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df_train[numeric_cols] = df_train[numeric_cols].apply(pd.to_numeric, errors='coerce')

    return df_train, df_test


def standardize(train_df, test_df):
    """
    Standardiza (mean=0, std=1) usando estadísticas de train.
    Devuelve dos DataFrames estandarizados (train mantiene la columna 'knight').
    """
    numeric_cols = [c for c in train_df.columns if c != 'knight']
    means = train_df[numeric_cols].mean()
    stds  = train_df[numeric_cols].std(ddof=0)

    train_std = (train_df[numeric_cols] - means) / stds
    test_std  = (test_df[numeric_cols]  - means) / stds

    # Añadir columna 'knight' al train estandarizado
    train_std = train_std.copy()
    train_std['knight'] = train_df['knight'].astype(str).str.lower().str.strip()
    return train_std, test_std


def print_dataset(df):
    """Imprime datos con header y filas formateadas a 2 decimales, manejando la columna 'knight'."""
    cols = list(df.columns)
    # Imprime header
    print(" ".join(cols))
    for _, row in df.iterrows():
        vals = []
        for c in cols:
            v = row[c]
            if pd.isna(v):
                vals.append("nan")
            elif c == 'knight':
                vals.append(str(v))
            else:
                # Asegurar que v es numérico
                try:
                    vals.append(f"{float(v):.2f}")
                except (ValueError, TypeError):
                    vals.append(str(v))
        print(" ".join(vals))


def plot_stims_empowered(train_std):
    """Grafica Stims vs Empowered estándar (Train), diferenciando Jedi y Sith."""
    jedi = train_std[train_std['knight']=='jedi']
    sith = train_std[train_std['knight']=='sith']

    plt.figure()
    plt.scatter(jedi['empowered'], jedi['stims'], alpha=0.4, label='Jedi')
    plt.scatter(sith['empowered'], sith['stims'], alpha=0.4, label='Sith')
    plt.xlabel('Std Empowered')
    plt.ylabel('Std Stims')
    plt.legend()
    plt.title('Standardized: Stims vs Empowered (Train)')
    plt.savefig('ex03_stims_empowered_std.jpg', bbox_inches='tight', dpi=300)
    plt.close()


def main():
    df_train, df_test = load_datasets()
    train_std, test_std = standardize(df_train, df_test)

    # Imprime train estandarizado
    print_dataset(train_std)
    print()  # separación entre train y test
    # Imprime test estandarizado
    print_dataset(test_std)

    # Dibuja gráfico de ejemplo
    plot_stims_empowered(train_std)

if __name__ == '__main__':
    main()


