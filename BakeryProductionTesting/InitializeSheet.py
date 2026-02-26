from GoogleSheetLinker import GoogleSheetLinker
import json
"""
This script initializes the Google Sheet with empty FIFO queues for each product.
just needs to be run when the sheet if first created, or more items are added.
"""
def main():
    linker = GoogleSheetLinker()

    products = ["Bread", "Croissant", "Cookies", "Pizza", "Bagel"]
    shelf_lives = [2, 2, 5, 2, 12]

    values = [["Product", "ShelfLife", "QueueJSON", "PullToday"]]

    for name, shelf in zip(products, shelf_lives):
        empty_queue = [0] * shelf
        values.append([
            name,
            shelf,
            json.dumps(empty_queue),
            0
        ])

    linker.ws.update("A1", values)
    print("Sheet initialized.")

if __name__ == "__main__":
    main()
