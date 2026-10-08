# Mamaearth Growth Analytics

## 1. Project Overview

The Mamaearth Growth Analytics project analyzes e-commerce order data to identify revenue patterns, return-risk segments, data-quality issues, and business opportunities.

Workflow:
Raw CSV Data -> SQL Analysis -> Python Cleaning & EDA -> Visualizations -> GenAI Business Narrative

## 2. Dataset

| Dataset | Records |
|---|---:|
| Customers | 45 |
| Products | 16 |
| Orders | 180 |

## 3. Data-Quality Issues

- 5 duplicate orders
- 12 missing discount values
- 15 missing rating values
- Inconsistent payment-method capitalization
- 2 unusually large quantity values

Raw CSV files were not manually modified. Cleaning was performed using Python/Pandas.

## 4. SQL Analysis

MySQL was used for the database layer.

SQL reports included:
- Total orders, revenue and AOV
- Missing rating analysis
- Zero-order customer identification
- City-level return-rate analysis
- Top customer analysis
- Category-level revenue analysis
- Customer-name filtering using LIKE
- Distinct acquisition sources
- Loyalty-tier classification

Raw SQL results:
- Orders: 180
- Revenue: Rs 99,860.20
- AOV: Rs 554.78
- Missing ratings: 15
- Zero-order customer: C045 / Vihaan
- Jaipur return rate: 42.11%

## 5. Python Data Cleaning

Cleaning steps:
- Removed duplicate orders using a natural-key approach
- Standardized payment methods to COD, Card and UPI
- Filled missing discounts with 0%
- Filled missing ratings using median rating of 3.0
- Joined customer and product information
- Calculated order value
- Detected quantity outliers using the IQR method

Cleaning results:
- Raw orders: 180
- Clean orders: 175
- Duplicates removed: 5
- Missing discounts filled: 12
- Missing ratings filled: 15
- Median rating used: 3.0

## 6. Revenue Reconciliation

Raw SQL revenue: Rs 99,860.20

Cleaned Python revenue: Rs 97,358.30

Difference: -Rs 2,501.90

The main difference comes from removing duplicate orders from the raw dataset.

## 7. Return-Risk Analysis

COD had the highest return rate at 44.44%.

The highest-risk combination identified was COD + City Tier 2, with a 54.55% return rate.

This segment should be investigated further before making policy changes.

## 8. Outlier Analysis

2 quantity outliers were identified using the IQR method.

The upper IQR threshold was 3.5 units.

The outliers were retained as flagged observations rather than automatically deleted.

## 9. Monthly Revenue Analysis

With outliers included, January 2026 appears to be the peak revenue month.

After excluding quantity outliers from the trend analysis, March 2026 becomes the corrected peak revenue month.

## 10. Correlation Analysis

Correlation was analyzed between quantity, discount, rating, returned status and order value.

The strongest relationship was between quantity and order value, which is expected because quantity directly contributes to order value.

Relationships between return status and the other variables were weak or negligible.

Important: Correlation does not imply causation.

## 11. Visualizations

The project contains two primary visualizations:

1. Return Rate by Payment Method
2. Monthly Revenue After Outlier Adjustment

## 12. GenAI Narrative

Google Gemini was used to convert validated analytical findings into a management-level business narrative.

The narrative contains:
- Executive Summary
- Key Findings
- Business Recommendations
- Caveats

Numeric accuracy validation:
- 180 raw orders: PASS
- 175 clean orders: PASS
- 5 duplicates removed: PASS
- 44.44% COD return rate: PASS
- 54.55% COD + Tier 2 return rate: PASS

Validation score: 5/5

## 13. Business Recommendations

### 1. Investigate Tier 2 COD Returns

The 54.55% return rate for COD orders in Tier 2 cities indicates a high-risk segment.

Potential interventions include pre-shipment confirmation, delivery verification, address validation and incentives for prepaid orders.

### 2. Improve Data Quality Controls

Automated duplicate detection and standardized payment-method values should be included in future reporting pipelines.

### 3. Use Clean Data for Forecasting

Operational planning should rely on cleaned revenue trends rather than raw figures affected by duplicates and extreme quantity values.

### 4. Investigate Return Drivers

Further analysis should examine product category, customer location, delivery performance, product ratings, acquisition source and payment method.

## 14. Project Structure

Mamaearth-Growth-Analytics/
  README.md
  requirements.txt
  data/
  sql/
  analysis/
  visualizations/
  narrator/

## 15. How to Run

Install dependencies:

pip install -r requirements.txt

Run Python analysis:

python analysis/clean_and_eda.py

Generate visualizations:

python analysis/visualize.py

Set Gemini API key:

export GEMINI_API_KEY='YOUR_API_KEY'

Generate narrative:

python narrator/generate_narrative.py

## 16. Key Business Takeaways

- Data cleaning reduced the dataset from 180 to 175 orders.
- Rs 2,501.90 difference exists between raw SQL revenue and cleaned Python revenue.
- COD has the highest return rate at 44.44%.
- COD + City Tier 2 is the highest-risk segment at 54.55%.
- Two quantity outliers affect revenue interpretation.
- January 2026 is the apparent peak with outliers.
- March 2026 is the corrected peak after outlier adjustment.
- Correlation does not imply causation.

## 17. Conclusion

The analysis demonstrates how SQL, Python/Pandas, visualization and GenAI can transform raw e-commerce data into actionable business insights.

The key lesson is that data quality directly affects reported business performance. Cleaning duplicates, handling missing values, standardizing fields and investigating outliers creates a more reliable foundation for revenue and return-risk decisions.