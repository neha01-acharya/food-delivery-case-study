from collections import defaultdict


# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class InvalidDataError(Exception):
    """Raised when invalid business data is provided."""
    pass


class EntityNotFoundError(Exception):
    """Raised when a requested entity does not exist."""
    pass


# ============================================================
# CUSTOMER CLASS
# ============================================================

class Customer:

    def __init__(
        self,
        customer_id,
        customer_name,
        city,
        signup_date,
        customer_segment
    ):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.city = city
        self.signup_date = signup_date
        self.customer_segment = customer_segment

    def get_customer_info(self):
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "city": self.city,
            "signup_date": self.signup_date,
            "customer_segment": self.customer_segment
        }

    def __str__(self):
        return f"{self.customer_name} ({self.customer_id})"


# ============================================================
# RESTAURANT CLASS
# ============================================================

class Restaurant:

    def __init__(
        self,
        restaurant_id,
        restaurant_name,
        city,
        cuisine,
        rating,
        delivery_fee
    ):
        self.restaurant_id = restaurant_id
        self.restaurant_name = restaurant_name
        self.city = city
        self.cuisine = cuisine
        self.rating = rating
        self.delivery_fee = delivery_fee

    def is_valid_rating(self):
        if self.rating is None:
            return False

        return 0 <= self.rating <= 5

    def get_restaurant_info(self):
        return {
            "restaurant_id": self.restaurant_id,
            "restaurant_name": self.restaurant_name,
            "city": self.city,
            "cuisine": self.cuisine,
            "rating": self.rating,
            "delivery_fee": self.delivery_fee
        }

    def __str__(self):
        return f"{self.restaurant_name} ({self.restaurant_id})"


# ============================================================
# ORDER CLASS
# ============================================================

class Order:

    def __init__(
        self,
        order_id,
        customer_id,
        restaurant_id,
        order_date,
        order_status,
        payment_method,
        subtotal,
        delivery_fee,
        discount
    ):
        self.order_id = order_id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.order_date = order_date
        self.order_status = order_status
        self.payment_method = payment_method
        self.subtotal = subtotal
        self.delivery_fee = delivery_fee
        self.discount = discount

    def calculate_order_value(self):
        return (
            self.subtotal
            + self.delivery_fee
            - self.discount
        )

    def is_successful(self):
        return self.order_status == "Delivered"

    def is_cancelled(self):
        return self.order_status == "Cancelled"

    def get_order_info(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "restaurant_id": self.restaurant_id,
            "order_date": self.order_date,
            "order_status": self.order_status,
            "order_value": self.calculate_order_value()
        }

    def __str__(self):
        return f"Order {self.order_id}"


# ============================================================
# ORDER ITEM CLASS
# ============================================================

class OrderItem:

    def __init__(
        self,
        order_id,
        item_name,
        category,
        quantity,
        unit_price
    ):
        self.order_id = order_id
        self.item_name = item_name
        self.category = category
        self.quantity = quantity
        self.unit_price = unit_price

    def calculate_item_value(self):
        return self.quantity * self.unit_price

    def is_valid_quantity(self):
        return self.quantity > 0

    def get_item_info(self):
        return {
            "order_id": self.order_id,
            "item_name": self.item_name,
            "category": self.category,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "item_value": self.calculate_item_value()
        }

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"


# ============================================================
# CUSTOMER PREFERENCE CLASS
# ============================================================

class CustomerPreference:

    def __init__(self, customer_id, preferences):
        self.customer_id = customer_id
        self.preferences = preferences or []

    def add_preference(self, cuisine):
        if cuisine not in self.preferences:
            self.preferences.append(cuisine)

    def has_preference(self, cuisine):
        return cuisine in self.preferences

    def get_preferences(self):
        return list(self.preferences)

    def __str__(self):
        return (
            f"Customer {self.customer_id}: "
            f"{', '.join(self.preferences)}"
        )


# ============================================================
# INHERITANCE + POLYMORPHISM
# ============================================================

class OrderAnalyzer:

    def calculate_value(self, order):
        return order.calculate_order_value()


class SuccessfulOrderAnalyzer(OrderAnalyzer):

    def calculate_value(self, order):
        if order.is_successful():
            return order.calculate_order_value()

        return 0


class CancelledOrderAnalyzer(OrderAnalyzer):

    def calculate_value(self, order):
        if order.is_cancelled():
            return order.calculate_order_value()

        return 0


# ============================================================
# ANALYTICS CLASS
# ============================================================

