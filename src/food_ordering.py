import sqlite3


# ---------------- DATABASE CONNECTION ----------------

conn = sqlite3.connect("food_ordering.db")
cursor = conn.cursor()


# ---------------- CREATE TABLES ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    food_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    food_name TEXT NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    total_amount REAL,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    food_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (food_id) REFERENCES menu(food_id)
)
""")

conn.commit()


# ---------------- INSERT SAMPLE DATA ----------------

cursor.execute("SELECT COUNT(*) FROM restaurants")
restaurant_count = cursor.fetchone()[0]

if restaurant_count == 0:

    cursor.execute(
        "INSERT INTO restaurants (name) VALUES (?)",
        ("Paradise Restaurant",)
    )

    cursor.execute(
        "INSERT INTO restaurants (name) VALUES (?)",
        ("Domino's Pizza",)
    )

    cursor.execute(
        "INSERT INTO restaurants (name) VALUES (?)",
        ("Biryani House",)
    )

    conn.commit()

    cursor.execute("SELECT restaurant_id, name FROM restaurants")

    restaurants = cursor.fetchall()

    for restaurant_id, name in restaurants:

        if name == "Paradise Restaurant":
            foods = [
                ("Chicken Biryani", 250),
                ("Mutton Biryani", 350),
                ("Chicken 65", 180)
            ]

        elif name == "Domino's Pizza":
            foods = [
                ("Veg Pizza", 200),
                ("Chicken Pizza", 300),
                ("Garlic Bread", 120)
            ]

        else:
            foods = [
                ("Special Biryani", 280),
                ("Paneer Biryani", 220),
                ("Chicken Kebab", 200)
            ]

        for food_name, price in foods:
            cursor.execute("""
                INSERT INTO menu
                (restaurant_id, food_name, price)
                VALUES (?, ?, ?)
            """, (restaurant_id, food_name, price))

    conn.commit()


# ---------------- CUSTOMER REGISTRATION ----------------

def register_customer():

    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")

    try:

        cursor.execute("""
            INSERT INTO customers (name, phone)
            VALUES (?, ?)
        """, (name, phone))

        conn.commit()

        print("Registration successful!")

        return cursor.lastrowid

    except sqlite3.IntegrityError:

        print("Phone number already registered.")

        cursor.execute(
            "SELECT customer_id FROM customers WHERE phone = ?",
            (phone,)
        )

        result = cursor.fetchone()

        return result[0]


# ---------------- SHOW RESTAURANTS ----------------

def show_restaurants():

    cursor.execute("""
        SELECT restaurant_id, name
        FROM restaurants
    """)

    restaurants = cursor.fetchall()

    print("\nAvailable Restaurants:")

    for restaurant_id, name in restaurants:
        print(restaurant_id, "-", name)


# ---------------- SHOW MENU ----------------

def show_menu(restaurant_id):

    cursor.execute("""
        SELECT food_id, food_name, price
        FROM menu
        WHERE restaurant_id = ?
    """, (restaurant_id,))

    foods = cursor.fetchall()

    print("\nMenu:")

    for food_id, food_name, price in foods:
        print(
            f"{food_id} - {food_name} - Rs.{price}"
        )


# ---------------- PLACE ORDER ----------------

def place_order(customer_id):

    show_restaurants()

    restaurant_id = int(
        input("\nEnter restaurant ID: ")
    )

    # Check restaurant
    cursor.execute("""
        SELECT name
        FROM restaurants
        WHERE restaurant_id = ?
    """, (restaurant_id,))

    restaurant = cursor.fetchone()

    if restaurant is None:
        print("Invalid restaurant ID.")
        return

    show_menu(restaurant_id)

    cart = []

    while True:

        food_id = int(
            input("\nEnter food ID (0 to finish): ")
        )

        if food_id == 0:
            break

        quantity = int(
            input("Enter quantity: ")
        )

        # Check food belongs to selected restaurant
        cursor.execute("""
            SELECT food_name, price
            FROM menu
            WHERE food_id = ?
            AND restaurant_id = ?
        """, (food_id, restaurant_id))

        food = cursor.fetchone()

        if food is None:

            print("Invalid food ID.")

        else:

            food_name, price = food

            cart.append(
                (food_id, food_name, price, quantity)
            )

            print(food_name, "added to cart.")

    if not cart:

        print("Cart is empty.")
        return

    # Calculate total
    total = 0

    print("\n----- BILL -----")

    for food_id, food_name, price, quantity in cart:

        item_total = price * quantity

        total += item_total

        print(
            f"{food_name} x {quantity} = Rs.{item_total}"
        )

    print("----------------")
    print("Total Amount: Rs.", total)

    confirm = input(
        "Confirm order? (yes/no): "
    )

    if confirm.lower() != "yes":

        print("Order cancelled.")
        return

    # Insert order
    cursor.execute("""
        INSERT INTO orders
        (customer_id, total_amount, status)
        VALUES (?, ?, ?)
    """, (customer_id, total, "Placed"))

    order_id = cursor.lastrowid

    # Insert order items
    for food_id, food_name, price, quantity in cart:

        cursor.execute("""
            INSERT INTO order_items
            (order_id, food_id, quantity)
            VALUES (?, ?, ?)
        """, (order_id, food_id, quantity))

    conn.commit()

    print("\nOrder placed successfully!")
    print("Your Order ID:", order_id)


# ---------------- ORDER HISTORY ----------------

def view_orders(customer_id):

    cursor.execute("""
        SELECT order_id, total_amount, status
        FROM orders
        WHERE customer_id = ?
    """, (customer_id,))

    orders = cursor.fetchall()

    if not orders:

        print("No orders found.")
        return

    print("\n----- ORDER HISTORY -----")

    for order_id, total, status in orders:

        print(
            f"Order ID: {order_id} | "
            f"Amount: Rs.{total} | "
            f"Status: {status}"
        )


# ---------------- MAIN PROGRAM ----------------

print("================================")
print("   ONLINE FOOD ORDERING SYSTEM")
print("================================")

customer_id = register_customer()

while True:

    print("\n1. View Restaurants")
    print("2. Place Order")
    print("3. View Order History")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        show_restaurants()

    elif choice == "2":

        place_order(customer_id)

    elif choice == "3":

        view_orders(customer_id)

    elif choice == "4":

        print("Thank you for using the system!")

        break

    else:

        print("Invalid choice.")


conn.close()