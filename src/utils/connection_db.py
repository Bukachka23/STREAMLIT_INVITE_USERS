import psycopg2

from src.config.settings import ConfigDatabase


def get_db_connection():
    conn = psycopg2.connect(
        host=ConfigDatabase.HOST,
        database=ConfigDatabase.DB,
        user=ConfigDatabase.USER,
        password=ConfigDatabase.PASSWORD
    )
    return conn


def get_top_inviters(limit=10):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT discord_id, invite_count
        FROM users
        ORDER BY invite_count DESC
        LIMIT %s
    """, (limit,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
