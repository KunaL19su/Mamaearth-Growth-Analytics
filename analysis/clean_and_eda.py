
import pandas as pd
import numpy as np
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
NARRATOR_DIR = os.path.join(BASE_DIR, "narrator")

os.makedirs(NARRATOR_DIR, exist_ok=True)

customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
orders = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))

print("Data loaded successfully!")
print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)

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

duplicates_removed = len(orders) - len(orders_clean)

orders_clean["payment_method"] = (
    orders_clean["payment_method"]
    .str.lower()
    .map({
        "cod": "COD",
        "card": "Card",
        "upi": "UPI"
    })
)

missing_discounts = orders_clean["discount_pct"].isnull().sum()
missing_ratings = orders_clean["rating"].isnull().sum()

orders_clean["discount_pct"] = (
    orders_clean["discount_pct"].fillna(0)
)

rating_median = orders_clean["rating"].median()

orders_clean["rating"] = (
    orders_clean["rating"].fillna(rating_median)
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

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

orders_merged["quantity_outlier"] = (
    (orders_merged["quantity"] < lower_bound) |
    (orders_merged["quantity"] > upper_bound)
)

quantity_outliers = int(
    orders_merged["quantity_outlier"].sum()
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

highest_payment_method = payment_returns.index[0]

highest_payment_return_rate = float(
    payment_returns.iloc[0]["return_rate"]
)

risk_segment = (
    orders_merged
    .groupby(["payment_method", "city_tier"])
    .agg(
        total_orders=("order_id", "count"),
        returned_orders=("returned", "sum")
    )
)

risk_segment["return_rate"] = (
    risk_segment["returned_orders"]
    / risk_segment["total_orders"]
    * 100
)

risk_segment = risk_segment.sort_values(
    "return_rate",
    ascending=False
)

highest_risk_payment = risk_segment.index[0][0]
highest_risk_city_tier = int(risk_segment.index[0][1])

highest_risk_return_rate = float(
    risk_segment.iloc[0]["return_rate"]
)

correlation_columns = [
    "quantity",
    "discount_pct",
    "rating",
    "returned",
    "order_value"
]

correlation_matrix = (
    orders_merged[correlation_columns].corr()
)

orders_merged["order_month"] = pd.to_datetime(
    orders_merged["order_date"],
    format="%Y-%m-%d"
).dt.to_period("M")

monthly_with_outliers = (
    orders_merged
    .groupby("order_month")["order_value"]
    .sum()
)

monthly_without_outliers = (
    orders_merged[
        ~orders_merged["quantity_outlier"]
    ]
    .groupby("order_month")["order_value"]
    .sum()
)

peak_with_outliers = str(
    monthly_with_outliers.idxmax()
)

peak_without_outliers = str(
    monthly_without_outliers.idxmax()
)

raw_sql_revenue = 99860.20

cleaned_python_revenue = float(
    orders_merged["order_value"].sum()
)

revenue_difference = (
    cleaned_python_revenue - raw_sql_revenue
)

findings = {
    "data_quality": {
        "raw_orders": int(len(orders)),
        "clean_orders": int(len(orders_clean)),
        "duplicates_removed": int(duplicates_removed),
        "missing_discounts_filled": int(missing_discounts),
        "missing_ratings_filled": int(missing_ratings),
        "rating_median": float(rating_median)
    },
    "revenue": {
        "raw_sql_revenue": raw_sql_revenue,
        "cleaned_python_revenue": round(
            cleaned_python_revenue, 2
        ),
        "difference": round(
            revenue_difference, 2
        )
    },
    "returns": {
        "highest_payment_method": highest_payment_method,
        "highest_payment_return_rate": round(
            highest_payment_return_rate, 2
        )
    },
    "risk_segment": {
        "payment_method": highest_risk_payment,
        "city_tier": highest_risk_city_tier,
        "return_rate": round(
            highest_risk_return_rate, 2
        )
    },
    "outliers": {
        "quantity_outliers": quantity_outliers,
        "upper_bound": float(upper_bound)
    },
    "monthly_revenue": {
        "peak_with_outliers": peak_with_outliers,
        "peak_without_outliers": peak_without_outliers
    }
}

findings_path = os.path.join(
    NARRATOR_DIR,
    "findings.json"
)

with open(
    findings_path,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        findings,
        f,
        indent=4
    )

print("Analysis completed successfully!")
