import tkinter as tk
from tkinter import ttk
import json
import random

from GoogleSheetLinker import GoogleSheetLinker
from DateManager import InventoryQueue
from BakeryProduction import Product   # reuse your Product class

class BakeryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bakery Production Manager")

        self.linker = GoogleSheetLinker()

        # Load initial FIFO state
        self.load_inventory()

        # Generate today's production
        self.generate_production()

        # Build GUI layout
        self.build_layout()

        # Display initial data
        self.refresh_tables()

    def load_inventory(self):
        df = self.linker.pull()
        self.inventory = []

        for _, row in df.iterrows():
            name = row["Product"]
            shelf = row["ShelfLife"]
            queue = json.loads(row["QueueJSON"])
            self.inventory.append(InventoryQueue(name, shelf, queue))

    def generate_production(self):
        products = ["Bread", "Croissant", "Cookies", "Pizza", "Bagel"]
        shelf_lives = [2, 2, 5, 2, 12]

        self.today_products = []
        for name, shelf in zip(products, shelf_lives):
            qty = random.randint(0, 3)
            self.today_products.append(Product(name, qty, shelf))

        # Compute pull-today values
        self.pull_today = []
        for inv, prod in zip(self.inventory, self.today_products):
            # simulate FIFO without modifying queues yet
            temp_queue = inv.queue.copy()
            pulled = temp_queue.popleft() if len(temp_queue) == inv.shelf_life else 0
            self.pull_today.append(pulled)

    def build_layout(self):
        # Inventory On Hand table
        inv_label = ttk.Label(self.root, text="Inventory On Hand", font=("Arial", 14))
        inv_label.grid(row=0, column=2, padx=10, pady=5)

        self.inv_tree = ttk.Treeview(self.root, columns=("product", "total"), show="headings")
        self.inv_tree.heading("product", text="Product")
        self.inv_tree.heading("total", text="Total")
        self.inv_tree.grid(row=1, column=2, padx=10, pady=5)


        # Production table
        prod_label = ttk.Label(self.root, text="Today's Production", font=("Arial", 14))
        prod_label.grid(row=0, column=0, padx=10, pady=5)

        self.prod_tree = ttk.Treeview(self.root, columns=("product", "qty"), show="headings")
        self.prod_tree.heading("product", text="Product")
        self.prod_tree.heading("qty", text="Quantity")
        self.prod_tree.grid(row=1, column=0, padx=10, pady=5)

        # Pull table
        pull_label = ttk.Label(self.root, text="Pull Today", font=("Arial", 14))
        pull_label.grid(row=0, column=1, padx=10, pady=5)

        self.pull_tree = ttk.Treeview(self.root, columns=("product", "pull"), show="headings")
        self.pull_tree.heading("product", text="Product")
        self.pull_tree.heading("pull", text="Amount")

        self.pull_tree.grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        self.finish_btn = ttk.Button(self.root, text="Production Finished", command=self.finish_production)
        self.finish_btn.grid(row=2, column=1, sticky="e", padx=10, pady=10)

        self.next_day_btn = ttk.Button(self.root, text="Next Day", command=self.next_day)
        self.next_day_btn.grid(row=2, column=0, sticky="w", padx=10, pady=10)

    def refresh_tables(self):
    # Clear tables
        for i in self.prod_tree.get_children():
            self.prod_tree.delete(i)
        for i in self.pull_tree.get_children():
            self.pull_tree.delete(i)
        for i in self.inv_tree.get_children():
            self.inv_tree.delete(i)

        for inv in self.inventory:
            self.inv_tree.insert("", "end",
                values=(inv.name, inv.total_inventory())
            )

        # Fill production table
        for prod in self.today_products:
            self.prod_tree.insert("", "end",
                values=(prod.getProduct(), prod.getQuantity())
            )

        # Fill pull table
        for inv, pulled in zip(self.inventory, self.pull_today):
            self.pull_tree.insert("", "end",
                values=(inv.name, pulled)
            )



    def finish_production(self):
        # Update FIFO queues
        for inv, prod in zip(self.inventory, self.today_products):
            inv.add_today(prod.getQuantity())

        # Push updated queues to Sheets
        self.linker.push_fifo(self.inventory)

        # Disable button to prevent double submission
        self.finish_btn.config(state="disabled")
        self.refresh_tables()

    def next_day(self):
        # Reload inventory from Sheets
        self.load_inventory()

        # Generate new production
        self.generate_production()

        # Refresh GUI
        self.refresh_tables()

        # Re-enable finish button
        self.finish_btn.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    gui = BakeryGUI(root)
    root.mainloop()
