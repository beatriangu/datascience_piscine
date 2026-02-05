-- 01_data_warehouse/ex01/create_customers.sql
-- Build a consolidated customers table by stacking monthly partitions.

BEGIN;

DROP TABLE IF EXISTS customers;

-- Create an empty table with the same schema as the reference month.
CREATE TABLE customers (LIKE data_2022_oct INCLUDING ALL);

-- Append all monthly datasets.
INSERT INTO customers
SELECT * FROM data_2022_oct
UNION ALL
SELECT * FROM data_2022_nov
UNION ALL
SELECT * FROM data_2022_dec
UNION ALL
SELECT * FROM data_2023_jan
UNION ALL
SELECT * FROM data_2023_feb;

-- Optional, but helpful for query planning.
ANALYZE customers;

COMMIT;



