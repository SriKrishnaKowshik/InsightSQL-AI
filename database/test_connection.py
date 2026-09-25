from service import DatabaseService

db = DatabaseService()

print("=" * 40)
print("Tables")
print("=" * 40)

print(db.list_tables())

print("\n")

print("=" * 40)
print("Revenue by Category")
print("=" * 40)

query = """
SELECT
    c.category_name,
    ROUND(SUM(oi.quantity * oi.unit_price),2) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN categories c
    ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY revenue DESC;
"""

print(db.execute_query(query))