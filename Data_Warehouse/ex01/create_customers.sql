-- ex01/create_customers.sql
-- Exercise 01: Create 'customers' table by uniting all data_202*_*** tables

-- Remove existing table if any
DROP TABLE IF EXISTS customers;

-- Create the 'customers' table
CREATE TABLE customers AS
  SELECT * FROM data_2022_oct
  UNION ALL
  SELECT * FROM data_2022_nov
  UNION ALL
  SELECT * FROM data_2022_dec
  UNION ALL
  SELECT * FROM data_2023_jan
  UNION ALL
  SELECT * FROM data_2023_feb;

-- Optional: Add a primary key or index if needed
-- CREATE INDEX idx_customers_event_time ON customers(event_time);
