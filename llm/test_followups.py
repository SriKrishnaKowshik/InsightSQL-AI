from llm.followup_generator import FollowUpGenerator

gen = FollowUpGenerator()

sql = """
SELECT product_name, SUM(quantity * unit_price) AS revenue
FROM products
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 5;
"""

questions = gen.generate(
    "Show the top 5 products by revenue.",
    sql
)

print(questions)