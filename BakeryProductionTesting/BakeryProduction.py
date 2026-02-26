"""available products, bread, croissant, cookies, pizza, bagel
sell by date
bread days - 2 (donate after 2 days)
croissant days - 2
cookies days - 5
pizza days - 2 (non donateable)
bagel days - 12


"""
import random

class Product:
    def __init__(self, product=None, quantity=0, sell_by_date=0):
        self.product = product
        self.quantity = quantity
        self.sell_by_date = sell_by_date
    
    def getProduct(self):
        return self.product
    
    def getQuantity(self):
        return self.quantity
    
    def getSellByDate(self):
        return self.sell_by_date

def main():
    print("Generating list of today's production...")
    #change for quantity (inclusive on both ends)
    lower_bound = 0
    upper_bound = 3
    #add products if needed
    AviailableProducts = ["Bread", "Croissant", "Cookies", "Pizza", "Bagel"]

    #generate random quantity for each product and create product objects
    #bread
    ranquantity = random.randint(lower_bound, upper_bound)
    Product1 = Product(AviailableProducts[0], ranquantity, 2)

    #Croissant
    ranquantity = random.randint(lower_bound, upper_bound)
    Product2 = Product(AviailableProducts[1], ranquantity, 2)

    #Cookies
    ranquantity = random.randint(lower_bound, upper_bound)
    Product3 = Product(AviailableProducts[2], ranquantity, 5)

    #Pizza
    ranquantity = random.randint(lower_bound, upper_bound)
    Product4 = Product(AviailableProducts[3], ranquantity, 2)

    #Bagel
    ranquantity = random.randint(lower_bound, upper_bound)
    Product5 = Product(AviailableProducts[4], ranquantity, 12)

    #print products
    products = [Product1, Product2, Product3, Product4, Product5]

    # Find longest product name
    max_name_len = max(len(p.getProduct()) for p in products)
    # Add padding
    name_width = max_name_len + 2

    print(f"{'Name':<{name_width}} {'Quantity':<10} {'Sell by date'}")

    for product in products:
        print(f"{product.getProduct():<{name_width}} {product.getQuantity():<10} {product.getSellByDate()} days")


if __name__ == "__main__":
    main()