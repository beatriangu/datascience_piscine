-- 01_data_warehouse/ex03/fusion.sql
-- Exercise: Fusion
--
-- Build an enriched customer events table by joining customer activity
-- with a de-duplicated view of the items reference table.

BEGIN;

DROP TABLE IF EXISTS customers_full;

-- Create a stable, unique items view:
-- - Keep a single row per product_id
-- - Ensure deterministic selection if duplicates exist
WITH uniq_items AS (
    SELECT DISTINCT ON (product_id)
        product_id,
        category_id,
        category_code,
        brand,
        price
    FROM items
    -- Prefer rows with more information; fall back deterministically.
    ORDER BY
        product_id,
        (category_id IS NULL) ASC,
        (category_code IS NULL) ASC,
        (brand IS NULL) ASC
),
-- Normalize product_id to integer when safe (prevents join errors)
items_int AS (
    SELECT
        CASE
            WHEN product_id ~ '^[0-9]+$' THEN product_id::INTEGER
            ELSE NULL
        END AS product_id_int,
        category_id,
        category_code,
        brand,
        price
    FROM uniq_items
)
SELECT
    c.event_time,
    c.event_type,
    c.product_id,
    c.price AS purchase_price,
    c.user_id,
    c.user_session,
    i.category_id,
    i.category_code,
    i.brand AS item_brand,
    i.price AS item_price
INTO customers_full
FROM customers AS c
LEFT JOIN items_int AS i
    ON c.product_id = i.product_id_int;

-- Index for common access patterns (product joins / filters)
CREATE INDEX IF NOT EXISTS idx_customers_full_product_id
    ON customers_full (product_id);

-- Optional: enable if you often filter by these columns
-- CREATE INDEX IF NOT EXISTS idx_customers_full_user_id ON customers_full (user_id);
-- CREATE INDEX IF NOT EXISTS idx_customers_full_event_time ON customers_full (event_time);

ANALYZE customers_full;

COMMIT;



