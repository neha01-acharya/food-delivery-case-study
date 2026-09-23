from data.customers import customers
from data.restaurants import restaurants
from data.orders import orders
from data.order_items import order_items
from data.customer_preferences import customer_preferences

from collections import Counter, defaultdict
from datetime import datetime


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_valid_customer_ids():
    return {customer["customer_id"] for customer in customers}


def get_valid_restaurant_ids():
    return {restaurant["restaurant_id"] for restaurant in restaurants}


def get_valid_order_ids():
    return {order["order_id"] for order in orders}


# ============================================================
# VALIDATION
# ============================================================

def find_duplicate_records(data):
    seen = set()
    duplicates = []

    for record in data:
        record_key = str(record)

        if record_key in seen:
            duplicates.append(record)
        else:
            seen.add(record_key)

    return duplicates


def find_duplicate_ids(data, id_field):
    seen = set()
    duplicates = []

    for record in data:
        record_id = record.get(id_field)

        if record_id in seen:
            duplicates.append(record_id)
        else:
            seen.add(record_id)

    return duplicates


def find_missing_values(data):
    missing = []

    for index, record in enumerate(data):
        missing_fields = []

        for key, value in record.items():
            if value is None or value == "":
                missing_fields.append(key)

        if missing_fields:
            missing.append({
                "index": index,
                "missing_fields": missing_fields
            })

    return missing


def validate_customer_references():
    valid_customer_ids = get_valid_customer_ids()
    invalid_orders = []

    for order in orders:
        if order.get("customer_id") not in valid_customer_ids:
            invalid_orders.append(order)

    return invalid_orders


def validate_restaurant_references():
    valid_restaurant_ids = get_valid_restaurant_ids()
    invalid_orders = []

    for order in orders:
        if order.get("restaurant_id") not in valid_restaurant_ids:
            invalid_orders.append(order)

    return invalid_orders


def validate_order_references():
    valid_order_ids = get_valid_order_ids()
    invalid_items = []

    for item in order_items:
        if item.get("order_id") not in valid_order_ids:
            invalid_items.append(item)

    return invalid_items


def validate_ratings():
    invalid = []

    for restaurant in restaurants:
        rating = restaurant.get("rating")

        if rating is not None and not (0 <= rating <= 5):
            invalid.append(restaurant)

    return invalid


def validate_quantities():
    invalid = []

    for item in order_items:
        quantity = item.get("quantity")

        if quantity is None or quantity <= 0:
            invalid.append(item)

    return invalid


def validate_cuisines():
    valid_cuisines = {
        restaurant["cuisine"]
        for restaurant in restaurants
        if restaurant.get("cuisine") is not None
    }

    invalid = []
    duplicate_preferences = []

    for customer_id, preferences in customer_preferences.items():

        seen = set()

        for cuisine in preferences:

            # Invalid cuisine
            if cuisine not in valid_cuisines:
                invalid.append({
                    "customer_id": customer_id,
                    "cuisine": cuisine
                })

            # Duplicate cuisine preference
            if cuisine in seen:
                duplicate_preferences.append({
                    "customer_id": customer_id,
                    "cuisine": cuisine
                })

            seen.add(cuisine)

    return invalid, duplicate_preferences
def validate_discounts():
    invalid = []

    for order in orders:

        subtotal = order.get("subtotal", 0)
        delivery_fee = order.get("delivery_fee", 0)
        discount = order.get("discount", 0)

        order_value = subtotal + delivery_fee - discount

        if discount < 0 or discount > subtotal + delivery_fee:
            invalid.append(order)

        elif order_value < 0:
            invalid.append(order)

    return invalid

def run_validation():

    print("\n" + "=" * 70)
    print("DATA VALIDATION")
    print("=" * 70)

    print("\n--- Duplicate Records ---")

    print("Customer duplicates:",
          len(find_duplicate_records(customers)))

    print("Restaurant duplicates:",
          len(find_duplicate_records(restaurants)))

    print("Order duplicates:",
          len(find_duplicate_records(orders)))

    print("Order item duplicates:",
          len(find_duplicate_records(order_items)))

    print("\n--- Duplicate IDs ---")

    print("Duplicate customer IDs:",
          find_duplicate_ids(customers, "customer_id"))

    print("Duplicate restaurant IDs:",
          find_duplicate_ids(restaurants, "restaurant_id"))

    print("Duplicate order IDs:",
          find_duplicate_ids(orders, "order_id"))

    print("\n--- Missing Values ---")

    print("Customer missing values:",
          find_missing_values(customers))

    print("Restaurant missing values:",
          find_missing_values(restaurants))

    print("Order missing values:",
          find_missing_values(orders))

    print("Order item missing values:",
          find_missing_values(order_items))

    print("\n--- Invalid References ---")

    print("Invalid customer references:",
          len(validate_customer_references()))

    print("Invalid restaurant references:",
          len(validate_restaurant_references()))

    print("Invalid order references:",
          len(validate_order_references()))

    print("\n--- Data Quality Rules ---")

    print("Invalid ratings:",
          len(validate_ratings()))

    print("Invalid quantities:",
          len(validate_quantities()))

    invalid_cuisines, duplicate_preferences = validate_cuisines()

    print("Invalid cuisines:",
      len(invalid_cuisines))

    print("Duplicate preferences:",
      len(duplicate_preferences))       
    
    print("Invalid discounts:",
          len(validate_discounts()))


