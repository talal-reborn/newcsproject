import sqlite3

# connecting db ---------------------------------------------

con = sqlite3.connect('carnival_pos.db')
cur = con.cursor()

def setup_database():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image_path TEXT
        )
    """)

    con.commit()

setup_database() # Runs every startup. Creates database table if it doesn't exist.


# structures ----------------------------------------------

cart = {} # Dictionary storing item_id as key and quantity as value.


# major functions ---------------------------------------------

def add_item(name, price, description, imagepath):
    #adds new item in db

    cur.execute('''
    INSERT INTO items (
        item_name,
        price,
        description,
        image_path)
    VALUES(?,?,?,?)
    ''', (name, price, description, imagepath))

    con.commit()

def get_items():
    #returns all items in db to main menu

    cur.execute("SELECT * FROM items")
    items = cur.fetchall()

    return items


def add_to_order(item_id):
    #adds new item into the cart

    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1

    print(cart)

def remove_from_order(item_id):
    #removes item currently in cart
    if item_id in cart:
        if cart[item_id] == 1:
            cart.pop(item_id)
        else:
            cart[item_id] -= 1

    print(cart)
