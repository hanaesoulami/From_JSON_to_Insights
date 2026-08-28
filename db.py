# db.py
import os
import psycopg2

def get_connection():
    """
    Return a psycopg2 connection using DATABASE_URL if set, otherwise
    use DB_HOST/DB_NAME/DB_USER/DB_PASSWORD/DB_PORT env vars with defaults.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url)

    host = os.getenv("DB_HOST", "127.0.0.1")
    dbname = os.getenv("DB_NAME", "studentdb")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "admin")
    port = int(os.getenv("DB_PORT", 5432))
    
    return psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
