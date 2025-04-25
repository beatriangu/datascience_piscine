import os
import argparse
import pandas as pd
from io import StringIO
from db_utils import get_connection

def infer_sql_dtype(dtype, series):
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return 'TIMESTAMP'
    elif pd.api.types.is_integer_dtype(dtype):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'REAL'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    else:
        max_len = series.astype(str).map(len).max()
        if max_len and max_len < 256:
            return f'VARCHAR({max_len})'
        return 'TEXT'

def create_table_from_csv(conn, csv_path, table_name):
    df = pd.read_csv(csv_path, parse_dates=[0], infer_datetime_format=True)
    columns = df.columns.tolist()
    dtypes = df.dtypes
    sql_types = [infer_sql_dtype(dtypes[col], df[col]) for col in columns]

    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS "{table_name}";')
    col_defs = [f'"{col}" {sql_type}' for col, sql_type in zip(columns, sql_types)]
    create_stmt = f'CREATE TABLE "{table_name}" (\n  ' + ',\n  '.join(col_defs) + '\n);'
    cur.execute(create_stmt)

    buf = StringIO()
    df.to_csv(buf, index=False, header=False)
    buf.seek(0)
    cols_list = ', '.join([f'"{c}"' for c in columns])
    copy_stmt = f'COPY "{table_name}" ({cols_list}) FROM STDIN WITH CSV'
    cur.copy_expert(copy_stmt, buf)
    conn.commit()
    cur.close()
    print(f"Table '{table_name}' created and data loaded.")

def main():
    parser = argparse.ArgumentParser(description='Create PostgreSQL tables from CSV.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--folder', help='Carpeta con CSVs')
    group.add_argument('--file', help='Un único CSV')
    parser.add_argument('--table', help='Nombre de tabla si usas --file')
    args = parser.parse_args()

    conn = get_connection(dbname='piscineds')
    if args.folder:
        for fname in os.listdir(args.folder):
            if fname.lower().endswith('.csv'):
                path = os.path.join(args.folder, fname)
                tbl = os.path.splitext(fname)[0]
                create_table_from_csv(conn, path, tbl)
    else:
        if not args.table:
            parser.error('--table es obligatorio con --file')
        create_table_from_csv(conn, args.file, args.table)
    conn.close()

if __name__ == '__main__':
    main()
