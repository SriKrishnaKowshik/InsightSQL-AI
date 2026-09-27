from llm.text_to_sql import TextToSQL

agent = TextToSQL()

question = "Show the top 5 products by revenue."

sql = agent.generate_sql(question)

print("\nGenerated SQL\n")
print(sql)