class FoodDeliveryAnalytics:

    def __init__(
        self,
        customers,
        restaurants,
        orders,
        order_items,
        customer_preferences
    ):

        self.customers = customers
        self.restaurants = restaurants
        self.orders = orders
        self.order_items = order_items
        self.customer_preferences = customer_preferences

        # Dictionary indexes
        self.customer_lookup = {
            customer.customer_id: customer
            for customer in customers
        }

        self.restaurant_lookup = {
            restaurant.restaurant_id: restaurant
            for restaurant in restaurants
        }

        self.order_lookup = {
            order.order_id: order
            for order in orders
        }

        self.preference_lookup = {
            preference.customer_id: preference
            for preference in customer_preferences
        }

    # --------------------------------------------------------
    # ENTITY LOOKUPS
    # --------------------------------------------------------

    def get_customer(self, customer_id):

        customer = self.customer_lookup.get(customer_id)

        if customer is None:
            raise EntityNotFoundError(
                f"Customer {customer_id} not found."
            )

        return customer

    def get_restaurant(self, restaurant_id):

        restaurant = self.restaurant_lookup.get(restaurant_id)

        if restaurant is None:
            raise EntityNotFoundError(
                f"Restaurant {restaurant_id} not found."
            )

        return restaurant

    # --------------------------------------------------------
    # ORDER ANALYSIS
    # --------------------------------------------------------

    def get_successful_orders(self):

        return [
            order
            for order in self.orders
            if order.is_successful()
        ]

    def get_customer_orders(self, customer_id):

        return [
            order
            for order in self.orders
            if order.customer_id == customer_id
        ]

    def get_customer_spending(self, customer_id):

        try:
            self.get_customer(customer_id)
        except EntityNotFoundError:
            raise

        return sum(
            order.calculate_order_value()
            for order in self.orders
            if order.customer_id == customer_id
            and order.is_successful()
        )

    # --------------------------------------------------------
    # TOP CUSTOMERS
    # --------------------------------------------------------

    def get_top_customers(self, top_n=5):

        spending = []

        for customer in self.customers:

            amount = self.get_customer_spending(
                customer.customer_id
            )

            spending.append(
                (customer, amount)
            )

        spending.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return spending[:top_n]

    # --------------------------------------------------------
    # RESTAURANT PERFORMANCE
    # --------------------------------------------------------

    def get_restaurant_performance(self, restaurant_id):

        restaurant = self.get_restaurant(restaurant_id)

        successful_orders = [
            order
            for order in self.orders
            if order.restaurant_id == restaurant_id
            and order.is_successful()
        ]

        revenue = sum(
            order.calculate_order_value()
            for order in successful_orders
        )

        return {
            "restaurant": restaurant.restaurant_name,
            "successful_orders": len(successful_orders),
            "revenue": revenue
        }

    def get_top_restaurants(self, top_n=5):

        performance = []

        for restaurant in self.restaurants:

            revenue = sum(
                order.calculate_order_value()
                for order in self.orders
                if order.restaurant_id == restaurant.restaurant_id
                and order.is_successful()
            )

            performance.append(
                (restaurant, revenue)
            )

        performance.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return performance[:top_n]

    # --------------------------------------------------------
    # FOOD ITEM ANALYSIS
    # --------------------------------------------------------

    def get_top_food_items(self, top_n=5):

        item_revenue = defaultdict(float)

        for item in self.order_items:

            item_revenue[item.item_name] += (
                item.calculate_item_value()
            )

        results = list(item_revenue.items())

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return results[:top_n]

    # --------------------------------------------------------
    # CUSTOMER PREFERENCES
    # --------------------------------------------------------

    def get_customer_preferences(self, customer_id):

        preference = self.preference_lookup.get(customer_id)

        if preference is None:
            return []

        return preference.get_preferences()

    # --------------------------------------------------------
    # EXPLORER CUSTOMERS
    # --------------------------------------------------------

    def get_explorer_customers(self):

        explorers = set()

        for order in self.orders:

            if not order.is_successful():
                continue

            restaurant = self.restaurant_lookup.get(
                order.restaurant_id
            )

            if restaurant is None:
                continue

            preferences = self.get_customer_preferences(
                order.customer_id
            )

            if restaurant.cuisine not in preferences:
                explorers.add(order.customer_id)

        return [
            self.customer_lookup[customer_id]
            for customer_id in explorers
            if customer_id in self.customer_lookup
        ]

    # --------------------------------------------------------
    # PREFERENCE-ALIGNED CUSTOMERS
    # --------------------------------------------------------

    def get_preference_aligned_customers(self):

        aligned = set()

        for order in self.orders:

            if not order.is_successful():
                continue

            restaurant = self.restaurant_lookup.get(
                order.restaurant_id
            )

            if restaurant is None:
                continue

            preferences = self.get_customer_preferences(
                order.customer_id
            )

            if restaurant.cuisine in preferences:
                aligned.add(order.customer_id)

        return [
            self.customer_lookup[customer_id]
            for customer_id in aligned
            if customer_id in self.customer_lookup
        ]

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    def validate_data(self):

        errors = []

        for restaurant in self.restaurants:

            if restaurant.rating is not None:
                if not restaurant.is_valid_rating():
                    errors.append(
                        f"Invalid rating for restaurant "
                        f"{restaurant.restaurant_id}"
                    )

        for item in self.order_items:

            if not item.is_valid_quantity():
                errors.append(
                    f"Invalid quantity for "
                    f"{item.item_name}"
                )

        for order in self.orders:

            if order.customer_id not in self.customer_lookup:
                errors.append(
                    f"Invalid customer reference in order "
                    f"{order.order_id}"
                )

            if order.restaurant_id not in self.restaurant_lookup:
                errors.append(
                    f"Invalid restaurant reference in order "
                    f"{order.order_id}"
                )

        return errors