# ============================================================
# BASIC PROFILING
# ============================================================

def profile_data():

    print("\n" + "=" * 70)
    print("BASIC DATA PROFILING")
    print("=" * 70)

    print("\nDataset counts")
    print("-" * 40)

    print("Customers:", len(customers))
    print("Restaurants:", len(restaurants))
    print("Orders:", len(orders))
    print("Order Items:", len(order_items))
    print("Customer Preferences:", len(customer_preferences))

    print("\nCustomer cities")
    print("-" * 40)

    city_counts = Counter(
        customer["city"]
        for customer in customers
        if customer.get("city") is not None
    )

    for city, count in city_counts.most_common():
        print(city, ":", count)

    print("\nCustomer segments")
    print("-" * 40)

    segment_counts = Counter(
        customer.get("customer_segment")
        for customer in customers
    )

    for segment, count in segment_counts.items():
        print(segment, ":", count)

    print("\nRestaurant cuisines")
    print("-" * 40)

    cuisine_counts = Counter(
        restaurant.get("cuisine")
        for restaurant in restaurants
        if restaurant.get("cuisine") is not None
    )

    for cuisine, count in cuisine_counts.most_common():
        print(cuisine, ":", count)

    print("\nOrder status")
    print("-" * 40)

    status_counts = Counter(
        order.get("order_status")
        for order in orders
    )

    for status, count in status_counts.items():
        print(status, ":", count)


# ============================================================
# ORDER ANALYSIS
# ============================================================

def calculate_order_value(order):
    return (
        order.get("subtotal", 0)
        + order.get("delivery_fee", 0)
        - order.get("discount", 0)
    )


def order_analysis():

    print("\n" + "=" * 70)
    print("ORDER ANALYSIS")
    print("=" * 70)

    total_orders = len(orders)

    delivered_orders = [
        order for order in orders
        if order.get("order_status") == "Delivered"
    ]

    cancelled_orders = [
        order for order in orders
        if order.get("order_status") == "Cancelled"
    ]

    failed_orders = [
        order for order in orders
        if order.get("order_status") == "Failed"
    ]

    successful_count = len(delivered_orders)

    order_values = [
        calculate_order_value(order)
        for order in orders
    ]

    total_value = sum(order_values)

    aov = (
        total_value / total_orders
        if total_orders
        else 0
    )

    success_rate = (
        successful_count / total_orders * 100
        if total_orders
        else 0
    )

    discounts = [
        order.get("discount", 0)
        for order in orders
    ]

    print("Total orders:", total_orders)
    print("Delivered orders:", len(delivered_orders))
    print("Cancelled orders:", len(cancelled_orders))
    print("Failed orders:", len(failed_orders))

    print(f"Success rate: {success_rate:.2f}%")
    print(f"Total order value: {total_value:.2f}")
    print(f"Average Order Value: {aov:.2f}")

    if order_values:
        print(f"Minimum order value: {min(order_values):.2f}")
        print(f"Maximum order value: {max(order_values):.2f}")

    print(f"Total discount: {sum(discounts):.2f}")
# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

def customer_analysis():

    print("\n" + "=" * 70)
    print("CUSTOMER ANALYSIS")
    print("=" * 70)

    customer_orders = defaultdict(list)

    for order in orders:
        customer_orders[order.get("customer_id")].append(order)

    customer_summary = []

    for customer in customers:

        customer_id = customer["customer_id"]

        customer_order_list = customer_orders.get(
            customer_id,
            []
        )

        successful_orders = [
            order for order in customer_order_list
            if order.get("order_status") == "Delivered"
        ]

        spending = sum(
            calculate_order_value(order)
            for order in successful_orders
        )

        aov = (
            spending / len(successful_orders)
            if successful_orders
            else 0
        )

        customer_summary.append({
            "customer_id": customer_id,
            "customer_name": customer["customer_name"],
            "orders": len(customer_order_list),
            "successful_orders": len(successful_orders),
            "spending": spending,
            "aov": aov
        })

    top_spenders = sorted(
        customer_summary,
        key=lambda x: x["spending"],
        reverse=True
    )[:10]

    top_successful = sorted(
        customer_summary,
        key=lambda x: x["successful_orders"],
        reverse=True
    )[:10]

    no_successful = [
        customer
        for customer in customer_summary
        if customer["successful_orders"] == 0
    ]

    never_ordered = [
        customer
        for customer in customer_summary
        if customer["orders"] == 0
    ]

    print("\nTop 10 customers by spending")

    for customer in top_spenders:
        print(
            customer["customer_name"],
            "->",
            round(customer["spending"], 2)
        )

    print("\nTop 10 customers by successful orders")

    for customer in top_successful:
        print(
            customer["customer_name"],
            "->",
            customer["successful_orders"]
        )

    print("\nCustomers with no successful orders:",
          len(no_successful))

    print("Customers who never ordered:",
          len(never_ordered))

    return customer_summary


