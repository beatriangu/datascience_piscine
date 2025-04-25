import os
import psycopg2

def get_connection(dbname=None):
    user = os.getenv('POSTGRES_USER') or os.getenv('USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('DB_HOST', 'db')
    port = int(os.getenv('DB_PORT', 5432))
    database = dbname or os.getenv('POSTGRES_DB', 'piscineds')
    return psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
