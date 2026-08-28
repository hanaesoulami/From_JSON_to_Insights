# create_tables.py
import os
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

def create_database():
    """
    Connect to a default DB (DB_DEFAULT_DB) to create the target DB (DB_NAME).
    Returns a connection to the target DB.
    """
    default_db = os.getenv("DB_DEFAULT_DB", "studentdb")
    db_name = os.getenv("DB_NAME", "sparkifydb")
    host = os.getenv("DB_HOST", "127.0.0.1")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "admin")
    port = int(os.getenv("DB_PORT", 5432))

    # connect to default DB to create target DB
    conn = psycopg2.connect(host=host, dbname=default_db, user=user, password=password, port=port)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name} WITH ENCODING 'utf8' TEMPLATE template0")

    cur.close()
    conn.close()

    # connect to the newly created database
    conn = psycopg2.connect(host=host, dbname=db_name, user=user, password=password, port=port)
    return conn

def drop_tables(conn):
    with conn.cursor() as cur:
        for query in drop_table_queries:
            cur.execute(query)
    conn.commit()

def create_tables(conn):
    with conn.cursor() as cur:
        for query in create_table_queries:
            cur.execute(query)
    conn.commit()

def main():
    conn = create_database()
    try:
        drop_tables(conn)
        print("Tables dropped successfully!!")
        create_tables(conn)
        print("Tables created successfully!!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
