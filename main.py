import tkinter as tk
from tkinter import messagebox

class CarnivalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Carnival POS System")
        self.geometry("1000x700")
        self.frames = {}
        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)

        for F in (StallSelectionScreen, StallPOSScreen):
            page_name = F.__name__
            frame = F(container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame("StallSelectionScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StallSelectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text = "Select a stall", font = ("Arial", 24))
        label.pack(pady=20)

        # Temporary button to navigate to Stall POS
        test_button = tk.Button(self, text="Go to Stall POS (Test)", font=("Arial", 14),
                                command=lambda: controller.show_frame("StallPOSScreen"))
        test_button.pack(pady=10)

class StallPOSScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header_frame = tk.Frame(self)
        header_frame.pack(fill = "x", pady=10)

        back_btn = tk.Button(header_frame, text = "< Back to Stalls", font = ("Arial",12), command = lambda: controller.show_frame("StallSelectionScreen"))
        back_btn.pack(side="left", padx=15)
        title_label = tk.Label(header_frame, text = "Stall POS System", font = ("Arial",20, "bold"))
        title_label.pack(side = "left", padx = 20)

        main_layout = tk.Frame(self)
        main_layout.pack(fill = "both", expand = True, padx = 15, pady = 10)

        #Menu
        menu_frame = tk.LabelFrame(main_layout, text = "Menu Items", font = ("Arial", 14, "bold"), padx = 10, pady = 10)
        menu_frame.pack(side = "left", fill = "both", expand = True, padx = (0, 10))

        #Placeholder - supposed to be search/filters and food item buttons

        label_menu = tk.Label(menu_frame, text = "Food list will be here", font = ("Arial", 12))
        label_menu.pack(pady = 50)

        #Right side - Order Summary
        order_frame = tk.LabelFrame(main_layout, text = "Current Order", font = ("Arial", 14, 'bold'), padx = 10, pady = 10)
        order_frame.pack(side = "right", fill = "both")

        #Listbox to show items in cart
        self.cart_listbox = tk.Listbox(order_frame, font = ("Arial", 12), width = 35)
        self.cart_listbox.pack(fill = "both", expand = True, pady = 10)

        #Total price
        self.total_label = tk.Label(order_frame, text = "Total: KWD 0.00", font = ("Arial", 16, "bold"), fg = "green")
        self.total_label.pack(pady = 10)

        #Action Buttons
        btn_frame = tk.Frame(order_frame)
        btn_frame.pack(fill = "x", pady = 10)
        
        cancel_btn = tk.Button(btn_frame, text = "Cancel", font = ("Arial", 12), bg = "red", fg = "white", height = 2)
        cancel_btn.pack(side = "left", fill = "x", expand = True, padx = (0, 5))

        checkout_btn = tk.Button(btn_frame, text = "Complete Order", font = ("Arial", 12), bg = "green", fg = "white", height = 2)
        checkout_btn.pack(side = "right", fill = "x", expand = True, padx = (5, 0))

if __name__ == "__main__":
    app = CarnivalApp()
    app.mainloop()
        