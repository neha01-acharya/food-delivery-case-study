import os
import random
import pprint
from datetime import datetime, timedelta


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = "data"

CITIES = [
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Mumbai",
    "Delhi"
]

CUISINES = [
    "Indian",
    "Chinese",
    "Italian",
    "Mexican",
    "Thai",
    "South Indian",
    "North Indian",
    "Fast Food",
    "Desserts",
    "Biryani"
]

SEGMENTS = [
    "Premium",
    "Regular",
    "New"
]

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Wallet",
    "Cash"
]

STATUSES = (
    ["Delivered"] * 80
    + ["Cancelled"] * 15
    + ["Failed"] * 5
)

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun",
    "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
    "Diya", "Sanya", "Kavya", "Neha", "Priya",
    "Ananya", "Riya", "Aadya", "Anika", "Vanya"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Reddy", "Singh",
    "Kumar", "Rao", "Das", "Gupta", "Nair"
]

RESTAURANT_PREFIXES = [
    "Spice", "Royal", "Urban", "The Grand", "Golden",
    "Tandoori", "Nawabi", "Street", "Sizzle"
]

RESTAURANT_SUFFIXES = [
    "Route", "Bites", "Bowl", "Kitchen", "Diner",
    "Palace", "Treats", "Fusion", "Express"
]

FOOD_ITEMS = {
    "Main Course": [
        "Paneer Butter Masala",
        "Chicken Biryani",
        "Margherita Pizza",
        "Pad Thai",
        "Masala Dosa",
        "Hakka Noodles"
    ],
    "Starter": [
        "Chilli Paneer",
        "Spring Rolls",
        "Garlic Bread",
        "Nachos",
        "Chicken Tikka"
    ],
    "Dessert": [
        "Gulab Jamun",
        "Brownie",
        "Ice Cream",
        "Tiramisu",
        "Cheesecake"
    ],
    "Beverage": [
        "Cold Coffee",
        "Masala Chai",
        "Mojito",
        "Coke",
        "Lassi"
    ]
}


# ============================================================
# CREATE DATA DIRECTORY
# ============================================================

os.makedirs(DATA_DIR, exist_ok=True)


# ============================================================
# GENERATE CUSTOMERS
# ============================================================

customers = []

start_date = datetime(2024, 1, 1)

for i in range(100):

    customers.append({
        "customer_id": 1001 + i,
        "customer_name": (
            f"{random.choice(FIRST_NAMES)} "
            f"{random.choice(LAST_NAMES)}"
        ),
        "city": random.choice(CITIES),
        "signup_date": (
            start_date
            + timedelta(days=random.randint(0, 700))
        ).strftime("%Y-%m-%d"),
        "customer_segment": random.choice(SEGMENTS)
    })


# Customer edge cases

customers.append(customers[10].copy())
customers.append(customers[25].copy())

customers[42]["customer_segment"] = None
customers[67]["customer_segment"] = None

customers[88]["city"] = "Atlantis"


# ============================================================
# GENERATE RESTAURANTS
# ============================================================

restaurants = []

for i in range(30):

    restaurants.append({
        "restaurant_id": 501 + i,
        "restaurant_name": (
            f"{random.choice(RESTAURANT_PREFIXES)} "
            f"{random.choice(RESTAURANT_SUFFIXES)}"
        ),
        "city": CITIES[i % len(CITIES)],
        "cuisine": random.choice(CUISINES),
        "rating": round(
            random.uniform(3.0, 5.0),
            1
        ),
        "delivery_fee": random.choice([
            20.0,
            35.0,
            50.0,
            0.0
        ])
    })


# Restaurant edge cases

restaurants.append(restaurants[5].copy())

restaurants[12]["rating"] = None
restaurants[21]["rating"] = 9.5


# ============================================================
# GENERATE ORDERS + ORDER ITEMS
# ============================================================

orders = []
order_items = []

order_item_id_counter = 1

valid_customer_ids = [
    customer["customer_id"]
    for customer in customers[:100]
]

valid_restaurant_ids = [
    restaurant["restaurant_id"]
    for restaurant in restaurants[:30]
]


