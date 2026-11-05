#importsqlite3
import sqlite3
from pathlip import Path
import Pandas as pd

DB_PATH = Path("data/inventory_forecasting.dp")

#creating the database connection
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def save_sales(df: pd.DataFrame):
    with _connect() as conn:
        df.to_sql("sales_history", conn, if_exists="replace", index=False)

def save_forecasts(df: pd.DataFrame):
    with _connect() as conn:
        df.to_sql("demand_forecasts", conn, if_exists="replace", index=False)

def load_table(table: str) -> pd.DataFrame:
    allowed = {"sales_history", "demand_forecasts"}
    if table not in allowed:
        raise ValueError("Unsupported table")
    with _connect() as conn:
        try:
            return pd.read_sql_query(f"SELECT * FROM {table}", conn)
        except Exception:
            return pd.DataFrame()