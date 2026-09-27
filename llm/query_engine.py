from llm.text_to_sql import TextToSQL
from llm.insight_generator import InsightGenerator
from llm.sql_validator import SQLValidator
from llm.followup_generator import FollowUpGenerator
from database.service import DatabaseService


class QueryEngine:
    """
    InsightSQL AI Pipeline

    User Question
        ↓
    Text-to-SQL
        ↓
    SQL Validation
        ↓
    PostgreSQL Execution
        ↓
    AI Business Insight
        ↓
    Follow-up Questions
    """

    def __init__(self):
        self.generator = TextToSQL()
        self.database = DatabaseService()
        self.insights = InsightGenerator()
        self.followups = FollowUpGenerator()

    def ask(self, question: str):

        # ----------------------------------------
        # Step 1: Generate SQL
        # ----------------------------------------
        sql = self.generator.generate_sql(question)

        # ----------------------------------------
        # Step 2: Validate SQL
        # ----------------------------------------
        valid, message = SQLValidator.validate(sql)

        if not valid:

            retry_prompt = f"""
The previous SQL is invalid.

Validation Error:
{message}

Original User Question:
{question}

Generate a corrected PostgreSQL SELECT query.

Rules:
- Use ONLY existing tables and columns.
- Return ONLY SQL.
"""

            sql = self.generator.generate_sql(retry_prompt)

        # ----------------------------------------
        # Step 3: Execute SQL
        # ----------------------------------------
        try:
            dataframe = self.database.execute_query(sql)

        except Exception as e:

            retry_prompt = f"""
The previous SQL produced a PostgreSQL error.

ERROR:
{str(e)}

ORIGINAL QUESTION:
{question}

PREVIOUS SQL:
{sql}

DATABASE SCHEMA:
{self.generator.schema}

Correct the SQL.

Requirements:
- Use ONLY existing tables and columns.
- If filtering by city, use customers.city.
- Never use orders.city.
- Return ONLY executable PostgreSQL SQL.
- Do not explain anything.
"""

            sql = self.generator.generate_sql(retry_prompt)
            dataframe = self.database.execute_query(sql)

        # ----------------------------------------
        # Step 4: AI Insight
        # ----------------------------------------
        insight = self.insights.generate(question, dataframe)

        # ----------------------------------------
        # Step 5: Follow-up Questions
        # ----------------------------------------
        followups = self.followups.generate(question, sql)

        # Debug (remove later if you want)
        print("FOLLOWUPS:", followups)

        # ----------------------------------------
        # Step 6: Return everything
        # ----------------------------------------
        return {
            "question": question,
            "sql": sql,
            "data": dataframe,
            "insight": insight,
            "followups": followups,
        }