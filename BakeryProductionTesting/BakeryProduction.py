import random
import json
from DateManager import InventoryQueue
from GoogleSheetLinker import GoogleSheetLinker

class Product:
    def __init__(self, product=None, quantity=0, shelfLife=0):
        self.product = product
        self.quantity = quantity
        self.shelfLife = shelfLife
    
    def getProduct(self):
        return self.product
    
    def getQuantity(self):
        return self.quantity
    
    def getShelfLife(self):
        return self.shelfLife

def main():
    linker = GoogleSheetLinker()

    # Step 1: Pull yesterday's FIFO queues
    df = linker.pull()

    # Step 2: Build FIFO inventory objects
    inventory = []
    for _, row in df.iterrows():
        name = row["Product"]
        shelf = row["ShelfLife"]
        queue = json.loads(row["QueueJSON"])
        inventory.append(InventoryQueue(name, shelf, queue))

    # Step 3: Generate today's production
    AvailableProducts = ["Bread", "Croissant", "Cookies", "Pizza", "Bagel"]
    ShelfLives = [2, 2, 5, 2, 12]

    products = []
    for name, shelf in zip(AvailableProducts, ShelfLives):
        qty = random.randint(0, 3)
        products.append(Product(name, qty, shelf))

    # Step 4: Update FIFO queues with today's production
    for inv, product in zip(inventory, products):
        inv.add_today(product.getQuantity())

    # Step 5: Push updated FIFO queues back to Sheets
    linker.push_fifo(inventory)

if __name__ == "__main__":
    main()
