import json
import sqlite3

# Connect to the database
conn = sqlite3.connect('tubes.db')
c = conn.cursor()

# Drop tables if they exist
c.execute('DROP TABLE IF EXISTS users')
c.execute('DROP TABLE IF EXISTS food_delivery')
c.execute('DROP TABLE IF EXISTS laundry')
c.execute('DROP TABLE IF EXISTS cleaning')
c.execute('DROP TABLE IF EXISTS daily_needs')
c.execute('DROP TABLE IF EXISTS daily_needs_products')
c.execute('DROP TABLE IF EXISTS restaurants')
c.execute('DROP TABLE IF EXISTS menus')
c.execute('DROP TABLE IF EXISTS order_laundry')

# Create tables
c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    role TEXT,
    password TEXT
)
''')

c.execute('''
CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
''')

c.execute('''
CREATE TABLE laundry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_customer INTEGER,
    nama TEXT,
    alamat TEXT,
    jenis TEXT,
    berat INTEGER,
    service TEXT
)
''')

c.execute('''
CREATE TABLE cleaning (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id,
    nama TEXT,
    alamat TEXT,
    tanggal DATETIME,
    FOREIGN KEY (customer_id) REFERENCES users(id)
)
''')

c.execute('''
CREATE TABLE menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    name TEXT,
    harga INTEGER,
    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
)
''')

c.execute('''
CREATE TABLE food_delivery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    customer_id INTEGER,
    alamat TEXT,
    price INTEGER,
    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
)
''')

c.execute('''
CREATE TABLE foods (
    id_food_delivery INTEGER,
    food_name TEXT,
    quantity INTEGER,
    FOREIGN KEY(id_food_delivery) REFERENCES food_delivery(id)
)
''')

# Define the correct daily_needs table
c.execute('''
CREATE TABLE daily_needs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER,
  alamat TEXT,
  tanggal DATETIME,
  status TEXT DEFAULT 'pending',                
  FOREIGN KEY(customer_id) REFERENCES users(id)
)
''')

c.execute('''
CREATE TABLE daily_needs_order (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER,
  product TEXT,
  quantity INTEGER,
  total TEXT,
  status TEXT DEFAULT 'pending',                
  FOREIGN KEY(order_id) REFERENCES daily_needs(id)
)
''')

c.execute('''
CREATE TABLE daily_needs_products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_name TEXT,
  price INTEGER
)
''')

c.execute("""
CREATE TABLE IF NOT EXISTS pickups (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    destination TEXT,
    pickup_datetime TEXT,
    num_passengers INTEGER,
    FOREIGN KEY (customer_id) REFERENCES users(id)
)
""")

# Insert data into users table
c.execute("INSERT INTO users (username, role, password) VALUES (?,?,?)", 
          ('user1', 'user', '12345'))
c.execute("INSERT INTO users (username, role, password) VALUES (?,?,?)", 
          ('admin', 'admin', 'admin'))

# Insert restaurant and menu items
c.execute("INSERT INTO restaurants(name) VALUES ('Ayam Arjana')")
c.execute("INSERT INTO menus(restaurant_id, name, harga) VALUES (?,?,?)", (1, 'Ayam Geprek', 15000))
c.execute("INSERT INTO menus(restaurant_id, name, harga) VALUES (?,?,?)", (1, 'Ayam Sambel Rica', 18000))

#insert daily_needs
c.execute("INSERT INTO daily_needs_products (product_name, price) VALUES ('Sabun Mandi', 15000)")
c.execute("INSERT INTO daily_needs_products (product_name, price) VALUES ('Minyak Goreng', 20000)")
c.execute("INSERT INTO daily_needs_products (product_name, price) VALUES ('Gula Pasir', 5000)")
c.execute("INSERT INTO daily_needs_products (product_name, price) VALUES ('Teh Celup', 10000)")
c.execute("INSERT INTO daily_needs_products (product_name, price) VALUES ('Susu Bubuk', 30000)")

# Commit changes and close the connection
conn.commit()
conn.close()