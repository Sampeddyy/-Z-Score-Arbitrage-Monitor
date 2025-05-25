# storage.py
# Optional: storing data in a database (e.g., PostgreSQL, InfluxDB, or TimescaleDB).

import psycopg2
from config import USE_DATABASE, DATABASE_URI

def init_db():
    if not USE_DATABASE:
        return None
    conn = psycopg2.connect(DATABASE_URI)
    # Optionally create tables for price history, signals, etc.
    return conn

def store_signal(conn, signal_data):
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO signals (timestamp, pair, exchange_a, price_a, exchange_b, price_b, spread, z_score, direction)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                signal_data["timestamp"],
                signal_data["pair"],
                signal_data["exchange_a"],
                signal_data["price_a"],
                signal_data["exchange_b"],
                signal_data["price_b"],
                signal_data["spread"],
                signal_data["z_score"],
                signal_data["direction"],
            ))
        conn.commit()
    except Exception as e:
        print(f"Error storing signal: {e}")
        conn.rollback()
