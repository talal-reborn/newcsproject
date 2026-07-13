import sqlite3
from datetime import datetime
import hashlib


# connecting db ---------------------------------------------

con = sqlite3.connect("carnival_pos.db")
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()


def setup_database():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stalls (
            stall_id INTEGER PRIMARY KEY AUTOINCREMENT,
            stall_name TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            stall_type TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            stall_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image_path TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,

            FOREIGN KEY (stall_id)
            REFERENCES stalls(stall_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            stall_id INTEGER NOT NULL,
            total_price REAL NOT NULL,
            timestamp DATETIME NOT NULL,

            FOREIGN KEY (stall_id)
            REFERENCES stalls(stall_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,

            FOREIGN KEY (order_id)
            REFERENCES orders(order_id),

            FOREIGN KEY (item_id)
            REFERENCES items(item_id)
        )
    """)

    con.commit()


setup_database()  # Runs every startup. Creates database table if it doesn't exist.


# structures ----------------------------------------------

cart = {}  # Dictionary storing item_id as key and quantity as value. Used to create a receipt.


# stall functions ---------------------------------------------

def hash_password(password):
    # converts password into a hash before storing/comparing it

    return hashlib.sha256(password.encode()).hexdigest()


def create_stall(stall_name, password, stall_type):
    # creates a new stall/project

    password_hash = hash_password(password)

    cur.execute("""
        INSERT INTO stalls (
            stall_name,
            password_hash,
            stall_type
        )
        VALUES (?, ?, ?)
    """, (
        stall_name,
        password_hash,
        stall_type
    ))

    con.commit()

    return cur.lastrowid


def get_stalls():
    # returns all stalls to the stall selection screen

    cur.execute("""
        SELECT
            stall_id,
            stall_name,
            stall_type
        FROM stalls
        ORDER BY stall_name
    """)

    stalls = cur.fetchall()

    return stalls


def get_stall(stall_id):
    # returns one specific stall

    cur.execute("""
        SELECT
            stall_id,
            stall_name,
            stall_type
        FROM stalls
        WHERE stall_id = ?
    """, (stall_id,))

    stall = cur.fetchone()

    return stall


def verify_stall_password(stall_id, password):
    # checks whether the entered stall password is correct

    entered_hash = hash_password(password)

    cur.execute("""
        SELECT password_hash
        FROM stalls
        WHERE stall_id = ?
    """, (stall_id,))

    result = cur.fetchone()

    if result is None:
        return False

    stored_hash = result[0]

    return entered_hash == stored_hash


# item functions ---------------------------------------------

def add_item(stall_id, name, price, description, imagepath):
    # adds new item in db and assigns it to a stall

    cur.execute("""
        INSERT INTO items (
            stall_id,
            item_name,
            price,
            description,
            image_path
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        stall_id,
        name,
        price,
        description,
        imagepath
    ))

    con.commit()

    return cur.lastrowid


def get_items(stall_id):
    # returns all active items belonging to one stall to main menu

    cur.execute("""
        SELECT *
        FROM items
        WHERE stall_id = ?
        AND is_active = 1
        ORDER BY item_name
    """, (stall_id,))

    items = cur.fetchall()

    return items


def get_item(item_id):
    # returns a specific item from db to menu/receipt

    cur.execute("""
        SELECT *
        FROM items
        WHERE item_id = ?
    """, (item_id,))

    item = cur.fetchone()

    return item


def update_item(item_id, name, price, description, imagepath):
    # edits an existing item's information

    cur.execute("""
        UPDATE items
        SET item_name = ?,
            price = ?,
            description = ?,
            image_path = ?
        WHERE item_id = ?
    """, (
        name,
        price,
        description,
        imagepath,
        item_id
    ))

    con.commit()


def delete_item(item_id):
    # hides item from menu without deleting old receipt information

    cur.execute("""
        UPDATE items
        SET is_active = 0
        WHERE item_id = ?
    """, (item_id,))

    con.commit()


# order functions ---------------------------------------------

def add_to_order(item_id):
    # adds new item into the cart

    item = get_item(item_id)

    if item is None or item[6] == 0:
        return False

    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1

    print(cart)

    return True


def remove_from_order(item_id):
    # removes item currently in cart

    if item_id in cart:
        if cart[item_id] == 1:
            cart.pop(item_id)
        else:
            cart[item_id] -= 1

    print(cart)


def calculate_total():
    # calc total bill -- gets cart item, gets its price,
    # multiplies by quantity, updates running total.

    total = 0

    for item_id, quantity in cart.items():
        item = get_item(item_id)

        if item is not None:
            price = item[3]
            subtotal = price * quantity
            total += subtotal

    return round(total, 3)


def complete_order(stall_id):
    # complete the order, make a receipt id for it,
    # insert items into one and receipts into one table.

    if not cart:
        return None

    total = calculate_total()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cur.execute("""
            INSERT INTO orders (
                stall_id,
                total_price,
                timestamp
            )
            VALUES (?, ?, ?)
        """, (
            stall_id,
            total,
            timestamp
        ))

        order_id = cur.lastrowid

        for item_id, quantity in cart.items():
            item = get_item(item_id)

            if item is None:
                raise ValueError("An item in the cart no longer exists.")

            item_stall_id = item[1]
            unit_price = item[3]

            if item_stall_id != stall_id:
                raise ValueError(
                    "The cart contains an item belonging to another stall."
                )

            cur.execute("""
                INSERT INTO order_items (
                    order_id,
                    item_id,
                    quantity,
                    unit_price
                )
                VALUES (?, ?, ?, ?)
            """, (
                order_id,
                item_id,
                quantity,
                unit_price
            ))

        con.commit()
        clear_order()

        return order_id

    except Exception:
        con.rollback()
        raise


def clear_order():
    # clear order from cart/complete for fresh new

    cart.clear()
    print(cart)


# temporary testing ---------------------------------------------

"""
stall_id = create_stall(
    "Burger Station",
    "burger123",
    "food"
)

add_item(
    stall_id,
    "Burger",
    5.990,
    "Patties, buns, and amazing cheese",
    "burger.png"
)

add_item(
    stall_id,
    "Pizza",
    9.990,
    "Yummy yummy in my tummy",
    "pizza.png"
)
"""


"""
if not get_stalls():
    create_stall(
        "Burger Station",
        "burger123",
        "food"
    )

print(get_stalls())
print(verify_stall_password(1, "burger123"))
print(verify_stall_password(1, "wrong"))
"""