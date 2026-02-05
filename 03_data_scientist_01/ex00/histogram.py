#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import math
import sys
import os

# Ejercicio 00: Histogramas de skills
def detect_delimiter(path):
    """Detecta automáticamente ',' o ';' basándose en la primera línea útil."""
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                return ';' if line.count(';') > line.count(',') else ','
    return ','

FEATURES = [
    "Sensitivity","Hability","Strength","Power","Agility","Dexterity",
    "Awareness","Prescience","Reactivity","Midi-chlorien","Slash","Push",
    "Pull","Lightsaber","Survival","Repulse","Friendship","Blocking",
    "Deflection","Mass","Recovery","Evade","Stims","Sprint","Combo",
    "Delay","Attunement","Empowered","Burst","Grasping"
]

OUTPUT_TEST = 'Test_histograms.png'
OUTPUT_TRAIN = 'Train_histograms.png'


def plot_grid(df, plot_func, title, out_file, legend=False):
    """Crea un grid de histogramas para cada feature usando plot_func(ax, df, feat)."""
    n = len(FEATURES)
    cols = 6
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols*3, rows*2.5), constrained_layout=True)
    axes = axes.flatten()

    for ax, feat in zip(axes, FEATURES):
        plot_func(ax, df, feat)
        ax.set_title(feat, fontsize='small')
        ax.set_xlabel('Valor del skill', fontsize='x-small')
        ax.set_ylabel('Frecuencia', fontsize='x-small')
        ax.set_yticks(range(0, 16, 5))
        ax.tick_params(labelsize='x-small')
        if legend:
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                ax.legend(fontsize='x-small')

    for ax in axes[n:]:
        ax.set_visible(False)

    fig.suptitle(title, y=1.02)
    fig.savefig(out_file, dpi=150)
    plt.close(fig)
    print(f"Generado: {out_file}")


def plot_test():
    """Lee Test_knight.csv y genera Test_histograms.png con histogramas globales."""
    path = 'Test_knight.csv'
    if not os.path.isfile(path):
        sys.exit(f"ERROR: {path} no encontrado.")

    delim = detect_delimiter(path)
    df = pd.read_csv(path, sep=delim, usecols=FEATURES)
    df = df.apply(pd.to_numeric, errors='coerce')

    def draw_test(ax, df, feat):
        data = df[feat].dropna()
        if data.size:
            ax.hist(data, bins=30, color='C0', alpha=0.6)
        else:
            ax.text(0.5,0.5,'No data',ha='center',va='center',transform=ax.transAxes,fontsize='small',color='gray')

    plot_grid(df, draw_test,
              'Distribución global de cada skill (Test_knight.csv)',
              OUTPUT_TEST)


def plot_train():
    """Lee Train_knight.csv y genera Train_histograms.png comparando clases."""
    path = 'Train_knight.csv'
    if not os.path.isfile(path):
        sys.exit(f"ERROR: {path} no encontrado.")

    delim = detect_delimiter(path)
    # Primero intentar con header real
    df = pd.read_csv(path, sep=delim)
    if 'knight' not in df.columns:
        # Saltar fila corrupta y asignar nombres
        df = pd.read_csv(path, sep=delim, header=None, skiprows=1,
                         names=FEATURES + ['knight'])

    # Convertir features a numérico
    df[FEATURES] = df[FEATURES].apply(pd.to_numeric, errors='coerce')
    # Asegurar que 'knight' sea string y sin espacios
    df['knight'] = df['knight'].astype(str).str.strip()

    # Filtrar solo clases existentes en datos
    df = df[df['knight'].isin(['Jedi','Sith'])]

    def draw_train(ax, df, feat):
        d0 = df.loc[df['knight']=='Jedi', feat].dropna()
        d1 = df.loc[df['knight']=='Sith', feat].dropna()
        if d0.size:
            ax.hist(d0, bins=30, color='purple', alpha=0.6)
        if d1.size:
            ax.hist(d1, bins=30, color='pink', alpha=0.6)
        if not d0.size and not d1.size:
            ax.text(0.5,0.5,'No data',ha='center',va='center',transform=ax.transAxes,fontsize='small',color='gray')
        # Always add legend with fixed labels
        ax.legend(['Jedi','Sith'], fontsize='x-small')

    plot_grid(df, draw_train,
              'Distribución por clase de cada skill (Train_knight.csv)',
              OUTPUT_TRAIN,
              legend=True)


if __name__ == '__main__':
    print('Generando histogramas...')
    plot_test()
    plot_train()
    print('Generación completa.')
