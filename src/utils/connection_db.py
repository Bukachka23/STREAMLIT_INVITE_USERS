import logging.config
import psycopg2

from src.config.log_config import LOGGING
from src.config.settings import ConfigDatabase

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        database_url = ConfigDatabase.DATABASE_URL
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set")
        conn = psycopg2.connect(database_url)
        logger.info(f"Successfully connected to database")
        return conn
    except (psycopg2.Error, ValueError) as e:
        logger.error(f"Unable to connect to the database. Error: {e}")
        raise


def get_top_inviters(limit=10):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT discord_id, invite_count
        FROM discord_users
        ORDER BY invite_count DESC
        LIMIT %s
    """, (limit,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
