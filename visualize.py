
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
VIS_DIR = os.path.join(BASE_DIR, "visualizations")

os.makedirs(VIS_DIR, exist_ok=True)

customers = pd.read_csv(
    os.path.join(DATA_DIR, "customers.csv")
)

products = pd.read_csv(
    os.path.join(DATA_DIR, "products.csv")
)

orders = pd.read_csv(
    os.path.join(DATA_DIR, "orders.csv")
)

natural_key = [
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "discount_pct",
    "payment_method",
    "rating",
    "returned"
]

orders_clean = orders.drop_duplicates(
    subset=natural_key,
    keep="first"
).copy()

orders_clean["payment_method"] = (
    orders_clean["payment_method"]
    .str.lower()
    .map({
        "cod": "COD",
        "card": "Card",
        "upi": "UPI"
    })
)

orders_clean["discount_pct"] = (
    orders_clean["discount_pct"].fillna(0)
)

orders_clean["rating"] = (
    orders_clean["rating"]
    .fillna(orders_clean["rating"].median())
)

orders_merged = orders_clean.merge(
    customers,
    on="customer_id",
    how="left"
)

orders_merged = orders_merged.merge(
    products,
    on="product_id",
    how="left"
)

orders_merged["order_value"] = (
    orders_merged["price"]
    * orders_merged["quantity"]
    * (1 - orders_merged["discount_pct"] / 100)
)

Q1 = orders_merged["quantity"].quantile(0.25)
Q3 = orders_merged["quantity"].quantile(0.75)
IQR = Q3 - Q1

upper_bound = Q3 + 1.5 * IQR

orders_merged["quantity_outlier"] = (
    orders_merged["quantity"] > upper_bound
)

payment_returns = (
    orders_merged
    .groupby("payment_method")
    .agg(
        total_orders=("order_id", "count"),
        returned_orders=("returned", "sum")
    )
)

payment_returns["return_rate"] = (
    payment_returns["returned_orders"]
    / payment_returns["total_orders"]
    * 100
)

payment_returns = payment_returns.sort_values(
    "return_rate",
    ascending=False
)

plt.figure(figsize=(8, 5))

payment_returns["return_rate"].plot(
    kind="bar"
)

plt.title("Return Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Return Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    os.path.join(
        VIS_DIR,
        "return_rate.png"
    ),
    dpi=150,
    bbox_inches="tight"
)

plt.close()

orders_merged["order_month"] = pd.to_datetime(
    orders_merged["order_date"],
    format="%Y-%m-%d"
).dt.to_period("M")

monthly_revenue = (
    orders_merged[
        ~orders_merged["quantity_outlier"]
    ]
    .groupby("order_month")["order_value"]
    .sum()
)

plt.figure(figsize=(9, 5))

monthly_revenue.plot(
    kind="line",
    marker="o"
)

plt.title(
    "Monthly Revenue After Outlier Adjustment"
)

plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(
        VIS_DIR,
        "monthly_revenue.png"
    ),
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print("Visualizations created successfully!")
