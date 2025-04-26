# Module: Data Warehouse

This module covers exercises **00–03** from the **"Data Warehouse"** subject of the Piscine Data Science program.

## Exercises Overview

- **Ex00 – Database Visualization**\
  Verify and explore the existing `piscineds` database in pgAdmin. (See `ex00/README.md` for details.)

- **Ex01 – Create Customers Table**\
  Combine all monthly data tables into a single `customers` table using:

  ```bash
  docker-compose exec db psql -U bea -d piscineds -f Data_Warehouse/ex01/create_customers.sql
  ```

- **Ex02 – Remove Duplicates**\
  Generate `customers_distinct` and `customers_dedup` tables to eliminate exact and near-duplicate records:

  ```bash
  docker-compose exec db psql -U bea -d piscineds -f Data_Warehouse/ex02/remove_duplicates.sql
  ```

- **Ex03 – Merge Customers with Items**\
  Create `customers_full` by LEFT JOIN-ing `customers` with `items`:

  ```bash
  docker-compose exec db psql -U bea -d piscineds -f Data_Warehouse/ex03/fusion.sql
  ```

> **Tip:** Always start with Ex00 to ensure your database and pgAdmin are correctly configured before running the SQL scripts.

## Setup & Commands

1. **Start all services**
   ```bash
   make up
   ```
2. **Run each exercise**
   - Ex01:
     ```bash
     docker-compose exec db psql -U bea -d piscineds -f Data_Warehouse/ex01/create_customers.sql
     ```
   - Ex02:
     ```bash
     docker-compose exec db psql -U bea -d piscineds -f Data_Warehouse/ex02/remove_duplicates.sql
     ```
   - Ex03:
     ```bash
     docker-compose exec db psql -U bea -d piscineds -f Data_Warehouse/ex03/fusion.sql
     ```
3. **Verify results**
   - In **pgAdmin**: open [http://localhost:8080](http://localhost:8080) → connect to `piscineds` → expand **Schemas → public → Tables**. You should see:
     ```
     data_2022_oct, data_2022_nov, data_2022_dec, data_2023_jan, data_2023_feb,
     customers, customers_distinct, customers_dedup, customers_full, items
     ```
   - Or via **psql**:
     ```bash
     docker-compose exec db psql -U bea -d piscineds -c "\dt"
     ```
4. **Cleanup**
   ```bash
   make clean
   ```



