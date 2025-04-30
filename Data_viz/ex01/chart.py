#!/usr/bin/env python3
# chart.py

import os
import argparse
import psycopg2
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# Database connection parameters
DB_NAME = "piscineds"
DB_USER = "bea"
DB_PASS = "mysecretpassword"
DB_HOST = "localhost"
DB_PORT = "5432"


def fetch_purchases():
    """
    Fetch user_id, event_time, and price for all purchases
    between 2022-10-01 and 2023-02-28.
    """
    sql = """
        SELECT user_id, event_time, event_type, price
        FROM customers
        WHERE event_type = 'purchase'
          AND event_time >= '2022-10-01'
          AND event_time < '2023-03-01'
    """
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER,
        password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def plot_daily_customers(rows, outdir):
    """
    Plot daily unique customer counts and save to outdir.
    """
    daily_users = defaultdict(set)
    for user_id, event_time, _, _ in rows:
        date = event_time.strftime('%Y-%m-%d')
        daily_users[date].add(user_id)

    dates = sorted(daily_users.keys())
    counts = [len(daily_users[d]) for d in dates]

    plt.figure(figsize=(12, 5))
    plt.plot(dates, counts, linewidth=1)
    plt.ylabel("Number of Customers")

    # Show ticks at the start of each month
    xticks = [i for i, d in enumerate(dates) if d.endswith('-01')]
    xticklabels = [
        datetime.strptime(d, '%Y-%m-%d').strftime('%b') 
        for d in dates if d.endswith('-01')
    ]
    plt.xticks(xticks, xticklabels)
    plt.tight_layout()

    path = os.path.join(outdir, "daily_customers.png")
    plt.savefig(path)
    plt.clf()
    print(f"Saved: {path}")


def plot_monthly_sales(rows, outdir):
    """
    Plot total monthly sales and save to outdir.
    """
    monthly_sales = defaultdict(float)
    for _, event_time, _, price in rows:
        month = event_time.strftime('%Y-%m')
        monthly_sales[month] += price

    months = sorted(monthly_sales.keys())
    sales = [monthly_sales[m] for m in months]

    plt.figure(figsize=(10, 5))
    plt.bar(months, sales)
    plt.title("Total Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales (Altairian $)")
    plt.tight_layout()

    path = os.path.join(outdir, "monthly_sales.png")
    plt.savefig(path)
    plt.clf()
    print(f"Saved: {path}")


def plot_monthly_avg_spend(rows, outdir):
    """
    Plot average spend per customer per month and save to outdir.
    """
    monthly_sales = defaultdict(float)
    monthly_users = defaultdict(set)
    for user_id, event_time, _, price in rows:
        month = event_time.strftime('%Y-%m')
        monthly_sales[month] += price
        monthly_users[month].add(user_id)

    months = sorted(monthly_sales.keys())
    avg_spend = [
        monthly_sales[m] / len(monthly_users[m]) for m in months
    ]
    labels = [
        datetime.strptime(m, '%Y-%m').strftime('%b') for m in months
    ]

    plt.figure(figsize=(10, 5))
    plt.fill_between(labels, avg_spend, alpha=0.3)
    plt.plot(labels, avg_spend, linestyle='-', linewidth=2)
    plt.title("Average Spend per Customer/Month")
    plt.xlabel("Month")
    plt.ylabel("Average Spend (Altairian $)")
    plt.tight_layout()

    path = os.path.join(outdir, "avg_spend_per_customer.png")
    plt.savefig(path)
    plt.clf()
    print(f"Saved: {path}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate charts for purchases')
    parser.add_argument(
        '--outdir',
        default='.',
        help='Output directory for the charts (PNG)')
    args = parser.parse_args()

    # 1. Ensure output directory exists
    os.makedirs(args.outdir, exist_ok=True)

    # 2. Fetch data
    purchases = fetch_purchases()

    # 3. Generate and save charts
    plot_daily_customers(purchases, args.outdir)
    plot_monthly_sales(purchases, args.outdir)
    plot_monthly_avg_spend(purchases, args.outdir)

    print("\nAll charts generated successfully.")


if __name__ == '__main__':
    main()