for i in range(500):

    order_id = 10001 + i

    num_items = random.choices(
        [1, 2, 3, 4, 5],
        weights=[20, 45, 25, 5, 5]
    )[0]

    subtotal = 0.0

    for _ in range(num_items):

        category = random.choice(
            list(FOOD_ITEMS.keys())
        )

        item_name = random.choice(
            FOOD_ITEMS[category]
        )

        quantity = random.randint(1, 3)

        unit_price = float(
            random.randint(100, 400)
        )

        order_items.append({
            "order_item_id": order_item_id_counter,
            "order_id": order_id,
            "item_name": item_name,
            "category": category,
            "quantity": quantity,
            "unit_price": unit_price
        })

        subtotal += quantity * unit_price

        order_item_id_counter += 1


    delivery_fee = random.choice([
        20.0,
        35.0,
        50.0,
        0.0
    ])

    discount = float(
        random.choice([
            0,
            0,
            0,
            50,
            100,
            150
        ])
    )

    orders.append({
        "order_id": order_id,
        "customer_id": random.choice(valid_customer_ids),
        "restaurant_id": random.choice(valid_restaurant_ids),
        "order_date": (
            datetime(2025, 1, 1)
            + timedelta(days=random.randint(0, 500))
        ).strftime("%Y-%m-%d"),
        "order_status": random.choice(STATUSES),
        "payment_method": random.choice(PAYMENT_METHODS),
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "discount": discount
    })


# ============================================================
# ORDER EDGE CASES
# ============================================================

orders.append(orders[15].copy())
orders.append(orders[115].copy())
orders.append(orders[215].copy())


for index in [30, 70, 150, 220, 310]:
    orders[index]["customer_id"] = 9999


for index in [40, 90, 180]:
    orders[index]["restaurant_id"] = 999


orders[400]["discount"] = 5000.0


# ============================================================
# ORDER ITEM EDGE CASES
# ============================================================

order_items[10]["order_id"] = 99999
order_items[50]["order_id"] = 99999

order_items.append(order_items[100].copy())
order_items.append(order_items[200].copy())

order_items[300]["quantity"] = 0
order_items[400]["quantity"] = 500


# ============================================================
# CUSTOMER PREFERENCES
# ============================================================

customer_preferences = {}

for customer_id in valid_customer_ids:

    number_of_preferences = random.randint(1, 3)

    customer_preferences[customer_id] = random.sample(
        CUISINES,
        number_of_preferences
    )


# Preference edge cases

customer_preferences[valid_customer_ids[5]] = []

customer_preferences[valid_customer_ids[15]] = []

customer_preferences[valid_customer_ids[25]].append(
    "Martian Food"
)

customer_preferences[valid_customer_ids[35]] = [
    "Indian",
    "Indian",
    "Chinese"
]


# ============================================================
# WRITE DATA TO FILES
# ============================================================

def write_file(filename, variable_name, data):

    filepath = os.path.join(
        DATA_DIR,
        filename
    )

    with open(filepath, "w") as file:

        formatted_data = pprint.pformat(
            data,
            indent=4,
            sort_dicts=False,
            width=120
        )

        file.write(
            f"{variable_name} = {formatted_data}\n"
        )


write_file(
    "customers.py",
    "customers",
    customers
)

write_file(
    "restaurants.py",
    "restaurants",
    restaurants
)

write_file(
    "orders.py",
    "orders",
    orders
)

write_file(
    "order_items.py",
    "order_items",
    order_items
)

write_file(
    "customer_preferences.py",
    "customer_preferences"
    , customer_preferences
)


# ============================================================
# SUMMARY
# ============================================================

print("\nDataset generated successfully!\n")

print(f"customers.py            : {len(customers)} records")
print(f"restaurants.py          : {len(restaurants)} records")
print(f"orders.py               : {len(orders)} records")
print(f"order_items.py          : {len(order_items)} records")
print(
    f"customer_preferences.py : "
    f"{len(customer_preferences)} records"
)

print("\nFiles created inside:", DATA_DIR)