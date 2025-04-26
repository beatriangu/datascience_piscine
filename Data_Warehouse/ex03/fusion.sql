-- ex03/fusion.sql
-- Exercise 03: Inspect table structures and create 'customers_full' by merging 'customers' with 'items'

-- 1) Inspect 'customers' table structure
SELECT column_name, data_type, ordinal_position
  FROM information_schema.columns
 WHERE table_schema = 'public'
   AND table_name   = 'customers'
 ORDER BY ordinal_position;

-- 2) Inspect 'items' table structure
SELECT column_name, data_type, ordinal_position
  FROM information_schema.columns
 WHERE table_schema = 'public'
   AND table_name   = 'items'
 ORDER BY ordinal_position;

-- 3) Create the merged table 'customers_full'
-- Explanation of LEFT JOIN:
-- A LEFT JOIN returns all rows from the "left" table (customers),
-- and the matched rows from the "right" table (items).
-- If there is no match, the result is NULL on the right side.
-- We use LEFT JOIN to ensure that every customer event remains,
-- even when the corresponding product_id is not present in the items table.

-- Drop existing fused table if it exists
DROP TABLE IF EXISTS customers_full;

-- Create the fused table
CREATE TABLE customers_full AS
SELECT
    c.*,
    i.item_name,
    i.price,
    i.category
FROM customers c
LEFT JOIN items i
  ON c.product_id = i.product_id;

-- Optional: Add index on product_id for faster joins
-- CREATE INDEX idx_customers_full_product_id ON customers_full(product_id);
