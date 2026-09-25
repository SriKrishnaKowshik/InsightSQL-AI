import re


class SQLValidator:
    """
    Cleans and validates LLM-generated SQL.
    """

    @staticmethod
    def clean(sql: str) -> str:
        """
        Remove markdown code fences.
        """

        sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
        sql = re.sub(r"```", "", sql)
        return sql.strip()

    @staticmethod
    def validate(sql: str) -> bool:
        """
        Allow only SELECT statements.
        """

        sql = sql.strip().lower()

        forbidden = [
            "insert",
            "update",
            "delete",
            "drop",
            "truncate",
            "alter",
            "create"
        ]

        if not sql.startswith("select"):
            return False

        return not any(word in sql for word in forbidden)