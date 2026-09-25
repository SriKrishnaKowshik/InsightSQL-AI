import pandas as pd
from langchain_ollama import ChatOllama


class InsightGenerator:

    def __init__(self):

        self.llm = ChatOllama(
            model="gemma3:4b",
            temperature=0.2
        )

    def generate(self, question: str, dataframe: pd.DataFrame):

        table = dataframe.to_markdown(index=False)

        prompt = f"""
You are a senior Business Data Analyst.

Question:
{question}

Result:
{table}

Write plain text only.

Summary:
Two short sentences.

Key Finding:
One sentence.

Business Insight:
One practical recommendation.

Maximum 100 words.
"""

        response = self.llm.invoke(prompt)

        return response.content.strip()