import re


class SQLValidator:

    @staticmethod
    def clean(text: str) -> str:
        """
        Extract SQL from an LLM response.
        Removes markdown and extra text.
        """
        if "```sql" in text:
            text = text.split("```sql")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return text.strip()

    @staticmethod
    def validate(sql: str):
        sql = sql.strip().lower()

        if not sql.startswith("select"):
            return False, "Only SELECT statements are allowed."

        forbidden = [
            "drop", "delete", "update",
            "insert", "alter", "truncate", "create"
        ]

        for word in forbidden:
            if re.search(rf"\b{word}\b", sql):
                return False, f"Forbidden keyword: {word}"

        return True, "Valid SQL"