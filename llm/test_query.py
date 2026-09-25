from llm.query_engine import QueryEngine

engine = QueryEngine()

question = "Show the top 5 products by revenue."

response = engine.ask(question)

print("="*60)
print("QUESTION")
print("="*60)

print(response["question"])

print("\n")

print("="*60)
print("SQL")
print("="*60)

print(response["sql"])

print("\n")

print("="*60)
print("RESULT")
print("="*60)

print(response["data"])

print("\n")

print("="*60)
print("AI INSIGHT")
print("="*60)

print(response["insight"])