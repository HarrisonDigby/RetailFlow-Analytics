from pathlib import Path
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker


fake = Faker("en_GB")
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = Path("data/raw")


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def random_date(start_date: datetime, end_date: datetime) -> datetime:
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))


def generate_customers(n: int = 500) -> pd.DataFrame:
    customers = []

    for customer_id in range(1, n + 1):
        customers.append(
            {
                "customer_id": customer_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "country": random.choice(["UK", "UK", "UK", "Ireland", "France", "Germany"]),
                "signup_date": random_date(datetime(2024, 1, 1), datetime(2025, 12, 31)).date(),
            }
        )

    return pd.DataFrame(customers)


def generate_products() -> pd.DataFrame:
    categories = {
        "Clothing": ["T-Shirt", "Hoodie", "Jeans", "Jacket"],
        "Fitness": ["Resistance Bands", "Yoga Mat", "Protein Shaker", "Gym Gloves"],
        "Home": ["Desk Lamp", "Storage Box", "Mug", "Notebook"],
        "Electronics": ["Wireless Mouse", "Keyboard", "USB-C Cable", "Phone Stand"],
    }

    products = []
    product_id = 1

    for category, product_names in categories.items():
        for name in product_names:
            price = round(random.uniform(8, 120), 2)
            cost = round(price * random.uniform(0.35, 0.7), 2)

            products.append(
                {
                    "product_id": product_id,
                    "product_name": name,
                    "category": category,
                    "unit_price": price,
                    "unit_cost": cost,
                }
            )
            product_id += 1

    return pd.DataFrame(products)


def generate_orders(customers: pd.DataFrame, products: pd.DataFrame, n: int = 2000) -> pd.DataFrame:
    orders = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)

    channels = ["Website", "Amazon", "eBay", "Offline Trade"]
    statuses = ["completed", "completed", "completed", "refunded", "cancelled"]

    for order_id in range(1, n + 1):
        product = products.sample(1).iloc[0]
        quantity = random.randint(1, 5)
        order_date = random_date(start_date, end_date).date()

        orders.append(
            {
                "order_id": order_id,
                "customer_id": int(customers.sample(1).iloc[0]["customer_id"]),
                "product_id": int(product["product_id"]),
                "order_date": order_date,
                "channel": random.choice(channels),
                "quantity": quantity,
                "unit_price": product["unit_price"],
                "status": random.choice(statuses),
            }
        )

    return pd.DataFrame(orders)


def generate_ad_spend() -> pd.DataFrame:
    rows = []
    platforms = ["Google Ads", "Meta Ads", "TikTok Ads"]

    current_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)

    while current_date <= end_date:
        for platform in platforms:
            rows.append(
                {
                    "date": current_date.date(),
                    "platform": platform,
                    "campaign": random.choice(["Brand", "Prospecting", "Retargeting"]),
                    "spend": round(random.uniform(20, 500), 2),
                    "clicks": random.randint(20, 2000),
                    "impressions": random.randint(1000, 50000),
                }
            )
        current_date += timedelta(days=1)

    return pd.DataFrame(rows)


def generate_refunds(orders: pd.DataFrame) -> pd.DataFrame:
    refunded_orders = orders[orders["status"] == "refunded"].copy()
    refunds = []

    for _, order in refunded_orders.iterrows():
        refunds.append(
            {
                "refund_id": len(refunds) + 1,
                "order_id": order["order_id"],
                "refund_date": pd.to_datetime(order["order_date"]).date() + timedelta(days=random.randint(1, 30)),
                "refund_reason": random.choice(["Damaged", "Late Delivery", "Changed Mind", "Wrong Item"]),
            }
        )

    return pd.DataFrame(refunds)


def main() -> None:
    ensure_output_dir()

    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers, products)
    ad_spend = generate_ad_spend()
    refunds = generate_refunds(orders)

    customers.to_csv(OUTPUT_DIR / "customers.csv", index=False)
    products.to_csv(OUTPUT_DIR / "products.csv", index=False)
    orders.to_csv(OUTPUT_DIR / "orders.csv", index=False)
    ad_spend.to_csv(OUTPUT_DIR / "ad_spend.csv", index=False)
    refunds.to_csv(OUTPUT_DIR / "refunds.csv", index=False)

    print("Generated raw data files:")
    print("- customers.csv")
    print("- products.csv")
    print("- orders.csv")
    print("- ad_spend.csv")
    print("- refunds.csv")


if __name__ == "__main__":
    main()