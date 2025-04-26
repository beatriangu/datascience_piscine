-- ex02/remove_duplicates.sql
-- Exercise 02: Remove duplicate rows from 'customers' table
-- 1) Exact duplicates
-- 2) Duplicates within 1-second intervals for same event_type and product_id

BEGIN;

-- Drop intermediate tables if they exist
DROP TABLE IF EXISTS customers_distinct;
DROP TABLE IF EXISTS customers_dedup;

-- 1) Remove exact duplicates
CREATE TABLE customers_distinct AS
SELECT DISTINCT *
FROM customers;

-- 2) Remove near-duplicate events (within 1 second)
CREATE TABLE customers_dedup AS
SELECT *
FROM (
    SELECT
        cd.*,
        lag(event_time) OVER (
            PARTITION BY event_type, product_id
            ORDER BY event_time
        ) AS prev_time
    FROM customers_distinct cd
) sub
WHERE prev_time IS NULL
   OR extract(epoch FROM (event_time - prev_time)) > 1;

COMMIT;
