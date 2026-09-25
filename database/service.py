import pandas as pd
from sqlalchemy import text
from database.db import engine


class DatabaseService:
    """Handles all PostgreSQL operations."""

    def __init__(self):
        self.engine = engine

    def execute_query(self, sql: str) -> pd.DataFrame:
        """
        Execute a SELECT query and return a DataFrame.
        """

        sql = sql.strip()

        if not sql.lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed.")

        with self.engine.connect() as connection:
            result = pd.read_sql(text(sql), connection)

        return result

    def list_tables(self):
        sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        ORDER BY table_name;
        """

        return self.execute_query(sql)

    def get_schema(self):
        sql = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema='public'
        ORDER BY table_name, ordinal_position;
        """

        return self.execute_query(sql)