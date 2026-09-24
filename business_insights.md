# Business Insights — Food Delivery Restaurant Order Intelligence

## 1. Key Findings

The analysis was performed on:

* **102 customer records**
* **31 restaurants**
* **503 orders**
* **1,172 order-item records**
* **100 customer preference records**

### Overall Order Performance

| Metric              |     Result |
| ------------------- | ---------: |
| Total Orders        |        503 |
| Delivered Orders    |        416 |
| Cancelled Orders    |         61 |
| Failed Orders       |         26 |
| Success Rate        |     82.70% |
| Total Order Value   | 565,060.00 |
| Average Order Value |   1,123.38 |
| Total Discount      |  30,100.00 |

The dataset shows an overall delivered-order success rate of **82.70%**.

A negative minimum calculated order value was also identified. This is associated with an intentional discount anomaly in the generated dataset and was treated as a data-quality issue rather than silently correcting the raw record.

---

# 2. Customer Insights

## Highest-Value Customers

The top customers by successful spending were:

| Customer    | Successful Spending |
| ----------- | ------------------: |
| Priya Patel |           15,992.00 |
| Aarav Kumar |           13,360.00 |
| Anika Gupta |           12,319.00 |
| Aarav Patel |           10,297.00 |
| Anika Das   |            9,961.00 |

Using the defined threshold of **10,000**, the analysis identified **4 High Value Customers**.

These customers represent a segment that can be monitored separately because their successful order spending is substantially higher than the defined high-value threshold.

## Customers With No Successful Orders

The analysis identified **3 customers with no successful orders**.

These customers may require further investigation to understand whether the issue is caused by:

* Failed orders
* Cancelled orders
* Restaurant availability
* Customer ordering behavior
* Data-quality issues

---

# 3. Restaurant Insights

## Highest-Revenue Restaurants

The top restaurants by successful-order revenue were:

| Restaurant       |   Revenue |
| ---------------- | --------: |
| Urban Fusion     | 28,877.00 |
| Royal Diner      | 24,779.00 |
| Royal Bowl       | 24,752.00 |
| Tandoori Treats  | 23,430.00 |
| The Grand Palace | 19,857.00 |

**Urban Fusion** generated the highest successful-order revenue in the analysis.

## Restaurants With Higher Cancellation Rates

The restaurants with the highest observed cancellation rates were:

| Restaurant      | Cancellation Rate |
| --------------- | ----------------: |
| Royal Fusion    |            27.78% |
| The Grand Diner |            26.09% |
| Sizzle Fusion   |            25.00% |
| Spice Route     |            20.00% |
| Urban Express   |            18.75% |

These restaurants should be investigated further to determine whether cancellation patterns are associated with operational factors such as preparation time, availability, delivery capacity, or order volume.

Cancellation rate alone does not establish the cause.

---

# 4. Product Insights

## Highest-Revenue Food Items

The highest-revenue food items were:

| Food Item     |    Revenue |
| ------------- | ---------: |
| Mojito        | 196,592.00 |
| Chilli Paneer |  35,446.00 |
| Coke          |  32,712.00 |
| Masala Chai   |  32,171.00 |
| Cheesecake    |  31,889.00 |

Mojito generated substantially higher item revenue than the other individual food items in the dataset.

## Category Revenue

| Category    |    Revenue |
| ----------- | ---------: |
| Beverage    | 320,908.00 |
| Starter     | 144,582.00 |
| Main Course | 141,877.00 |
| Dessert     | 140,170.00 |

The **Beverage** category generated the highest revenue among the analyzed categories.

This suggests that beverage demand should be considered when planning menu availability, inventory, and promotional strategies.

---

# 5. Customer Preference Insights

Customers were divided into two analytical groups:

### Preference-Aligned Customers

These are customers who successfully ordered from at least one cuisine present in their stated preferences.

```text
Customers:       50
Orders:         236
Total Spending: 276,310.00
Average Order Value: 1,170.81
```

### Explorers

These are customers who successfully ordered from at least one cuisine outside their stated preferences.

```text
Customers:       98
Orders:         413
Total Spending: 470,152.00
Average Order Value: 1,138.38
```

These groups are **not mutually exclusive**. A customer can order both preferred and non-preferred cuisines.

The results indicate that customers are not limited to their stated preferences and that exploration of other cuisines is common in the dataset.

---

# 6. At-Risk Customer Insights

The implemented classification defines an at-risk customer as someone who:

1. Has ordered previously, and
2. Has no successful order during the latest calendar month present in the dataset.

Using this definition, **3 customers** were identified as at risk.

These customers can be investigated further using:

