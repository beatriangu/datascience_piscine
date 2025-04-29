#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Viz - Exercise 02: My Beautiful Mustache

Genera tres boxplots de precios de compra:
1. Distribución total (con outliers).
2. Distribución rango común (sin outliers).
3. Gasto promedio por usuario (con outliers).
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# --- Configuración de la conexión via env vars ---
DB_PARAMS = {
    "dbname":    os.getenv("POSTGRES_DB", "piscineds"),
    "user":      os.getenv("POSTGRES_USER", "bea"),
    "password":  os.getenv("POSTGRES_PASSWORD", "mysecretpassword"),
    "host":      os.getenv("DB_HOST", "localhost"),
    "port":      os.getenv("DB_PORT", "5432"),
}


def fetch_data(start, end):
    query = f"""
        SELECT
            purchase_price AS price,
            user_id,
            event_time
        FROM customers_full
        WHERE event_type = 'purchase'
          AND event_time >= '{start}'
          AND event_time <= '{end}'
          AND purchase_price IS NOT NULL
          AND user_id IS NOT NULL;
    """
    # Crear engine SQLAlchemy para pd.read_sql_query
    engine = create_engine(
        f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}"
        f"@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
    )
    df = pd.read_sql_query(query, engine, parse_dates=['event_time'])
    return df


def compute_stats(df: pd.DataFrame):
    """
    Devuelve un dict con estadísticas generales y arrays:
      - all_prices: todos los precios individuales
      - avg_prices: gasto promedio por usuario
    """
    prices = df['price']
    stats = prices.describe(percentiles=[.25, .5, .75]).to_dict()
    avg_per_user = df.groupby('user_id')['price'].mean()
    return stats, prices.values, avg_per_user.values


def plot_box(data, title, xlabel, facecolor, edgecolor,
             showfliers, xlim, output_path):
    """Genera y guarda un boxplot horizontal con estilo."""
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.boxplot(
        data,
        vert=False,
        patch_artist=True,
        showfliers=showfliers,
        boxprops=dict(facecolor=facecolor, edgecolor=edgecolor),
        whiskerprops=dict(color=edgecolor),
        capprops=dict(color=edgecolor),
        medianprops=dict(color=edgecolor, linewidth=2),
        flierprops=dict(marker='o', markersize=4,
                        markerfacecolor=edgecolor, markeredgecolor=edgecolor)
    )
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_yticks([])
    if xlim:
        ax.set_xlim(xlim)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(
        description="Exercise 02: My Beautiful Mustache (boxplots)")
    parser.add_argument('--start', default='2022-10-01',
                        help='Fecha inicio (YYYY-MM-DD)')
    parser.add_argument('--end',   default='2023-02-28',
                        help='Fecha fin (YYYY-MM-DD)')
    parser.add_argument('--outdir', default='.',
                        help='Directorio de salida para los PNG')
    args = parser.parse_args()

    # Crear carpeta de salida si no existe
    os.makedirs(args.outdir, exist_ok=True)

    # 1. Cargar datos
    df = fetch_data(args.start, args.end)
    if df.empty:
        print("No hay datos de compra en el rango especificado.")
        return

    # 2. Calcular estadísticas y series
    stats, all_prices, avg_prices = compute_stats(df)
    print("\n--- Estadísticas de precios de compra ---")
    for k, v in stats.items():
        print(f"{k.capitalize():>6}: {v:.6f}")

    # 3. Boxplots
    plot_box(
        all_prices,
        title="Overall Purchase Price Distribution",
        xlabel="Price (A$)",
        facecolor='lightgray',
        edgecolor='black',
        showfliers=True,
        xlim=(-70, 310),
        output_path=os.path.join(args.outdir, 'mustache_overall.png')
    )
    plot_box(
        all_prices,
        title="Purchase Price Distribution (Common Range)",
        xlabel="Price (A$)",
        facecolor='lightgreen',
        edgecolor='darkgreen',
        showfliers=False,
        xlim=(-1, 13),
        output_path=os.path.join(args.outdir, 'mustache_common.png')
    )
# 3) Gasto total por usuario (basket) 0–43, con outliers
plot_box(
    basket_prices,
    title="Average Basket Price per User",
    xlabel="Basket Price (A$)",
    facecolor='lightblue',
    edgecolor='darkblue',
    showfliers=True,
    xlim=(0, 43),
    output_path=os.path.join(args.outdir, 'mustache_avg_user.png')
)

print("\nBoxplots generados en:", args.outdir)


if __name__ == '__main__':
    main()




