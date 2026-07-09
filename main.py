import tkinter as tk
import backend

# tkinter GUI ---------------------------------------------

root = tk.Tk()
root.title("CARNIVAL POS")


# load every item currently stored in the database
items = backend.get_items()


# create one button for every item
for item in items:

    item_id = item[0]
    item_name = item[1]
    price = item[2]

    button_text = item_name + " - " + str(price) + " KD"

    item_button = tk.Button(
        root,
        text=button_text,

        # send the item's id to the backend when clicked
        command=lambda id=item_id: backend.add_to_order(id)
    )

    item_button.pack()


root.mainloop()