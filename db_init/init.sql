-- 1) Creamos la tabla
CREATE TABLE IF NOT EXISTS customers_full (
  event_time TIMESTAMP,
  event_type TEXT,
  product_id BIGINT,
  price NUMERIC,
  user_id TEXT
);

-- 2) Cargamos cada CSV con COPY (ruta dentro del contenedor)
COPY customers_full(event_time, event_type, product_id, price, user_id)
  FROM '/docker-entrypoint-initdb.d/data_2022_oct.csv'  CSV HEADER;
COPY customers_full(event_time, event_type, product_id, price, user_id)
  FROM '/docker-entrypoint-initdb.d/data_2022_nov.csv'  CSV HEADER;
COPY customers_full(event_time, event_type, product_id, price, user_id)
  FROM '/docker-entrypoint-initdb.d/data_2022_dec.csv'  CSV HEADER;
COPY customers_full(event_time, event_type, product_id, price, user_id)
  FROM '/docker-entrypoint-initdb.d/data_2023_jan.csv'  CSV HEADER;
COPY customers_full(event_time, event_type, product_id, price, user_id)
  FROM '/docker-entrypoint-initdb.d/data_2023_feb.csv'  CSV HEADER;


