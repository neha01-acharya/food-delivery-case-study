from collections import Counter, defaultdict
from datetime import datetime
import time

from data.customers import customers
from data.restaurants import restaurants
from data.orders import orders
from data.order_items import order_items
from data.customer_preferences import customer_preferences


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_order_value(order):
    """
    Order value = subtotal + delivery fee - discount
    """
    return (
        order.get("subtotal", 0)
        + order.get("delivery_fee", 0)
        - order.get("discount", 0)
    )


def is_successful(order):
    return order.get("order_status") == "Delivered"


def parse_date(date_string):
    """
    Convert YYYY-MM-DD string into a datetime object.
    Returns None for invalid/missing dates.
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except (TypeError, ValueError):
        return None


# ============================================================
# LOOKUP DICTIONARIES
# ============================================================

customer_lookup = {
    customer.get("customer_id"): customer
    for customer in customers
    if customer.get("customer_id") is not None
}

restaurant_lookup = {
    restaurant.get("restaurant_id"): restaurant
    for restaurant in restaurants
    if restaurant.get("restaurant_id") is not None
}

order_lookup = {
    order.get("order_id"): order
    for order in orders
    if order.get("order_id") is not None
}

preference_lookup = customer_preferences


# ============================================================
# TASK 1 — REUSABLE RANKING ENGINE
# ============================================================

def rank_entities(data, metric_function, top_n=5, reverse=True):
    """
    Generic ranking function.

    data:
        Input list of records.

    metric_function:
        Function that calculates the ranking metric.

    top_n:
        Number of results to return.

    reverse:
        True -> highest first
        False -> lowest first
    """

    results = []

    for item in data:
        try:
            metric = metric_function(item)
            results.append((item, metric))
        except (TypeError, ValueError, KeyError):
            continue

    results.sort(key=lambda x: x[1], reverse=reverse)

    return results[:top_n]


def get_customer_successful_orders(customer_id):
    return [
        order
        for order in orders
        if order.get("customer_id") == customer_id
        and is_successful(order)
    ]


def get_customer_spending(customer_id):
    return sum(
        calculate_order_value(order)
        for order in get_customer_successful_orders(customer_id)
    )


def get_restaurant_successful_orders(restaurant_id):
    return [
        order
        for order in orders
        if order.get("restaurant_id") == restaurant_id
        and is_successful(order)
    ]


def get_restaurant_revenue(restaurant_id):
    return sum(
        calculate_order_value(order)
        for order in get_restaurant_successful_orders(restaurant_id)
    )


def get_item_quantity(item_name):
    return sum(
        item.get("quantity", 0)
        for item in order_items
        if item.get("item_name") == item_name
    )


def get_item_revenue(item_name):
    return sum(
        item.get("quantity", 0) * item.get("unit_price", 0)
        for item in order_items
        if item.get("item_name") == item_name
    )


def show_rankings():
    print("\n" + "=" * 60)
    print("TASK 1 — RANKING ENGINE")
    print("=" * 60)

    # Top customers by successful spending
    print("\nTop 5 Customers by Successful Spending:")

    customer_rankings = rank_entities(
        customers,
        lambda customer: get_customer_spending(
            customer.get("customer_id")
        ),
        top_n=5
    )

    for customer, value in customer_rankings:
        print(
            f"{customer.get('customer_name')} -> "
            f"{value:.2f}"
        )

    # Top restaurants by revenue
    print("\nTop 5 Restaurants by Revenue:")

    restaurant_rankings = rank_entities(
        restaurants,
        lambda restaurant: get_restaurant_revenue(
            restaurant.get("restaurant_id")
        ),
        top_n=5
    )

    for restaurant, value in restaurant_rankings:
        print(
            f"{restaurant.get('restaurant_name')} -> "
            f"{value:.2f}"
        )

    # Top food items by quantity
    item_names = list({
        item.get("item_name")
        for item in order_items
        if item.get("item_name")
    })

    print("\nTop 5 Food Items by Quantity:")

    item_rankings = rank_entities(
        item_names,
        lambda item_name: get_item_quantity(item_name),
        top_n=5
    )

    for item_name, quantity in item_rankings:
        print(f"{item_name} -> {quantity}")

    # Top cuisines by number of restaurants
    cuisine_counter = Counter(
        restaurant.get("cuisine")
        for restaurant in restaurants
        if restaurant.get("cuisine")
    )

    print("\nTop 5 Cuisines by Restaurant Count:")

    for cuisine, count in cuisine_counter.most_common(5):
        print(f"{cuisine} -> {count}")

    # Top cities by customer count
    city_counter = Counter(
        customer.get("city")
        for customer in customers
        if customer.get("city")
    )

    print("\nTop 5 Cities by Customer Count:")

    for city, count in city_counter.most_common(5):
        print(f"{city} -> {count}")


# ============================================================
# TASK 2 — CUSTOMER PREFERENCE ANALYSIS
# ============================================================

def analyze_customer_preferences():
    print("\n" + "=" * 60)
    print("TASK 2 — CUSTOMER PREFERENCE ANALYSIS")
    print("=" * 60)

    aligned_customers = set()
    explorer_customers = set()

    customer_order_counts = Counter()
    customer_spending = defaultdict(float)

    for order in orders:

        if not is_successful(order):
            continue

        customer_id = order.get("customer_id")
        restaurant_id = order.get("restaurant_id")

        restaurant = restaurant_lookup.get(restaurant_id)

        if restaurant is None:
            continue

        cuisine = restaurant.get("cuisine")

        preferences = preference_lookup.get(customer_id, [])

        if preferences is None:
            preferences = []

        customer_order_counts[customer_id] += 1
        customer_spending[customer_id] += calculate_order_value(order)

        if cuisine in preferences:
            aligned_customers.add(customer_id)

        else:
            explorer_customers.add(customer_id)

    def group_metrics(customer_ids):

        total_orders = sum(
            customer_order_counts[customer_id]
            for customer_id in customer_ids
        )

        total_spending = sum(
            customer_spending[customer_id]
            for customer_id in customer_ids
        )

        average_order_value = (
            total_spending / total_orders
            if total_orders > 0
            else 0
        )

        return {
            "customers": len(customer_ids),
            "orders": total_orders,
            "spending": total_spending,
            "average_order_value": average_order_value
        }

    aligned_metrics = group_metrics(aligned_customers)
    explorer_metrics = group_metrics(explorer_customers)

    print("\nPreference-Aligned Customers:")
    print(f"Customers: {aligned_metrics['customers']}")
    print(f"Orders: {aligned_metrics['orders']}")
    print(f"Total Spending: {aligned_metrics['spending']:.2f}")
    print(
        f"Average Order Value: "
        f"{aligned_metrics['average_order_value']:.2f}"
    )

    print("\nExplorer Customers:")
    print(f"Customers: {explorer_metrics['customers']}")
    print(f"Orders: {explorer_metrics['orders']}")
    print(f"Total Spending: {explorer_metrics['spending']:.2f}")
    print(
        f"Average Order Value: "
        f"{explorer_metrics['average_order_value']:.2f}"
    )

    return aligned_customers, explorer_customers


# ============================================================
# TASK 3 — CUSTOMER BEHAVIOR CLASSIFICATION
# ============================================================

# The case study says to define thresholds but does not prescribe
# exact numerical values.
HIGH_VALUE_THRESHOLD = 10000
FREQUENT_ORDER_THRESHOLD = 10


def classify_customer(customer_id, explorer_customers):
    successful_orders = get_customer_successful_orders(customer_id)

    successful_spending = sum(
        calculate_order_value(order)
        for order in successful_orders
    )

    # High Value
    if successful_spending > HIGH_VALUE_THRESHOLD:
        return "High Value Customer"

    # Frequent
    if len(successful_orders) > FREQUENT_ORDER_THRESHOLD:
        return "Frequent Customer"

    # Explorer
    if customer_id in explorer_customers:
        return "Explorer"

    # At-Risk
    all_customer_orders = [
        order
        for order in orders
        if order.get("customer_id") == customer_id
    ]

    if all_customer_orders and not successful_orders:
        return "At-Risk Customer"

    if all_customer_orders:

        dates = [
            parse_date(order.get("order_date"))
            for order in all_customer_orders
        ]

        dates = [date for date in dates if date is not None]

        successful_dates = [
            parse_date(order.get("order_date"))
            for order in successful_orders
        ]

        successful_dates = [
            date for date in successful_dates
            if date is not None
        ]

        if dates and successful_dates:

            latest_order_date = max(dates)
            latest_successful_date = max(successful_dates)

            # Latest calendar month in the dataset is treated
            # as the latest period.
            latest_period = (
                latest_order_date.year,
                latest_order_date.month
            )

            successful_periods = {
                (date.year, date.month)
                for date in successful_dates
            }

            if latest_period not in successful_periods:
                return "At-Risk Customer"

    return "Regular Customer"


def classify_customers(explorer_customers):
    print("\n" + "=" * 60)
    print("TASK 3 — CUSTOMER BEHAVIOR CLASSIFICATION")
    print("=" * 60)

    classifications = {}

    for customer in customers:

        customer_id = customer.get("customer_id")

        if customer_id is None:
            continue

        classifications[customer_id] = classify_customer(
            customer_id,
            explorer_customers
        )

    counts = Counter(classifications.values())

    print("\nCustomer Classification Counts:")

    for category, count in counts.items():
        print(f"{category}: {count}")

    print("\nSample Classifications:")

    displayed = 0

    for customer in customers:

        customer_id = customer.get("customer_id")

        if customer_id not in classifications:
            continue

        print(
            f"{customer.get('customer_name')} -> "
            f"{classifications[customer_id]}"
        )

        displayed += 1

        if displayed == 10:
            break

    return classifications


# ============================================================
# TASK 4 — SEARCH & OPTIMIZATION
# ============================================================

def find_restaurant_nested(order, restaurants_list):
    """
    Approach 1:
    Search restaurant using a nested loop.

    Time complexity:
    O(R) per order
    """

    restaurant_id = order.get("restaurant_id")

    for restaurant in restaurants_list:

        if restaurant.get("restaurant_id") == restaurant_id:
            return restaurant

    return None


def find_restaurant_dictionary(order, restaurant_dict):
    """
    Approach 2:
    Search restaurant using dictionary lookup.

    Average time complexity:
    O(1)
    """

    return restaurant_dict.get(order.get("restaurant_id"))


def benchmark_lookup_methods():

    print("\n" + "=" * 60)
    print("TASK 4 — SEARCH & OPTIMIZATION")
    print("=" * 60)

    # Nested-loop approach
    start_time = time.perf_counter()

    nested_results = []

    for order in orders:
        restaurant = find_restaurant_nested(
            order,
            restaurants
        )

        nested_results.append(restaurant)

    nested_time = time.perf_counter() - start_time

    # Dictionary approach
    start_time = time.perf_counter()

    dictionary_results = []

    for order in orders:
        restaurant = find_restaurant_dictionary(
            order,
            restaurant_lookup
        )

        dictionary_results.append(restaurant)

    dictionary_time = time.perf_counter() - start_time

    print(f"\nNested-loop lookup time: {nested_time:.8f} seconds")
    print(
        f"Dictionary lookup time: "
        f"{dictionary_time:.8f} seconds"
    )

    print("\nComplexity:")
    print("Nested-loop: O(O × R)")
    print("Dictionary: O(O + R)")

    print("\nSpace Trade-off:")
    print(
        "Nested-loop: O(1) additional lookup space "
        "but slower searches."
    )

    print(
        "Dictionary: O(R) additional space "
        "but approximately O(1) lookup."
    )

    print("\nWhen to use:")
    print(
        "Nested-loop -> small datasets or one-off searches "
        "where simplicity matters."
    )

    print(
        "Dictionary -> repeated lookups and larger datasets "
        "where lookup speed matters."
    )


# ============================================================
# TASK 5 — SEQUENCE ANALYSIS
# ============================================================

def build_successful_order_history():

    history = defaultdict(list)

    for order in orders:

        if not is_successful(order):
            continue

        customer_id = order.get("customer_id")
        order_date = parse_date(order.get("order_date"))

        if customer_id is None or order_date is None:
            continue

        history[customer_id].append(order_date)

    for customer_id in history:
        history[customer_id].sort()

    return history


def find_consecutive_successful_orders():

    history = build_successful_order_history()

    consecutive_customers = set()

    for customer_id, dates in history.items():

        for i in range(1, len(dates)):

            gap = (dates[i] - dates[i - 1]).days

            if gap == 1:
                consecutive_customers.add(customer_id)
                break

    return consecutive_customers


def find_longest_gap():

    history = build_successful_order_history()

    longest_gap = -1
    longest_gap_customer = None

    for customer_id, dates in history.items():

        for i in range(1, len(dates)):

            gap = (dates[i] - dates[i - 1]).days

            if gap > longest_gap:
                longest_gap = gap
                longest_gap_customer = customer_id

    return longest_gap_customer, longest_gap


def find_longest_streak():

    history = build_successful_order_history()

    longest_streak = 0
    longest_customer = None

    for customer_id, dates in history.items():

        if not dates:
            continue

        current_streak = 1

        for i in range(1, len(dates)):

            gap = (dates[i] - dates[i - 1]).days

            if gap == 1:
                current_streak += 1
            else:
                current_streak = 1

            if current_streak > longest_streak:
                longest_streak = current_streak
                longest_customer = customer_id

    return longest_customer, longest_streak


def find_day_with_highest_successful_orders():

    successful_orders_by_day = Counter()

    for order in orders:

        if not is_successful(order):
            continue

        date = order.get("order_date")

        if date:
            successful_orders_by_day[date] += 1

    if not successful_orders_by_day:
        return None, 0

    return successful_orders_by_day.most_common(1)[0]


def find_day_with_highest_cancellation_rate():

    daily_total = Counter()
    daily_cancelled = Counter()

    for order in orders:

        date = order.get("order_date")

        if not date:
            continue

        daily_total[date] += 1

        if order.get("order_status") == "Cancelled":
            daily_cancelled[date] += 1

    if not daily_total:
        return None, 0

    cancellation_rates = {}

    for date, total in daily_total.items():

        if total == 0:
            continue

        cancellation_rates[date] = (
            daily_cancelled[date] / total
        )

    if not cancellation_rates:
        return None, 0

    highest_day = max(
        cancellation_rates,
        key=cancellation_rates.get
    )

    return highest_day, cancellation_rates[highest_day]


def show_sequence_analysis():

    print("\n" + "=" * 60)
    print("TASK 5 — SEQUENCE ANALYSIS")
    print("=" * 60)

    consecutive_customers = find_consecutive_successful_orders()

    print(
        "\nCustomers with consecutive successful orders:"
    )

    for customer_id in sorted(consecutive_customers):
        customer = customer_lookup.get(customer_id)

        if customer:
            print(
                f"{customer.get('customer_name')} "
                f"(ID: {customer_id})"
            )
        else:
            print(customer_id)

    longest_gap_customer, longest_gap = find_longest_gap()

    if longest_gap_customer is not None:

        customer = customer_lookup.get(longest_gap_customer)

        print(
            "\nLongest gap between successful orders:"
        )

        print(
            f"{customer.get('customer_name') if customer else longest_gap_customer}"
            f" -> {longest_gap} days"
        )

    longest_customer, longest_streak = find_longest_streak()

    if longest_customer is not None:

        customer = customer_lookup.get(longest_customer)

        print(
            "\nLongest successful-order streak:"
        )

        print(
            f"{customer.get('customer_name') if customer else longest_customer}"
            f" -> {longest_streak} consecutive days"
        )

    highest_success_day, success_count = (
        find_day_with_highest_successful_orders()
    )

    print(
        "\nDay with highest number of successful orders:"
    )

    print(
        f"{highest_success_day} -> {success_count} orders"
    )

    highest_cancel_day, cancel_rate = (
        find_day_with_highest_cancellation_rate()
    )

    print(
        "\nDay with highest cancellation rate:"
    )

    print(
        f"{highest_cancel_day} -> "
        f"{cancel_rate * 100:.2f}%"
    )


# ============================================================
# TASK 6 — EDGE CASE HANDLING
# ============================================================

def edge_case_checks():

    print("\n" + "=" * 60)
    print("TASK 6 — EDGE CASE HANDLING")
    print("=" * 60)

    # Empty list
    empty_result = rank_entities(
        [],
        lambda x: x,
        top_n=5
    )

    print(
        f"\nEmpty list handled: "
        f"{empty_result == []}"
    )

    # Missing customer
    missing_customer = customer_lookup.get(999999)

    print(
        f"Missing customer handled: "
        f"{missing_customer is None}"
    )

    # Missing restaurant
    missing_restaurant = restaurant_lookup.get(999999)

    print(
        f"Missing restaurant handled: "
        f"{missing_restaurant is None}"
    )

    # Invalid order reference
    invalid_order = order_lookup.get(999999)

    print(
        f"Invalid order reference handled: "
        f"{invalid_order is None}"
    )

    # Customer with no preferences
    no_preferences_customer = None

    for customer_id, preferences in preference_lookup.items():

        if not preferences:
            no_preferences_customer = customer_id
            break

    print(
        f"Customer with no preferences found: "
        f"{no_preferences_customer is not None}"
    )

    # Customer with no orders
    customers_with_orders = {
        order.get("customer_id")
        for order in orders
        if order.get("customer_id") is not None
    }

    no_order_customers = [
        customer.get("customer_id")
        for customer in customers
        if customer.get("customer_id")
        not in customers_with_orders
    ]

    print(
        f"Customers with no orders handled: "
        f"{len(no_order_customers)}"
    )

    # None values
    none_customer_segments = sum(
        1
        for customer in customers
        if customer.get("customer_segment") is None
    )

    print(
        f"None values handled: "
        f"{none_customer_segments}"
    )

    # Zero quantity
    zero_quantity_items = sum(
        1
        for item in order_items
        if item.get("quantity") == 0
    )

    print(
        f"Zero quantity records found: "
        f"{zero_quantity_items}"
    )

    # Invalid ratings
    invalid_ratings = []

    for restaurant in restaurants:

        rating = restaurant.get("rating")

        if rating is None:
            continue

        if not 0 <= rating <= 5:
            invalid_ratings.append(
                restaurant.get("restaurant_id")
            )

    print(
        f"Invalid ratings handled: "
        f"{len(invalid_ratings)}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("DAY 2 — DSA & ALGORITHMIC ANALYSIS")
    print("=" * 60)

    show_rankings()

    aligned_customers, explorer_customers = (
        analyze_customer_preferences()
    )

    classifications = classify_customers(
        explorer_customers
    )

    benchmark_lookup_methods()

    show_sequence_analysis()

    edge_case_checks()

    print("\n" + "=" * 60)
    print("DAY 2 ANALYSIS COMPLETED")
    print("=" * 60)