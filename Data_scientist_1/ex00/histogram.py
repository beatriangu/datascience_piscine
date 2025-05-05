#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import math
import sys
import os

# Ejercicio 00: Histogramas de skills
FEATURES = [
    "Sensitivity", "Hability", "Strength", "Power", "Agility", "Dexterity",
    "Awareness", "Prescience", "Reactivity", "Midi-chlorien", "Slash", "Push",
    "Pull", "Lightsaber", "Survival", "Repulse", "Friendship", "Blocking",
    "Deflection", "Mass", "Recovery", "Evade", "Stims", "Sprint", "Combo",
    "Delay", "Attunement", "Empowered", "Burst", "Grasping"
]


def create_grid(plot_func, title, out_file, legend_needed=False):
    """
    Crea un grid de histogramas para cada feature usando plot_func(ax, feat).
    """
    n = len(FEATURES)
    cols = 6
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols,
                             figsize=(cols * 3, rows * 2.5),
                             constrained_layout=True)
    for ax, feat in zip(axes.flat, FEATURES):
        plot_func(ax, feat)
        ax.set_title(feat, fontsize='small')
        ax.set_xlabel('Valor del skill', fontsize='x-small')
        ax.set_ylabel('Frecuencia', fontsize='x-small')
        ax.set_yticks(range(0, 16, 5))
        ax.tick_params(axis='both', which='major', labelsize='x-small')
        if legend_needed:
            ax.legend(fontsize='x-small')
    for ax in axes.flat[n:]:
        ax.set_visible(False)
    fig.suptitle(title, y=1.02)
    fig.savefig(out_file, dpi=150)
    plt.close(fig)
    print(f"Generado: {out_file}")


def plot_test():
    path = 'Test_knight.csv'
    if not os.path.isfile(path):
        print(f"ERROR: no se encuentra {path}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(path)

    missing = [f for f in FEATURES if f not in df.columns]
    if missing:
        print(f"ERROR: faltan columnas en Test_knight.csv: {missing}", file=sys.stderr)
        sys.exit(1)

    def draw_global(ax, feat):
        data = pd.to_numeric(df[feat], errors='coerce').dropna()
        ax.hist(data, bins=30, alpha=0.6, label='Knight', edgecolor='black')

    create_grid(
        plot_func=draw_global,
        title='Distribución global de cada skill (Test_knight.csv)',
        out_file='test_knight.png',
        legend_needed=True
    )


def plot_train():
    path = 'Train_knight.csv'
    if not os.path.isfile(path):
        print(f"ERROR: no se encuentra {path}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(path)

    # Verificar presencia de knight
    if 'knight' not in df.columns:
        print("WARNING: la columna 'knight' no se encontró en Train_knight.csv; se generará histograma global en su lugar.")
        # Reusar plot_test pero con Train data
        def draw_global_train(ax, feat):
            if feat in df.columns:
                data = pd.to_numeric(df[feat], errors='coerce').dropna()
                ax.hist(data, bins=30, alpha=0.6, label='Knight', edgecolor='black')
        create_grid(
            plot_func=draw_global_train,
            title='Distribución global de cada skill (Train_knight.csv)',
            out_file='train_knight.png',
            legend_needed=True
        )
        return

    missing = [f for f in FEATURES if f not in df.columns]
    if missing:
        print(f"WARNING: faltan columnas en Train_knight.csv: {missing}; se omitirán.")

    def draw_by_class(ax, feat):
        if feat in df.columns:
            data_jedi = pd.to_numeric(df.loc[df['knight']=='Jedi', feat], errors='coerce').dropna()
            data_sith = pd.to_numeric(df.loc[df['knight']=='Sith', feat], errors='coerce').dropna()
        else:
            data_jedi = []
            data_sith = []
        ax.hist(data_jedi, bins=30, color='pink', alpha=0.6,
                label='Lado Claro / Jedi', edgecolor='black')
        ax.hist(data_sith, bins=30, color='purple', alpha=0.6,
                label='Lado Oscuro / Sith', edgecolor='black')

    create_grid(
        plot_func=draw_by_class,
        title='Distribución por clase de cada skill (Train_knight.csv)',
        out_file='train_knight.png',
        legend_needed=True
    )

if __name__ == '__main__':
    print('Generando histogramas...')
    plot_test()
    plot_train()
    print('Archivos en directorio:', os.listdir('.'))