# ============================================================
# CONVERT RAW DATA → OBJECTS
# ============================================================

def create_objects():

    # Import raw generated data
    from data.customers import customers
    from data.restaurants import restaurants
    from data.orders import orders
    from data.order_items import order_items
    from data.customer_preferences import customer_preferences

    customer_objects = [
        Customer(
            customer["customer_id"],
            customer["customer_name"],
            customer["city"],
            customer["signup_date"],
            customer["customer_segment"]
        )
        for customer in customers
    ]

    restaurant_objects = [
        Restaurant(
            restaurant["restaurant_id"],
            restaurant["restaurant_name"],
            restaurant["city"],
            restaurant["cuisine"],
            restaurant["rating"],
            restaurant["delivery_fee"]
        )
        for restaurant in restaurants
    ]

    order_objects = [
        Order(
            order["order_id"],
            order["customer_id"],
            order["restaurant_id"],
            order["order_date"],
            order["order_status"],
            order["payment_method"],
            order["subtotal"],
            order["delivery_fee"],
            order["discount"]
        )
        for order in orders
    ]

    order_item_objects = [
        OrderItem(
            item["order_id"],
            item["item_name"],
            item["category"],
            item["quantity"],
            item["unit_price"]
        )
        for item in order_items
    ]

    preference_objects = [
        CustomerPreference(
            customer_id,
            preferences
        )
        for customer_id, preferences
        in customer_preferences.items()
    ]

    return (
        customer_objects,
        restaurant_objects,
        order_objects,
        order_item_objects,
        preference_objects
    )


# ============================================================
# DEMONSTRATION
# ============================================================

