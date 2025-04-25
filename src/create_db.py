from db_utils import get_connection

def create_database():
    """
    Conecta a la BD 'postgres' y crea 'piscineds' si no existe.
    """
    conn = get_connection(dbname='postgres')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'piscineds';")
    if not cur.fetchone():
        cur.execute("CREATE DATABASE piscineds;")
        print("Database 'piscineds' created.")
    else:
        print("Database 'piscineds' already exists.")
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_database()
