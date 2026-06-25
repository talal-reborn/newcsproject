import sqlite3
import tkinter as tk

#connecting db ---------------------------------------------

con=sqlite3.connect('carnival_pos.db')
cur=con.cursor()

def setup_database():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS food_items (
            food_id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image_path TEXT
        )
    """)

    con.commit()

setup_database() #main query call for database creation. runs on every startup regardless.

#structures ----------------------------------------------

cart = {} #a dictionary for the cart, storing food_id as key, and the quantity variable as value in the pair

#major functions ---------------------------------------------

def add_food_item(name, price, description, imagepath): #food adding into the main screen
    cur.execute('''INSERT INTO food_items (
    food_name,
    price,
    description,
    image_path) 
    VALUES(?,?,?,?)''',(name,price,description,imagepath))
    
    con.commit()


def add_to_cart(food_id): #adds item to cart on basis of quantity, into cart
    if food_id in cart: 
        cart[food_id]+=1
    else:
        cart[food_id]=1
    
    print(cart)

def get_food_items(): #get all items of food
    cur.execute('SELECT * FROM food_items')
    foods = cur.fetchall()
    return foods


#tkinter GUI ---------------------------------------------

root = tk.Tk()
root.title('CARNIVAL POS')

foods = get_food_items() #a colloection of all food available

for food in foods: #loops thru each food, assigning them a button, so that on click, adds to cart and tracks quantity
    food_id = food[0]
    food_name = food[1]
    price = food[2]

    button_text = food_name + '-' + str(price) + 'KD'
    food_button = tk.Button(
        root,
        text=button_text,
        command=lambda id=food_id: add_to_cart(id)
    )
    food_button.pack()

root.mainloop()