def main():

    print("\n" + "=" * 65)
    print("DAY 3 — OOPS: FOOD DELIVERY INTELLIGENCE SYSTEM")
    print("=" * 65)

    (
        customer_objects,
        restaurant_objects,
        order_objects,
        order_item_objects,
        preference_objects
    ) = create_objects()

    analytics = FoodDeliveryAnalytics(
        customer_objects,
        restaurant_objects,
        order_objects,
        order_item_objects,
        preference_objects
    )

    # --------------------------------------------------------
    # 1. OBJECTS
    # --------------------------------------------------------

    print("\nOBJECT CREATION")
    print("-" * 65)

    print(
        f"Customers created: {len(customer_objects)}"
    )

    print(
        f"Restaurants created: {len(restaurant_objects)}"
    )

    print(
        f"Orders created: {len(order_objects)}"
    )

    print(
        f"Order Items created: {len(order_item_objects)}"
    )

    print(
        f"Preferences created: {len(preference_objects)}"
    )

    # --------------------------------------------------------
    # 2. INSTANCE METHODS
    # --------------------------------------------------------

    print("\nINSTANCE METHODS")
    print("-" * 65)

    first_order = order_objects[0]

    print(
        f"{first_order} value: "
        f"{first_order.calculate_order_value():.2f}"
    )

    print(
        f"Successful: "
        f"{first_order.is_successful()}"
    )

    first_item = order_item_objects[0]

    print(
        f"{first_item} value: "
        f"{first_item.calculate_item_value():.2f}"
    )

    # --------------------------------------------------------
    # 3. TOP CUSTOMERS
    # --------------------------------------------------------

    print("\nTOP CUSTOMERS")
    print("-" * 65)

    for customer, spending in analytics.get_top_customers(5):

        print(
            f"{customer.customer_name} -> "
            f"{spending:.2f}"
        )

    # --------------------------------------------------------
    # 4. TOP RESTAURANTS
    # --------------------------------------------------------

    print("\nTOP RESTAURANTS")
    print("-" * 65)

    for restaurant, revenue in analytics.get_top_restaurants(5):

        print(
            f"{restaurant.restaurant_name} -> "
            f"{revenue:.2f}"
        )

    # --------------------------------------------------------
    # 5. TOP FOOD ITEMS
    # --------------------------------------------------------

    print("\nTOP FOOD ITEMS")
    print("-" * 65)

    for item, revenue in analytics.get_top_food_items(5):

        print(
            f"{item} -> "
            f"{revenue:.2f}"
        )

    # --------------------------------------------------------
    # 6. CUSTOMER SPENDING
    # --------------------------------------------------------

    print("\nCUSTOMER SPENDING")
    print("-" * 65)

    customer_id = customer_objects[0].customer_id

    print(
        f"{customer_objects[0].customer_name}: "
        f"{analytics.get_customer_spending(customer_id):.2f}"
    )

    # --------------------------------------------------------
    # 7. RESTAURANT PERFORMANCE
    # --------------------------------------------------------

    print("\nRESTAURANT PERFORMANCE")
    print("-" * 65)

    restaurant_id = restaurant_objects[0].restaurant_id

    performance = analytics.get_restaurant_performance(
        restaurant_id
    )

    print(
        f"Restaurant: {performance['restaurant']}"
    )

    print(
        f"Successful Orders: "
        f"{performance['successful_orders']}"
    )

    print(
        f"Revenue: "
        f"{performance['revenue']:.2f}"
    )

    # --------------------------------------------------------
    # 8. CUSTOMER PREFERENCES
    # --------------------------------------------------------

    print("\nCUSTOMER PREFERENCES")
    print("-" * 65)

    print(
        f"{customer_objects[0].customer_name}: "
        f"{analytics.get_customer_preferences(customer_id)}"
    )

    # --------------------------------------------------------
    # 9. EXPLORERS
    # --------------------------------------------------------

    print("\nEXPLORER CUSTOMERS")
    print("-" * 65)

    explorers = analytics.get_explorer_customers()

    print(
        f"Explorer customers: {len(explorers)}"
    )

    for customer in explorers[:10]:
        print(customer.customer_name)

    # --------------------------------------------------------
    # 10. PREFERENCE-ALIGNED
    # --------------------------------------------------------

    print("\nPREFERENCE-ALIGNED CUSTOMERS")
    print("-" * 65)

    aligned = analytics.get_preference_aligned_customers()

    print(
        f"Preference-aligned customers: {len(aligned)}"
    )

    for customer in aligned[:10]:
        print(customer.customer_name)

    # --------------------------------------------------------
    # 11. INHERITANCE + POLYMORPHISM
    # --------------------------------------------------------

    print("\nINHERITANCE + POLYMORPHISM")
    print("-" * 65)

    analyzers = [
        SuccessfulOrderAnalyzer(),
        CancelledOrderAnalyzer()
    ]

    sample_order = order_objects[0]

    for analyzer in analyzers:

        print(
            f"{analyzer.__class__.__name__}: "
            f"{analyzer.calculate_value(sample_order):.2f}"
        )

    # --------------------------------------------------------
    # 12. VALIDATION
    # --------------------------------------------------------

    print("\nVALIDATION")
    print("-" * 65)

    errors = analytics.validate_data()

    print(
        f"Validation issues found: {len(errors)}"
    )

    for error in errors[:10]:
        print(error)

    # --------------------------------------------------------
    # 13. EXCEPTION HANDLING
    # --------------------------------------------------------

    print("\nEXCEPTION HANDLING")
    print("-" * 65)

    try:

        analytics.get_customer(999999)

    except EntityNotFoundError as error:

        print(
            f"Handled exception: {error}"
        )

    try:

        analytics.get_restaurant(999999)

    except EntityNotFoundError as error:

        print(
            f"Handled exception: {error}"
        )

    print("\n" + "=" * 65)
    print("DAY 3 OOPS COMPLETED")
    print("=" * 65)


if __name__ == "__main__":
    main()