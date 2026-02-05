-- Data_Warehouse/ex03/fusion.sql

-- 1) Eliminar la tabla anterior si existe
DROP TABLE IF EXISTS customers_full;

-- 2) Crear customers_full fusionando customers con una versión única de items
CREATE TABLE customers_full AS
WITH uniq_items AS (
  SELECT DISTINCT ON (product_id)
    product_id,
    category_id,
    category_code,
    brand,
    price
  FROM items
  ORDER BY product_id
)
SELECT
  c.event_time,
  c.event_type,
  c.product_id,
  c.price        AS purchase_price,
  c.user_id,
  c.user_session,
  ui.category_id,
  ui.category_code,
  ui.brand        AS item_brand,
  ui.price        AS item_price
FROM customers c
LEFT JOIN uniq_items ui
  ON c.product_id = CAST(ui.product_id AS INTEGER);

-- 3) Índice opcional para acelerar consultas por product_id
CREATE INDEX IF NOT EXISTS idx_customers_full_product_id
  ON customers_full(product_id);


