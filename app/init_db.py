from sqlalchemy import create_engine, text
from app.config import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import urllib.parse

def ensure_database_exists():
    db_url = settings.DATABASE_URL
    parsed = urllib.parse.urlparse(db_url)

    dbname = parsed.path.lstrip("/")
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port or 5432

    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {dbname}")
    cur.close()
    conn.close()