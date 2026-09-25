from faker import Faker
from random import choices, randint, uniform
from datetime import datetime, timedelta
import pandas as pd

from database.db import engine
from database.config import (
    CATEGORIES,
    PRICE_RANGES,
    CITY_WEIGHTS,
    PAYMENT_WEIGHTS,
    STATUS_WEIGHTS,
    PRODUCTS,
    POPULARITY
)

fake = Faker("de_DE")

# ==========================================================
# Reset Tables
# ==========================================================

with engine.begin() as conn:
    conn.exec_driver_sql("""
        TRUNCATE TABLE
        payments,
        order_items,
        orders,
        products,
        categories,
        customers
        RESTART IDENTITY CASCADE;
    """)

print("Old data removed.")

# ==========================================================
# Categories
# ==========================================================

category_df = pd.DataFrame({
    "category_name": CATEGORIES
})

category_df.to_sql(
    "categories",
    engine,
    if_exists="append",
    index=False
)

print("Categories inserted.")

# ==========================================================
# Products
# ==========================================================

products = []

product_lookup = {}

product_id = 1

for category_id, category in enumerate(CATEGORIES, start=1):

    low, high = PRICE_RANGES[category]

    for product in PRODUCTS[category]:

        price = round(uniform(low, high), 2)

        products.append({
            "product_name": product,
            "category_id": category_id,
            "price": price
        })

        product_lookup[product_id] = {
            "name": product,
            "price": price,
            "category": category
        }

        product_id += 1

product_df = pd.DataFrame(products)

product_df.to_sql(
    "products",
    engine,
    if_exists="append",
    index=False
)

print("Products inserted.")

# ==========================================================
# Customers
# ==========================================================

cities = list(CITY_WEIGHTS.keys())
city_weights = list(CITY_WEIGHTS.values())

customers = []

for _ in range(2000):

    city = choices(cities, weights=city_weights, k=1)[0]

    customers.append({
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "city": city,
        "country": "Germany",
        "signup_date": fake.date_between(
            start_date="-3y",
            end_date="today"
        )
    })

customer_df = pd.DataFrame(customers)

customer_df.to_sql(
    "customers",
    engine,
    if_exists="append",
    index=False
)

print("Customers inserted.")

# ==========================================================
# Loyal Customers (20%)
# ==========================================================

loyal_customers = list(range(1,401))
regular_customers = list(range(401,2001))

# ==========================================================
# Orders (Seasonal)
# ==========================================================

status_names = list(STATUS_WEIGHTS.keys())
status_weights = list(STATUS_WEIGHTS.values())

orders = []

order_dates = []

start = datetime(2024,1,1)

for _ in range(12000):

    month = choices(
        population=[1,2,3,4,5,6,7,8,9,10,11,12],
        weights=[6,6,7,7,8,8,8,8,9,10,14,19],
        k=1
    )[0]

    day = randint(1,28)

    year = choices([2024,2025,2026],[30,40,30],k=1)[0]

    date = datetime(year,month,day)

    if randint(1,100) <= 50:
        customer = choices(loyal_customers, k=1)[0]
    else:
        customer = choices(regular_customers, k=1)[0]

    status = choices(status_names, status_weights, k=1)[0]

    orders.append({
        "customer_id": customer,
        "order_date": date.date(),
        "status": status
    })

    order_dates.append(date.date())

order_df = pd.DataFrame(orders)

order_df.to_sql(
    "orders",
    engine,
    if_exists="append",
    index=False
)

print("Orders inserted.")

# ==========================================================
# Order Items
# ==========================================================

product_ids = list(product_lookup.keys())

weights = []

for pid in product_ids:

    name = product_lookup[pid]["name"]

    weights.append(
        POPULARITY.get(name,3)
    )

items = []

for order in range(1,12001):

    item_count = choices(
        [1,2,3,4],
        [20,40,30,10],
        k=1
    )[0]

    for _ in range(item_count):

        pid = choices(
            product_ids,
            weights=weights,
            k=1
        )[0]

        items.append({
            "order_id": order,
            "product_id": pid,
            "quantity": randint(1,3),
            "unit_price": product_lookup[pid]["price"]
        })

item_df = pd.DataFrame(items)

item_df.to_sql(
    "order_items",
    engine,
    if_exists="append",
    index=False
)

print("Order items inserted.")

# ==========================================================
# Payments
# ==========================================================

payment_names = list(PAYMENT_WEIGHTS.keys())
payment_weights = list(PAYMENT_WEIGHTS.values())

payments = []

grouped = item_df.groupby("order_id")

for order_id, group in grouped:

    total = (
        group["quantity"] *
        group["unit_price"]
    ).sum()

    payments.append({
        "order_id": order_id,
        "amount": round(total,2),
        "payment_method": choices(
            payment_names,
            payment_weights,
            k=1
        )[0],
        "payment_date": order_dates[order_id-1]
    })

payment_df = pd.DataFrame(payments)

payment_df.to_sql(
    "payments",
    engine,
    if_exists="append",
    index=False
)

# ==========================================================
# Summary
# ==========================================================

revenue = payment_df["amount"].sum()

print("\n"+"="*55)
print(" InsightSQL AI Business Dataset Generated ")
print("="*55)

print(f"Categories      : {len(category_df)}")
print(f"Products        : {len(product_df)}")
print(f"Customers       : {len(customer_df)}")
print(f"Orders          : {len(order_df)}")
print(f"Order Items     : {len(item_df)}")
print(f"Payments        : {len(payment_df)}")
print(f"Total Revenue   : €{revenue:,.2f}")

print("="*55)