# Food Delivery — Restaurant Order Intelligence

## 1. Project Overview

This project analyzes a food delivery dataset using **Core Python, Data Structures & Algorithms, and Object-Oriented Programming (OOP)**.

The objective is to understand:

* Customer purchasing behavior
* Restaurant performance
* Food item and category revenue
* Customer preferences and exploration behavior
* Customer retention and potential risk
* Data-quality issues
* Efficient approaches for searching, ranking, grouping, and sequence analysis

The project intentionally uses Core Python instead of Pandas, NumPy, SQL, or external analytics libraries.

---

## 2. Business Problem

The food delivery business wants to understand its customers, restaurants, and food-ordering patterns in order to identify:

* High-value customers
* Strong-performing restaurants
* Restaurants requiring attention
* High-revenue food items and categories
* Customers who explore outside their stated preferences
* Customers who may be at risk based on recent ordering behavior

The analysis converts raw transactional data into business-oriented insights and recommendations.

---

## 3. Dataset

The dataset is generated using `generate_dataset.py` and stored as Python data files.

### Dataset components

| Dataset              | Records |
| -------------------- | ------: |
| Customers            |     102 |
| Restaurants          |      31 |
| Orders               |     503 |
| Order Items          |    1172 |
| Customer Preferences |     100 |

### Data files

```text
data/
├── customers.py
├── restaurants.py
├── orders.py
├── order_items.py
└── customer_preferences.py
```

---

# 4. Approach Followed

## Day 1 — Data Validation and Business Analysis

The first stage focused on understanding and validating the raw data before performing business analysis.

### Validation

Reusable validation functions were implemented to identify:

* Duplicate records
* Duplicate IDs
* Missing values
* Invalid customer references
* Invalid restaurant references
* Invalid order references
* Invalid ratings
* Invalid quantities
* Invalid cuisines
* Duplicate customer preferences
* Invalid discount values

The raw data was **not manually modified to hide or remove anomalies**. Issues were identified and reported so that downstream analysis could account for data-quality limitations.

### Profiling

Basic profiling was performed using Core Python to understand:

* Customer cities
* Customer segments
* Restaurant cuisines
* Order status distribution

### Order Analysis

The following metrics were calculated:

* Total orders
* Successful/delivered orders
* Cancelled orders
* Failed orders
* Success rate
* Total order value
* Average Order Value
* Minimum and maximum order value
* Total discount

Order value was calculated as:

```text
Order Value = Subtotal + Delivery Fee - Discount
```

### Customer Analysis

The analysis identified:

* Top customers by successful spending
* Customers with no successful orders
* Customers who never ordered

### Restaurant Analysis

Restaurant performance was evaluated using:

* Revenue
* Successful order count
* Average Order Value
* Cancellation rate

### Food Item Analysis

The analysis examined:

* Most frequently ordered items
* Quantity sold
* Item revenue
* Category revenue

---

# Day 2 — DSA and Algorithmic Analysis

The second stage focused on solving analytical problems using Core Python data structures and algorithms.

### Ranking Engine

A reusable ranking function was created so that different entities can be ranked using different metrics without rewriting the complete ranking logic.

It was applied to:

* Customers
* Restaurants
* Food items
* Cuisines
* Cities

### Customer Preference Analysis

Customers were grouped into:

**Preference-Aligned Customers**

Customers who successfully ordered from at least one cuisine listed in their preferences.

**Explorers**

Customers who successfully ordered from at least one cuisine outside their stated preferences.

The following metrics were calculated:

* Customer count
* Successful order count
* Total spending
* Average Order Value

### Customer Classification

A rule-based classification system was implemented using defined thresholds.

Current thresholds:

```text
High Value Customer:
Successful spending > 10,000

Frequent Customer:
Successful orders > 10

At-Risk Customer:
Has ordered previously but has no successful order in the latest dataset period

Explorer:
Has successfully ordered from cuisines outside stated preferences
```

