import tkinter as tk
from tkinter import messagebox
import backend


TEST_STALL_ID = 1  # Temporary until real stall selection is connected.


class CarnivalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Carnival POS System")
        self.geometry("1000x700")
        self.frames = {}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        for F in (StallSelectionScreen, StallPOSScreen):
            page_name = F.__name__
            frame = F(container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StallSelectionScreen")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()


class StallSelectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(
            self,
            text="Select a stall",
            font=("Arial", 24)
        )
        label.pack(pady=20)

        test_button = tk.Button(
            self,
            text="Go to Stall POS (Test)",
            font=("Arial", 14),
            command=lambda: controller.show_frame("StallPOSScreen")
        )
        test_button.pack(pady=10)


class StallPOSScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header_frame = tk.Frame(self)
        header_frame.pack(fill="x", pady=10)

        back_btn = tk.Button(
            header_frame,
            text="< Back to Stalls",
            font=("Arial", 12),
            command=lambda: controller.show_frame("StallSelectionScreen")
        )
        back_btn.pack(side="left", padx=15)

        title_label = tk.Label(
            header_frame,
            text="Stall POS System",
            font=("Arial", 20, "bold")
        )
        title_label.pack(side="left", padx=20)

        main_layout = tk.Frame(self)
        main_layout.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # Menu side -------------------------------------------------

        menu_frame = tk.LabelFrame(
            main_layout,
            text="Menu Items",
            font=("Arial", 14, "bold"),
            padx=10,
            pady=10
        )
        menu_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        items = backend.get_items(TEST_STALL_ID)

        for item in items:
            item_id = item[0]
            item_name = item[2]
            price = item[3]

            item_btn = tk.Button(
                menu_frame,
                text=item_name + " - KWD " + str(price),
                font=("Arial", 12),
                command=lambda id=item_id: self.add_item_click(id)
            )
            item_btn.pack(fill="x", pady=5)

        # Order side -------------------------------------------------

        order_frame = tk.LabelFrame(
            main_layout,
            text="Current Order",
            font=("Arial", 14, "bold"),
            padx=10,
            pady=10
        )
        order_frame.pack(
            side="right",
            fill="both"
        )

        self.order_items_frame = tk.Frame(order_frame)
        self.order_items_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        self.total_label = tk.Label(
            order_frame,
            text="Total: KWD 0.000",
            font=("Arial", 16, "bold"),
            fg="green"
        )
        self.total_label.pack(pady=10)

        btn_frame = tk.Frame(order_frame)
        btn_frame.pack(fill="x", pady=10)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            font=("Arial", 12),
            bg="red",
            fg="white",
            height=2,
            command=self.cancel_order_click
        )
        cancel_btn.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        checkout_btn = tk.Button(
            btn_frame,
            text="Complete Order",
            font=("Arial", 12),
            bg="green",
            fg="white",
            height=2
        )
        checkout_btn.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

    def add_item_click(self, item_id):
        backend.add_to_order(item_id)
        self.refresh_order_display()

    def remove_item_click(self, item_id):
        backend.remove_from_order(item_id)
        self.refresh_order_display()

    def cancel_order_click(self):
        backend.clear_order()
        self.refresh_order_display()

    def refresh_order_display(self):
        for widget in self.order_items_frame.winfo_children():
            widget.destroy()

        for item_id in backend.cart:
            item = backend.get_item(item_id)
            quantity = backend.cart[item_id]

            item_name = item[2]
            price = item[3]
            subtotal = price * quantity

            row = tk.Frame(self.order_items_frame)
            row.pack(fill="x", pady=4)

            name_label = tk.Label(
                row,
                text=item_name,
                font=("Arial", 11),
                anchor="w"
            )
            name_label.pack(
                side="left",
                fill="x",
                expand=True
            )

            minus_btn = tk.Button(
                row,
                text="-",
                width=3,
                command=lambda id=item_id: self.remove_item_click(id)
            )
            minus_btn.pack(side="left", padx=2)

            qty_label = tk.Label(
                row,
                text=str(quantity),
                font=("Arial", 11),
                width=3
            )
            qty_label.pack(side="left")

            plus_btn = tk.Button(
                row,
                text="+",
                width=3,
                command=lambda id=item_id: self.add_item_click(id)
            )
            plus_btn.pack(side="left", padx=2)

            subtotal_label = tk.Label(
                row,
                text=f"KWD {subtotal:.3f}",
                font=("Arial", 11),
                width=10
            )
            subtotal_label.pack(side="right")

        total = backend.calculate_total()

        self.total_label.config(
            text=f"Total: KWD {total:.3f}"
        )


if __name__ == "__main__":
    app = CarnivalApp()
    app.mainloop()