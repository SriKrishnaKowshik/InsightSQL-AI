from llm.text_to_sql import TextToSQL
from llm.insight_generator import InsightGenerator
from database.service import DatabaseService


class QueryEngine:

    def __init__(self):
        self.generator = TextToSQL()
        self.db = DatabaseService()
        self.insights = InsightGenerator()

    def ask(self, question: str):

        sql = self.generator.generate_sql(question)

        try:
            data = self.db.execute_query(sql)

        except Exception as e:

            fixed_question = f"""
            Original question:
            {question}

            Previous SQL:
            {sql}

            Database error:
            {str(e)}

            Generate a corrected PostgreSQL SELECT query using only existing columns.
            """

            sql = self.generator.generate_sql(fixed_question)
            data = self.db.execute_query(sql)

        insight = self.insights.generate(question, data)

        return {
            "question": question,
            "sql": sql,
            "data": data,
            "insight": insight,
        }