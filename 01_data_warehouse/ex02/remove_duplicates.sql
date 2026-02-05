-- Data_Warehouse/ex02/remove_duplicates.sql
-- Exercice 02 : remove duplicates
-- 1) elimina duplicados exactos → customers_distinct
-- 2) elimina registros casi idénticos en 1s → customers_dedup

DROP TABLE IF EXISTS customers_distinct;
CREATE TABLE customers_distinct AS
  SELECT DISTINCT * FROM customers;

DROP TABLE IF EXISTS customers_dedup;
CREATE TABLE customers_dedup AS
WITH numbered AS (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY event_type, product_id, price, user_id
           ORDER BY event_time
         ) AS rn
  FROM customers
)
SELECT event_time, event_type, product_id, price, user_id
FROM numbered
WHERE rn = 1;


