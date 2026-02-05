-- 01_data_warehouse/ex02/remove_duplicates.sql
-- Exercise: Remove duplicates
--
-- This script builds two cleaned versions of the consolidated `customers` table:
--
-- 1) customers_distinct
--    Removes exact duplicate rows using DISTINCT.
--
-- 2) customers_dedup
--    Removes near-duplicates by keeping the earliest event_time per logical key
--    (event_type, product_id, price, user_id).

BEGIN;

-- 1) Exact duplicates removal
DROP TABLE IF EXISTS customers_distinct;

CREATE TABLE customers_distinct AS
SELECT DISTINCT
    event_time,
    event_type,
    product_id,
    price,
    user_id
FROM customers;

-- 2) Near-duplicates removal (keep earliest event per key)
DROP TABLE IF EXISTS customers_dedup;

CREATE TABLE customers_dedup AS
WITH ranked AS (
    SELECT
        event_time,
        event_type,
        product_id,
        price,
        user_id,
        ROW_NUMBER() OVER (
            PARTITION BY event_type, product_id, price, user_id
            ORDER BY event_time ASC
        ) AS rn
    FROM customers_distinct
)
SELECT
    event_time,
    event_type,
    product_id,
    price,
    user_id
FROM ranked
WHERE rn = 1;

-- Optional: improve query planner statistics for downstream steps.
ANALYZE customers_distinct;
ANALYZE customers_dedup;

COMMIT;



