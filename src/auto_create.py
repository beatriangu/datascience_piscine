import glob
import os
from db_utils import get_connection
from create_table import create_table_from_csv

def main():
    conn = get_connection(dbname='piscineds')
    for csv_file in glob.glob(os.path.join('customer','*.csv')):
        tbl = os.path.splitext(os.path.basename(csv_file))[0]
        create_table_from_csv(conn, csv_file, tbl)
    conn.close()

if __name__ == '__main__':
    main()
