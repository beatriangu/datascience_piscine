#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys


def find_csv_dir():
    """
    Busca Train_knight.csv y Test_knight.csv en:
      1) ex02/ex00
      2) ../ex00  (la carpeta ex00 al mismo nivel que ex02)
    """
    script_dir = Path(__file__).resolve().parent  # .../Data_scientist_1/ex02
    candidates = [
        script_dir / "ex00",
        script_dir.parent / "ex00"  # .../Data_scientist_1/ex00
    ]
    for d in candidates:
        if (d / "Train_knight.csv").exists() and (d / "Test_knight.csv").exists():
            return d
    raise FileNotFoundError(f"No encontré CSV en ninguno de: {candidates!r}")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas: quita espacios, pasa a minúsculas y reemplaza '-' por '_'.
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
    - Encuentra la carpeta ex00
    - Lee Test_knight.csv con su cabecera
    - Construye los nombres para Train_knight.csv (header=None + names)
    - Normaliza columnas y devuelve df_train, df_test
    """
    csv_dir = find_csv_dir()
    test_csv = csv_dir / "Test_knight.csv"
    train_csv = csv_dir / "Train_knight.csv"

    # 1) Leer cabecera de test y crear lista de nombres
    header = test_csv.open("r", encoding="utf-8").readline().strip().split(",")

    # 2) Cargar DataFrame de test con header por defecto
    df_test = pd.read_csv(test_csv)

    # 3) Cargar DataFrame de train sin header, añadiendo columna 'knight'
    df_train = pd.read_csv(train_csv, header=None, names=header + ['knight'])

    # 4) Normalizar nombres en ambos DataFrames
    df_test = normalize_columns(df_test)
    df_train = normalize_columns(df_train)

    return df_train, df_test


def plot_jedi_info(df_test: pd.DataFrame):
    """Grafica Stims vs Empowered y Deflection vs Push para el conjunto Test (todos Knight)."""
    # Stims vs Empowered
    plt.figure()
    plt.scatter(df_test['empowered'], df_test['stims'],
                alpha=0.4, color='green', label='Knight')
    plt.xlabel('Empowered')
    plt.ylabel('Stims')
    plt.legend()
    plt.savefig('jedi_stims_empowered.jpg', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close()

    # Deflection vs Push
    plt.figure()
    plt.scatter(df_test['push'], df_test['deflection'],
                alpha=0.4, color='green', label='Knight')
    plt.xlabel('Push')
    plt.ylabel('Deflection')
    plt.xlim(0.3, 3.9)
    plt.ylim(0.007, 0.082)
    plt.legend()
    plt.savefig('jedi_deflection_push.jpg', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close()


def plot_knight_info(df_train: pd.DataFrame):
    """Grafica Stims vs Empowered y Deflection vs Push diferenciando Jedi y Sith."""
    if 'knight' not in df_train.columns:
        print("ERROR: no existe la columna 'knight'. Columnas disponibles:", df_train.columns.tolist(), file=sys.stderr)
        return

    # Filtrado y limpieza de valores
    df_train['knight'] = df_train['knight'].astype(str).str.strip().str.lower()
    jedi = df_train[df_train['knight'] == 'jedi']
    sith = df_train[df_train['knight'] == 'sith']

    if jedi.empty or sith.empty:
        print(f"¡Atención! Datos vacíos: Jedi({len(jedi)}), Sith({len(sith)})", file=sys.stderr)

    # Stims vs Empowered
    plt.figure()
    plt.scatter(jedi['empowered'], jedi['stims'], alpha=0.4, color='blue', label='Jedi')
    plt.scatter(sith['empowered'], sith['stims'], alpha=0.4, color='red', label='Sith')
    plt.xlabel('Empowered')
    plt.ylabel('Stims')
    plt.legend()
    plt.savefig('knight_stims_empowered.jpg', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close()

    # Deflection vs Push
    plt.figure()
    plt.scatter(jedi['push'], jedi['deflection'], alpha=0.4, color='blue', label='Jedi')
    plt.scatter(sith['push'], sith['deflection'], alpha=0.4, color='red', label='Sith')
    plt.xlabel('Push')
    plt.ylabel('Deflection')
    plt.legend()
    plt.savefig('knight_deflection_push.jpg', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close()


def main():
    # Carga de datos
    df_train, df_test = load_datasets()

    # Impresión de verificación
    print("Train — primeros registros:")
    print(df_train.head(), "\nColumns:", df_train.columns.tolist(), "\n")
    print("Test  — primeros registros:")
    print(df_test.head(),  "\nColumns:", df_test.columns.tolist(), "\n")

    # Generación de gráficos
    plot_jedi_info(df_test)
    plot_knight_info(df_train)

if __name__ == '__main__':
    main()