# ============================================================
# RESTAURANT ANALYSIS
# ============================================================

def restaurant_analysis():

    print("\n" + "=" * 70)
    print("RESTAURANT ANALYSIS")
    print("=" * 70)

    restaurant_orders = defaultdict(list)

    for order in orders:
        restaurant_orders[order.get("restaurant_id")].append(order)

    restaurant_summary = []

    for restaurant in restaurants:

        restaurant_id = restaurant["restaurant_id"]

        restaurant_order_list = restaurant_orders.get(
            restaurant_id,
            []
        )

        successful_orders = [
            order
            for order in restaurant_order_list
            if order.get("order_status") == "Delivered"
        ]

        cancelled_orders = [
            order
            for order in restaurant_order_list
            if order.get("order_status") == "Cancelled"
        ]

        revenue = sum(
            calculate_order_value(order)
            for order in successful_orders
        )

        aov = (
            revenue / len(successful_orders)
            if successful_orders
            else 0
        )

        cancellation_rate = (
            len(cancelled_orders) /
            len(restaurant_order_list) * 100
            if restaurant_order_list
            else 0
        )

        restaurant_summary.append({
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant["restaurant_name"],
            "orders": len(restaurant_order_list),
            "successful_orders": len(successful_orders),
            "cancelled_orders": len(cancelled_orders),
            "revenue": revenue,
            "aov": aov,
            "cancellation_rate": cancellation_rate,
            "rating": restaurant.get("rating")
        })

    top_revenue = sorted(
        restaurant_summary,
        key=lambda x: x["revenue"],
        reverse=True
    )[:5]

    top_successful = sorted(
        restaurant_summary,
        key=lambda x: x["successful_orders"],
        reverse=True
    )[:5]

    highest_aov = sorted(
        restaurant_summary,
        key=lambda x: x["aov"],
        reverse=True
    )[:5]

    highest_cancellation = sorted(
        restaurant_summary,
        key=lambda x: x["cancellation_rate"],
        reverse=True
    )[:5]

    print("\nTop 5 restaurants by revenue")

    for restaurant in top_revenue:
        print(
            restaurant["restaurant_name"],
            "->",
            round(restaurant["revenue"], 2)
        )

    print("\nTop 5 restaurants by successful orders")

    for restaurant in top_successful:
        print(
            restaurant["restaurant_name"],
            "->",
            restaurant["successful_orders"]
        )

    print("\nTop 5 restaurants by AOV")

    for restaurant in highest_aov:
        print(
            restaurant["restaurant_name"],
            "->",
            round(restaurant["aov"], 2)
        )

    print("\nTop 5 restaurants by cancellation rate")

    for restaurant in highest_cancellation:
        print(
            restaurant["restaurant_name"],
            "->",
            round(restaurant["cancellation_rate"], 2),
            "%"
        )

    return restaurant_summary


# ============================================================
# ORDER ITEM ANALYSIS
# ============================================================

def order_item_analysis():

    print("\n" + "=" * 70)
    print("ORDER ITEM ANALYSIS")
    print("=" * 70)

    item_frequency = Counter()
    item_quantity = Counter()
    category_revenue = Counter()
    item_revenue = Counter()
    restaurant_item_count = Counter()

    total_quantity = 0

    for item in order_items:

        item_name = item.get("item_name")
        category = item.get("category")
        quantity = item.get("quantity", 0)
        unit_price = item.get("unit_price", 0)
        restaurant_id = item.get("restaurant_id")

        item_frequency[item_name] += 1
        item_quantity[item_name] += quantity

        revenue = quantity * unit_price

        category_revenue[category] += revenue
        item_revenue[item_name] += revenue

        restaurant_item_count[restaurant_id] += 1

        total_quantity += quantity

    average_quantity = (
        total_quantity / len(order_items)
        if order_items
        else 0
    )

    print("\nMost frequently ordered items")

    for item, count in item_frequency.most_common(10):
        print(item, "->", count)

    print("\nTop 10 items by quantity")

    for item, quantity in item_quantity.most_common(10):
        print(item, "->", quantity)

    print("\nCategory revenue")

    for category, revenue in category_revenue.most_common():
        print(category, "->", round(revenue, 2))

    print("\nAverage quantity per order item:",
          round(average_quantity, 2))

    print("\nTop 5 items by revenue")

    for item, revenue in item_revenue.most_common(5):
        print(item, "->", round(revenue, 2))


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_validation()

    profile_data()

    order_analysis()

    customer_analysis()

    restaurant_analysis()

    order_item_analysis()