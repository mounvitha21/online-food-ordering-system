# 🍔 Online Food Ordering System

A console-based Online Food Ordering System developed using **Python and SQLite**.

The application allows customers to register, browse restaurants and menus, place food orders, and view their order history. SQLite is used to store customer, restaurant, menu, order, and order-item information.

## 🚀 Features

- Customer registration
- Restaurant listing
- Restaurant-specific food menus
- Add multiple food items to cart
- Quantity selection
- Automatic bill calculation
- Order confirmation
- Order history
- SQLite database storage
- Relational database design using primary and foreign keys

## 🛠️ Technologies Used

- Python
- SQLite
- SQL
- `sqlite3` Python library

## 🗄️ Database Design

The project uses five tables:

- `customers` – stores customer information
- `restaurants` – stores restaurant information
- `menu` – stores food items and prices
- `orders` – stores customer orders
- `order_items` – stores individual items belonging to an order

### Relationships

```text
Customers
    │
    │ 1
    │
    └──────< Orders
                │
                │ 1
                │
                └──────< Order_Items >────── Menu
                                              │
                                              │
                                              └──── Restaurants
```

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Open the project

```bash
cd online-food-ordering-system
```

### 3. Run the application

```bash
python src/food_ordering.py
```

The SQLite database `food_ordering.db` will be created automatically when the application runs.

## 📋 Main Operations

1. Register customer
2. View restaurants
3. Select restaurant
4. Browse menu
5. Add food items and quantities
6. Calculate total bill
7. Confirm order
8. View previous orders

## 🎯 Project Objective

The objective of this project is to demonstrate the implementation of a basic food ordering workflow using Python and a relational SQLite database.

## 👨‍💻 Author

**Souri Krishna**

B.Tech – Computer Science and Business Systems  
VIT-AP University