* Previous order frequency
* Previous spending
* Last successful order date
* Preferred cuisines
* Restaurant choices
* Cancellation and failure history

The at-risk classification is based on the chosen latest-period assumption and should be adjusted if the business defines a different retention window.

---

# 7. Customer Behavior and Sequence Insights

The sequence analysis identified:

### Consecutive Successful Orders

**Vivaan Das** had consecutive successful orders.

### Longest Gap

**Anika Rao** had the longest observed gap between successful orders:

```text
442 days
```

### Longest Successful-Order Streak

**Vivaan Das** had the longest successful-order streak:

```text
2 consecutive days
```

### Highest Successful-Order Day

```text
2025-10-06
5 successful orders
```

### Highest Cancellation-Rate Day

```text
2026-02-06
100% cancellation rate
```

The cancellation-rate result should be interpreted alongside the number of orders on that day because a 100% rate can occur when the number of orders is very small.

---

# 8. Data Quality Observations

The validation stage identified several issues in the generated dataset.

### Duplicate Records

* Duplicate customer records: 2
* Duplicate restaurant records: 1
* Duplicate order records: 3
* Duplicate order-item records: 2

### Duplicate IDs

Duplicate IDs were identified for:

* Customers
* Restaurants
* Orders

### Missing Values

Missing values were identified in:

* Customer segment
* Restaurant rating

### Invalid References

The data contained invalid references involving:

* Customers
* Restaurants
* Orders

### Other Validation Issues

The analysis also identified:

* Invalid ratings
* Invalid quantities
* Invalid cuisines
* Duplicate customer preferences
* Invalid discount values

The raw data was not manually rewritten to remove these issues. They were reported and handled through validation and conditional logic.

---

# 9. Business Recommendations

## Recommendation 1 — Monitor and Retain High-Value Customers

Create a dedicated monitoring segment for customers whose successful spending exceeds the defined high-value threshold.

For these customers, track:

* Order frequency
* Recent order activity
* Spending changes
* Preferred cuisines
* Cancellation history

This can help identify changes in behavior before they become significant retention issues.

---

## Recommendation 2 — Investigate Restaurants With High Cancellation Rates

Restaurants such as Royal Fusion, The Grand Diner, and Sizzle Fusion show comparatively high cancellation rates in the dataset.

The business should investigate:

* Preparation time
* Item availability
* Restaurant acceptance behavior
* Delivery-partner availability
* Time-of-day patterns
* Cancellation reasons

The goal should be to identify the operational cause rather than treating cancellation rate as the cause itself.

---

## Recommendation 3 — Use Product Demand for Inventory and Menu Planning

Beverages represent the highest-revenue category, while Mojito is the highest-revenue individual food item in this dataset.

Restaurants and the platform can use this information to:

* Monitor inventory for high-demand products
* Reduce stock-out risk
* Plan promotional bundles
* Evaluate menu placement
* Identify complementary food and beverage combinations

---

## Recommendation 4 — Use Exploration Behavior for Personalized Recommendations

A large number of customers ordered cuisines outside their stated preferences.

The platform can use this behavior to identify potential interests beyond explicit preference data.

For example, recommendation systems can combine:

* Stated preferences
* Previous orders
* Cuisine exploration
* Restaurant history
* Order frequency

This can help personalize recommendations while still allowing customers to discover new cuisines.

---

## Recommendation 5 — Monitor At-Risk Customers Using Recent Activity

The identified at-risk customers should be monitored using their previous ordering behavior and latest successful order date.

Potential retention analysis can include:

* Days since last successful order
* Historical order frequency
* Historical spending
* Cancellation frequency
* Preferred cuisines
* Previously ordered restaurants

This provides a more complete picture than relying on a single inactivity metric.

---

# 10. Limitations

* The dataset is synthetically generated.
* The dataset intentionally contains anomalies for validation practice.
* High-value and frequent-customer thresholds are defined assumptions.
* At-risk classification depends on the selected latest-calendar-month interpretation.
* Preference-aligned and explorer groups can overlap.
* Cancellation rates should be interpreted together with order volume.
* The findings should be validated against production data before being used for operational decisions.

---

# 11. Conclusion

The analysis demonstrates how Core Python and DSA can be used to convert raw food-delivery transaction data into actionable business insights.

The main areas identified are:

* High-value customer behavior
* Restaurant revenue and cancellation patterns
* High-revenue food items and categories
* Customer preference alignment and exploration
* Potentially at-risk customer behavior
* Data-quality issues requiring attention

The resulting recommendations focus on customer retention, restaurant operations, product demand, personalization, and monitoring of recent customer activity.
