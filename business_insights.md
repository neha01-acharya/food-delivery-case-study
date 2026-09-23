# Business Insights — Food Delivery Restaurant Order Intelligence

## 1. Executive Summary

The analysis of the food delivery dataset shows clear differences in customer spending, restaurant performance, food-item demand, and customer behavior.

The dataset contains 102 customer records, 31 restaurant records, 503 orders, and 1,172 order-item records. The generated dataset also contains intentional data-quality issues that were identified during validation.

Among the successful orders, the overall success rate is 82.70%.

---

## 2. Highest-Value Customers

The top customers by successful spending are:

| Customer | Successful Spending |
|---|---:|
| Priya Patel | 15,992 |
| Aarav Kumar | 13,360 |
| Anika Gupta | 12,319 |
| Aarav Patel | 10,297 |
| Anika Das | 9,961 |

These customers contribute relatively high order value and can be considered important customers based on their successful spending.

The customer classification logic also identified 4 customers as High Value Customers using the defined threshold of successful spending above 10,000.

### Business Interpretation

High-value customers can be monitored separately because changes in their ordering behavior may have a larger impact on revenue than changes among lower-spending customers.

---

## 3. Restaurant Performance

The top restaurants by successful-order revenue are:

| Restaurant | Revenue |
|---|---:|
| Urban Fusion | 28,877 |
| Royal Diner | 24,779 |
| Royal Bowl | 24,752 |
| Tandoori Treats | 23,430 |
| The Grand Palace | 19,857 |

Urban Fusion also recorded the highest number of successful orders with 24 successful orders.

### Restaurant Cancellation Rate

Restaurants with the highest observed cancellation rates included:

| Restaurant | Cancellation Rate |
|---|---:|
| Royal Fusion | 27.78% |
| The Grand Diner | 26.09% |
| Sizzle Fusion | 25.00% |
| Spice Route | 20.00% |
| Urban Express | 18.75% |

These restaurants can be investigated further to understand whether cancellations are related to preparation time, delivery operations, order availability, or other operational factors.

---

## 4. Food Item and Category Revenue

The highest-revenue food items were:

| Food Item | Revenue |
|---|---:|
| Mojito | 196,592 |
| Chilli Paneer | 35,446 |
| Coke | 32,712 |
| Masala Chai | 32,171 |
| Cheesecake | 31,889 |

Category-level revenue was:

| Category | Revenue |
|---|---:|
| Beverage | 320,908 |
| Starter | 144,582 |
| Main Course | 141,877 |
| Dessert | 140,170 |

Beverages generated the highest category revenue in the generated dataset.

Mojito was the highest-revenue individual item and also had the highest total quantity at 617 units.

---

## 5. Customer Preference vs Exploration

The preference analysis identified:

### Preference-Aligned Customers

- Customers: 50
- Successful orders: 236
- Total spending: 276,310
- Average order value: 1,170.81

### Explorer Customers

- Customers: 98
- Successful orders: 413
- Total spending: 470,152
- Average order value: 1,138.38

A customer is considered preference-aligned when they successfully order from at least one cuisine listed in their preference profile.

An explorer is a customer who successfully orders from at least one cuisine outside their stated preferences.

The two groups can overlap because a customer can both order preferred cuisines and explore other cuisines.

---

## 6. At-Risk Customers

The classification identified 3 customers as At-Risk based on the implemented rule:

- The customer has ordered previously.
- The customer has no successful order in the latest period.

These customers can be monitored for declining engagement and potentially targeted with retention initiatives.

---

## 7. Sequence Analysis

The sequence analysis identified:

- Customer with consecutive successful orders: Vivaan Das
- Longest gap between successful orders: 442 days, for Anika Rao
- Longest successful-order streak: Vivaan Das with 2 consecutive days
- Day with highest successful orders: 2025-10-06 with 5 successful orders
- Day with highest cancellation rate: 2026-02-06 with 100%

The date-based analysis was performed dynamically from the dataset rather than hard-coding a date range.

---

## 8. Data Quality Findings

The validation phase identified several intentionally introduced data-quality issues:

- Duplicate customer records
- Duplicate restaurant records
- Duplicate order records
- Duplicate order-item records
- Missing customer segment values
- Missing restaurant rating
- Invalid customer references
- Invalid restaurant references
- Invalid order references
- Invalid restaurant rating
- Invalid item quantity
- Invalid customer preference cuisine
- Duplicate customer preferences
- Unusual discount values

The raw data was not manually modified. Instead, reusable validation functions were used to identify the problems.

---

## 9. Recommendations

### 1. Monitor high-value customers

Track successful spending and ordering frequency of high-value customers to identify changes in their engagement.

### 2. Investigate restaurant cancellation patterns

Restaurants with higher cancellation rates should be investigated for operational causes such as order availability, preparation delays, or delivery-related issues.

### 3. Use food-item demand for menu planning

High-revenue and high-quantity items can be monitored when planning inventory and menu promotions.

### 4. Encourage exploration

Because many customers successfully order outside their stated preferences, recommendation systems can expose customers to related cuisines and new food categories.

### 5. Monitor at-risk customers

Customers with previous activity but no successful order in the latest period can be included in retention monitoring.

---

## 10. Important Data Limitation

The dataset is generated for the case study and intentionally contains duplicate and invalid records.

Therefore, the results should be interpreted as analysis of this generated dataset rather than as production business performance.

The analysis also preserves the generated anomalies rather than silently correcting them.