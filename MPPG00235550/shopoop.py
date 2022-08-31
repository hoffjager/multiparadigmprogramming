import sys
import csv
import os

class Product:
    def __init__(self, name, price = 0):
        self.name = name
        self.price = price
    
    def __repr__(self):
        return f'Product Name: {self.name} \nProduct Price: €{self.price:.2f}'

class ProductStock:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
    def name(self):
        return self.product.name
    def unit_price(self):
        return self.product.price
    def cost(self):
        return self.unit_price() * self.quantity
    def get_quantity(self):
        return self.quantity
    def set_quantity(self, saleQty):
        self.quantity -= saleQty
    def get_product(self):
        return self
    def __repr__(self):
        return f"{self.product}\nRosco's have {self.quantity:.0f} unit(s) in stock.\n"

class Customer:
    def __init__(self):
        self.shopping_list = []
        self.filename = input("Please enter a customer's file name: ")
        self.status = True
        path = "../" + str(self.filename) + ".csv"

        while self.status:
            try:
                with open(path) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter = ',')
                    first_row = next(csv_reader)
                    self.name = first_row[0]
                    self.budget = float(first_row[1])
                    for row in csv_reader:
                        name = row[0]
                        quantity = float(row[1])
                        p = Product(name)
                        ps = ProductStock(p, quantity)
                        self.shopping_list.append(ps)
                    return
            except Exception as err:
                    print("Error: Invalid customer file name detected.")
                    self.status = False
                    return

    def calculate_costs(self, price_list):
        for shop_item in price_list:
            for list_item in self.shopping_list:
                if(list_item.name() == shop_item.name()):
                    list_item.product.price = shop_item.unit_price()

    def order_cost(self):
        cost = 0
        for list_item in self.shopping_list:
            cost += list_item.cost()
        return cost

    def __repr__(self):
        print(f'Customer Name: {self.name} \nCustomer Budget: €{self.budget:.2f}')
        print("---------------------------------\n")
        for item in self.shopping_list:
            print(item.product)
            print(f"{self.name} ordered {item.quantity} of the above product(s)\n")
        print("We have the following items in stock: ")
        str = ""
        for item in self.shopping_list:
            price = item.product.price
            if price != 0:
                str += f"{item.quantity} units of {item.name()} at €{price} per unit for a total cost of €{item.cost()}\n\n"
        return str

class Live(Customer):
    def __init__(self):
        self.shopping_list = []
        self.name = input("Please enter your name: ")
        print(f"Welcome to Rosco's, {self.name}.")
        while True:
            try:
                self.budget = float(input(f"Please enter your budget: €"))
                break
            except ValueError:
                print("Error: please enter your budget as a number.")
        product = input("Please enter the name of the product you are looking to buy: ")

        while True:
            try:
                quantity = int(input(f"Please enter the quantity of {product} you are looking to buy: "))
                break
            except ValueError:
                print("Error: please enter the quantity as an integer.")
        p = Product(product)
        ps = ProductStock(p, quantity)
        self.shopping_list.append(ps)

class Shop:
    def __init__(self, path):
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)
    def __repr__(self):
        str = ""
        str += f"Rosco's have €{self.cash:.2f} cash in hand.\n"
        for item in self.stock:
            str += f"{item}\n"
        return str
    def process_order(self, c):
        print("Processing your order, please wait.")
        print("-----------------------------------")
        self.totalProductCost = 0
        for list_item in c.shopping_list:
            self.check_stock(list_item)
            self.update_cash(c)
            self.update_stock(self.product)
        print("Updating Balance\n--------------")
        print(f"{c.name} has €{c.budget:.2f} remaining.")
    def update_cash(self, c):
        self.process = False
        if c.budget >= self.totalProductCost:
            self.cash += self.totalProductCost
            c.budget -= self.totalProductCost
            if self.saleQty > 0:
                print(f"€{self.totalProductCost:.2f} has been deducted from {c.name}'s funds for {self.saleQty:.0f} unit(s) of {self.product.name()}.\n")
            self.process = True
        elif c.budget < self.totalProductCost:
            print(f"Error: insufficient funds, {c.name} only has €{c.budget:.2f}, €{self.totalProductCost:.2f} is required for {self.saleQty:.0f} unit(s) of {self.product_name}\n")
    def check_stock(self, list_item):
        for shop_item in self.stock:
            if(list_item.name() == shop_item.name()):
                self.product_name = shop_item.name()
                self.product = shop_item.get_product()
                if list_item.quantity <= shop_item.quantity:
                    self.totalProductCost = list_item.quantity *shop_item.product.price
                    self.saleQty = list_item.quantity
                    return self.totalProductCost, self.product, self.saleQty, self.product_name
                elif(list_item.quantity > shop_item.quantity):
                    print(f"Rosco's only have {shop_item.quantity} of {shop_item.name()} available at the moment. You will only ever be charged for the products sold.\n")
                    self.totalProductCost = shop_item.quantity *shop_item.product.price
                    self.saleQty = shop_item.quantity
                    return self.totalProductCost, self.product, self.saleQty, self.product_name
            if(list_item.name() != shop_item.name()):
                self.product = list_item
                self.saleQty = 0
                self.totalProductCost = 0
    def update_stock(self, product):
        if self.process == True:
            product.set_quantity(self.saleQty)
    def display_menu(self):
        while True:
            print("\n")
            print("\t\tWelcome to Rosco's, how may we help you?")
            print("\t\t-----------------------------------------")
            print("\t\t\tPress 1 for Shop Inventory")
            print("\t\t\tPress 2 for Batch Order Review")
            print("\t\t\tPress 3 for Live Order Mode")
            print("\t\t\tPress 0 to Exit")
            self.choice = input("\nPlease select an option from the main menu: ")
            if(self.choice == "1"):
                print("--------------------------------------")
                print("\t\t1: Shop Inventory")
                print("--------------------------------------")
                print(self)
                self.return_to_menu()
            elif(self.choice == "2"):
                print("-----------------------")
                print("2: Batch Order Review")
                print("-----------------------")
                c = Customer()
                if c.status == False:
                    self.return_to_menu()
                c.calculate_costs(self.stock)
                print(c)
                self.process_order(c)
                self.return_to_menu()
            elif(self.choice == "3"):
                print("------------------")
                print("3: Live Order Mode")
                print("------------------")
                c = Live()
                c.calculate_costs(self.stock)
                print(c)
                self.process_order(c)
                self.return_to_menu()
            elif(self.choice == "0"):
                print("\nThank you for shopping at Rosco's, have a nice day.")
                sys.exit()
            else:
                print("Please select an option from the main menu: ")
    def return_to_menu(self):
        menu = input("\nPress Enter to return to the main menu: ")
        if True:
            self.display_menu()

def main():
    s = Shop("../stock.csv")
    s.display_menu()

if __name__ == "__main__":
    main()