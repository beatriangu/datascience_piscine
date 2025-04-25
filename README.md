
📌 Piscine DS: Database Creation

This repository contains my complete solution for the "Creation of a DB" module from the Piscine Data Science program.

##Day 0 Data Engineer

ex 00 and 01 was just about to create the docker-compose file which runs 2 service, postgres for database and pgadmin to handle and see the db easier

ex 02 we created our first data table where I quickly realized doing things NOT ON the database make it significantly slower so first I connect to the postgres database and run my sql code directly on the database which made a table creation 7 second instead of 1,5-2 minute

ex 03 is the same as 02 but we need to create all the tables from the provided csv files

ex 04 we create the items table from the corresponding csv file, technically same as 02


This repository contains my complete solution for the "Creation of a DB" module from the Piscine Data Science program.

🚀 Project Objectives

The goal of this project is to develop key skills in:

Using Docker for isolated environments.

Creating and managing databases with PostgreSQL.

Automating CSV data import using Python.

Graphical database visualization using pgAdmin.

🗂️ Project Structure

Piscine_DS_Project
├── customer/            # Monthly data CSV files
│   ├── data_2022_dec.csv
│   ├── data_2022_nov.csv
│   ├── data_2022_oct.csv
│   ├── data_2023_feb.csv
│   └── data_2023_jan.csv
├── items/
│   └── item.csv         # Items CSV file
├── src/                 # Python scripts
│   ├── auto_create.py
│   ├── create_db.py
│   ├── create_table.py
│   └── db_utils.py
├── docker-compose.yml   # Docker services (Postgres + pgAdmin)
├── Dockerfile           # Docker image for Python app
├── requirements.txt     # Python dependencies
└── README.md            # This file

⚙️ Technologies Used

Docker and Docker Compose

PostgreSQL

Python with the following libraries:

pandas

psycopg2-binary

pgAdmin for database visualization

🔧 Installation and Setup

Make sure you have Docker and Docker Compose installed before proceeding.

1. Launch Containers

docker-compose up --build -d

2. Create the Database

docker-compose exec app python src/create_db.py

3. Create Tables from CSV files

# Monthly sales tables
docker-compose exec app python src/create_table.py --folder customer

# Items table
docker-compose exec app python src/create_table.py --file items/item.csv --table items

🎯 View the Database with pgAdmin

Go to pgAdmin in your browser.

Use the following credentials to log in:

Username (Email)

Password

admin@admin.com

admin

Database Connection Setup

Right-click on Servers → Create → Server.

General: Enter a name, e.g., piscineds.

Connection:

Field

Value

Host name/address

db

Port

5432

Maintenance database

piscineds

Username

bea

Password

mysecretpassword

Now you can inspect all your tables and data.

📋 Terminal Verification

You can also verify your tables via the terminal:

docker-compose exec db psql -U bea -d piscineds -c "\dt"

🎓 Completed Exercises

Exercise

Task

Status

00

Create PostgreSQL database piscineds

✅

01

Visualize DB using pgAdmin

✅

02

Tables from CSV (customer)

✅

03

Automate CSV import (customer)

✅

04

Create items table

✅

✨ Project completed by Beatriz Lamiquiz ✨
> ⚠️ Note: Due to file size constraints, the original CSV data files are not included in this repository. Please request access separately or use your own test data.