### Search Optimization

Two lookup approaches were implemented and compared:

1. Nested-loop search
2. Dictionary-based lookup

Complexity:

```text
Nested-loop lookup:
O(O × R)

Dictionary lookup:
O(O + R)
```

where:

* `O` = number of orders
* `R` = number of restaurants

The dictionary approach requires additional memory but provides faster repeated lookups.

### Sequence Analysis

Order sequences were analyzed to identify:

* Customers with consecutive successful orders
* Longest gap between successful orders
* Longest successful-order streak
* Day with the highest number of successful orders
* Day with the highest cancellation rate

The implementation derives dates from the dataset rather than hardcoding a fixed date range.

### Edge Cases

The implementation checks for cases such as:

* Empty lists
* Missing customers
* Missing restaurants
* Invalid order references
* Missing preferences
* Customers with no orders
* `None` values
* Zero quantities
* Invalid ratings

---

# Day 3 — OOP Design

The third stage converted the data and analytics logic into an object-oriented design.

## Core Classes

### Customer

Represents a customer and contains customer-specific information and behavior.

### Restaurant

Represents a restaurant and stores restaurant attributes such as cuisine, rating, city, and delivery fee.

### Order

Represents an order and provides methods such as:

```python
calculate_order_value()
is_successful()
```

### OrderItem

Represents an individual food item within an order and calculates item-level value.

### CustomerPreference

Represents the cuisine preferences associated with a customer.

### FoodDeliveryAnalytics

Acts as the business/analytics layer and provides reusable analytical methods such as:

```text
get_top_customers()
get_top_restaurants()
get_top_food_items()
get_customer_spending()
get_restaurant_performance()
get_customer_preferences()
get_explorer_customers()
```

---

## OOP Concepts Demonstrated

### Classes and Objects

Each raw record is converted into an appropriate Python object.

### Constructors

Classes use constructors to initialize their required attributes.

### Encapsulation

Data and related behavior are grouped within the relevant classes.

For example, an `Order` object is responsible for calculating its own order value.

### Inheritance

The project contains:

```text
OrderAnalyzer
├── SuccessfulOrderAnalyzer
└── CancelledOrderAnalyzer
```

The subclasses specialize order analysis based on order status.

### Polymorphism

Both analyzer classes implement the same analytical interface through an overridden `calculate_value()` method while applying status-specific behavior.

### Exception Handling

Custom exceptions are used for invalid entity lookups:

```text
InvalidDataError
EntityNotFoundError
```

For example, requesting a customer that does not exist raises an appropriate exception instead of causing an uncontrolled failure.

---

# 5. Assumptions

The following assumptions were made where the case study did not specify an exact interpretation.

### Order Value

Order value is calculated as:

```text
subtotal + delivery_fee - discount
```

### Successful Order

An order with:

```text
order_status == "Delivered"
```

is treated as a successful order.

### High-Value Threshold

A customer is considered high value when successful spending is greater than:

```text
10,000
```

### Frequent Customer Threshold

A customer is considered frequent when successful orders are greater than:

```text
10
```

### At-Risk Period

For the implemented classification, the latest period is interpreted as the **latest calendar month present in the dataset**.

A customer is considered at risk when they have ordered previously but have no successful order in that latest period.

### Customer Preferences

Preference alignment is based on cuisine. A customer is considered preference-aligned if they successfully ordered from at least one cuisine in their stated preferences.

An explorer is a customer who successfully ordered from at least one cuisine outside their preferences.

---

# 6. Data-Quality Decisions

The dataset intentionally contains anomalies.

Examples identified include:

* Duplicate customer records
* Duplicate restaurant records
* Duplicate order records
* Duplicate order-item records
* Duplicate IDs
* Missing customer segments
* Missing restaurant ratings
* Invalid customer references
* Invalid restaurant references
* Invalid order references
* Invalid ratings
* Invalid quantities
* Invalid cuisines
* Duplicate preferences
* Invalid discount values

