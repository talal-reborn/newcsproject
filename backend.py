import sqlite3
import tkinter as tk

#connecting db ---------------------------------------------

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

setup_database() #main query call for database creation. runs on every startup regardless.

#structures ----------------------------------------------

cart = {} #a dictionary for the cart, storing item_id as key, and the quantity variable as value in the pair

#major functions ---------------------------------------------

def add_item(name, price, description, imagepath): #item adding into the main screen
    cur.execute('''INSERT INTO items (
    item_name,
    price,
    description,
    image_path) 
    VALUES(?,?,?,?)''', (name, price, description, imagepath))
    
    con.commit()


def add_to_order(item_id): #adds item to cart on basis of quantity, into cart
    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1
    
    print(cart)

def get_items(): #get all items
    cur.execute('SELECT * FROM items')
    items = cur.fetchall()
    return items


#tkinter GUI ---------------------------------------------

root = tk.Tk()
root.title('CARNIVAL POS')

items = get_items() #a collection of all items available

for item in items: #loops through each item, assigning it a button, so that on click, it adds to the cart and tracks quantity
    item_id = item[0]
    item_name = item[1]
    price = item[2]

    button_text = item_name + ' - ' + str(price) + ' KD'
    item_button = tk.Button(
        root,
        text=button_text,
        command=lambda id=item_id: add_to_order(id)
    )
    item_button.pack()

root.mainloop()