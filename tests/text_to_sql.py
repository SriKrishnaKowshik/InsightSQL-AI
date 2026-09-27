from langchain_ollama import ChatOllama

from llm.prompts import SYSTEM_PROMPT
from llm.schema_retriever import SchemaRetriever
from llm.sql_validator import SQLValidator


class TextToSQL:

    def __init__(self):

        self.llm = ChatOllama(
            model="gemma3:4b",
            temperature=0
        )

        self.schema = SchemaRetriever()

    def generate_sql(self, question: str):

        schema = self.schema.get_schema_text()

        prompt = SYSTEM_PROMPT.format(schema=schema)

        response = self.llm.invoke([
            ("system", prompt),
            ("human", question)
        ])

        sql = SQLValidator.clean(response.content)

        if not SQLValidator.validate(sql):
            raise ValueError("Unsafe SQL generated.")

        return sql