### Important Decision

The raw records were **not silently corrected or manually deleted**.

Instead:

1. Validation functions identify the issue.
2. The issue is reported.
3. Analytical logic handles missing or invalid references where appropriate.
4. Data-quality limitations are documented.

One intentional consequence is that an invalid discount can produce a negative calculated order value. This is flagged as a data-quality issue rather than silently changing the original record.

---

# 7. Complexity Analysis

Important operations use dictionary and set-based lookups where repeated access is required.

| Operation                      | Approach                              | Complexity   |
| ------------------------------ | ------------------------------------- | ------------ |
| Dictionary lookup              | Hash-map lookup                       | O(1) average |
| Nested restaurant lookup       | Search each restaurant for each order | O(O × R)     |
| Dictionary restaurant lookup   | Build dictionary + process orders     | O(O + R)     |
| Frequency counting             | Dictionary                            | O(N)         |
| Set-based membership           | Set lookup                            | O(1) average |
| Sorting for ranking            | Sorting                               | O(N log N)   |
| Top-N ranking                  | Sort then slice                       | O(N log N)   |
| Customer preference membership | Set lookup                            | O(1) average |
| Date sequence analysis         | Sort dates                            | O(N log N)   |

Additional dictionary structures use extra memory in exchange for faster repeated lookups.

---

# 8. Key Results

### Order Performance

```text
Total Orders:       503
Delivered Orders:   416
Cancelled Orders:    61
Failed Orders:       26
Success Rate:       82.70%
Average Order Value: 1123.38
Total Order Value:  565060.00
```

### Top Customers by Successful Spending

```text
Priya Patel    -> 15992.00
Aarav Kumar    -> 13360.00
Anika Gupta    -> 12319.00
Aarav Patel    -> 10297.00
Anika Das      ->  9961.00
```

### Top Restaurants by Revenue

```text
Urban Fusion       -> 28877.00
Royal Diner        -> 24779.00
Royal Bowl         -> 24752.00
Tandoori Treats    -> 23430.00
The Grand Palace   -> 19857.00
```

### Top Food Items by Revenue

```text
Mojito             -> 196592.00
Chilli Paneer      ->  35446.00
Coke               ->  32712.00
Masala Chai        ->  32171.00
Cheesecake         ->  31889.00
```

---

# 9. How to Run

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run Day 1:

```bash
python day_1_analysis.py
```

Run Day 2:

```bash
python day_2_dsa.py
```

Run Day 3:

```bash
python day_3_oops.py
```

The dataset can be regenerated using:

```bash
python generate_dataset.py
```

---

# 10. Project Structure

```text
food_delivery_case_study/
│
├── data/
│   ├── customers.py
│   ├── restaurants.py
│   ├── orders.py
│   ├── order_items.py
│   └── customer_preferences.py
│
├── generate_dataset.py
├── day_1_analysis.py
├── day_2_dsa.py
├── day_3_oops.py
├── business_insights.md
├── README.md
└── .gitignore
```

---

# 11. Limitations

* The dataset is synthetically generated.
* The dataset intentionally contains data-quality anomalies.
* Thresholds for customer classification are analytical assumptions.
* At-risk classification depends on the selected latest-period interpretation.
* Business conclusions should not be treated as production-level conclusions without validating them against real operational data.
* No external analytics libraries were used because of the case-study restrictions.

---

# 12. Conclusion

This project demonstrates an end-to-end food delivery analytics workflow using Core Python.

The solution covers:

* Data validation
* Data profiling
* Business analysis
* Ranking
* Searching and optimization
* Frequency counting
* Set operations
* Customer classification
* Sequence analysis
* Complexity analysis
* Object-oriented design
* Inheritance
* Polymorphism
* Exception handling

The final analysis converts raw order data into customer, restaurant, product, and retention insights while demonstrating the ability to solve analytics problems using Core Python and DSA.
