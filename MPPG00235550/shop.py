from dataclasses import dataclass, field
from typing import List
import csv
import time
import itertools

# Data Structures
# @dataclass in Python is the equivalent to a struct in C
# The data includes products, products' stock, the shop and its customers.

# Products, including their names and prices.
@dataclass
class Product:
    name: str
    price: float = 0.00

# Product Stock, including referencing Product struct info, holding the quantity of each product.
@dataclass
class ProductStock:
    product: Product
    quantity: int

# Shop, which holds the cash, also referencing Product Stock info.
@dataclass
class Shop:
    cash: float = 0.00
    stock: List[ProductStock] = field(default_factory = list)

# Customer, including their names, budgets and shopping lists.
@dataclass
class Customer:
    name: str = ""
    budget: float = 0.00
    shopping_list: List[ProductStock] = field(default_factory = list)

# this function is used to create and stock up the shop via the stock.csv file.
def create_and_stock_shop():
    s = Shop()
    with open('../stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
    return s

# this function requests a customer's name to examine the order they placed.
def read_Customer():
    path = input("Please enter a customer's file name: ")
    path = "../" + str(path) + ".csv"   # customer's name is concatenated with csv extension.
    try:
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            first_row = next(csv_reader)
            c = Customer(first_row[0], float(first_row[1]))
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])
                p = Product(name)
                ps = ProductStock(p, quantity)
                c.shopping_list.append(ps)
            return c
    except Exception as err:
        print("Error: invalid customer file name detected.")
        return_to_menu()

# this function prints the shop's products, their names and prices passed in as arguments.
def print_product(p):
    print(f'\nProduct Name: {p.name} \nProduct Price: €{p.price:.2f}')

# this function displays the cash in hand at the shop and the level of stock of products.
def print_shop(s):
    print(f"Rosco's have €{s.cash:.2f} cash in hand.")
    for item in s.stock:
        print_product(item.product)
        print(f"Rosco's have {item.quantity:.0f} unit(s) in stock.")
        print('--------------------------------------')

# this function returns the user to the main menu.
def return_to_menu():
    menu = input("\nPress Enter to return to the main menu: ")
    if True:
        display_menu()

# this function displays the main menu with options available to check stock or examine orders.
def display_menu():
    print("\n")
    print("\t\tWelcome to Rosco's. How may we help you?")
    print("\t\t----------------------------------------")
    print("\t\t\tPress 1 for Shop Inventory")
    print("\t\t\tPress 2 for Batch Order Review")
    print("\t\t\tPress 3 for Live Order Mode")
    print("\t\t\tPress 0 to Exit")

# this function processes the live orders made by the user.
def process_order(c, s):
    print("-----------------------------------")
    print("Processing your order, please wait.")
    print("-----------------------------------")
    totalProductCost = 0
    for item in c.shopping_list:
        for prod in s.stock:
            if item.product.name == prod.product.name:
                if prod.quantity >= item.quantity:
                    totalProductCost = item.quantity * prod.product.price
                    if c.budget >= totalProductCost:
                        s.cash += totalProductCost
                        c.budget -= totalProductCost
                        print(f"€{totalProductCost:.2f} has been deducted from {c.name}'s funds for {item.quantity:.0f} unit(s) of {item.product.name}.\n")
                        prod.quantity -= item.quantity
                    elif c.budget < totalProductCost:
                        print(f"Error: insufficient funds, {c.name} has €{c.budget:.2f}, €{totalProductCost:.2f} is required to purchase {item.product.name}\n")
                        c.budget -= 0
    print(f"Updating Balance\n-----------------------------\n{c.name} now has €{c.budget:.2f} remaining.")

# this function prints the customer's name, their budget and placed order.
def print_customer(c, s):
    print(f'Customer Name: {c.name} \nCustomer Budget: €{c.budget:.2f}\n')
    print("Customer Order:\n")
    print("-----------------")
    orderCost = []
    for item in c.shopping_list:
        print_product(item.product)
        print(f"{c.name} ordered {item.quantity:.0f} unit(s) of {item.product.name}\n")
        print("---------------------------------------------")
    print("Please wait while we check our available stock...\n")
    print("-------------------------------------------------")
    print("Rosco's have the following items in stock:\n")
    for item in c.shopping_list:
        for prod in s.stock:
            if item.product.name == prod.product.name:
                cost = item.quantity * prod.product.price
                orderCost.append(cost)
                print(f"{item.quantity:.0f} unit(s) of {item.product.name} at €{prod.product.price:.2f} per unit, for a total cost of €{item.quantity *prod.product.price}.\n")

# this function details the live order steps.
def live_order(s):
    shopping_list = []
    c = Customer()
    c.name = input("Please enter your name: ")
    print("------------------------------")
    print(f"Welcome to Rosco's, {c.name}.")
    print("------------------------------")
    while True:
        try:
            c.budget = float(input("Please enter your budget: €"))
            break
        except ValueError:
            print("Error: please enter your budget as a number.")
    print("-----------------------------------------------------------------------")
    product = input("Please enter the name of the product you are looking to buy: ")
    p = Product(product)
    while True:
        try:
            print("-------------------------------------------------------------------------------")
            quantity = int(input(f"Please enter the quantity of {product} you are looking to buy: "))
            break
        except ValueError:
            print("Error: please enter the quantity as an integer.")
    ps = ProductStock(p, quantity)
    print("-----------------------------------------------------------------------")
    c.shopping_list.append(ps)
    return c

def main():
    s = create_and_stock_shop()
    while True:
        display_menu()
        choice = input("\nPlease select an option from the main menu: ")
        if(choice == "1"):
            print("-----------------")
            print("1: Shop Inventory")
            print("-----------------")
            print_shop(s)
            return_to_menu()
        elif(choice == "2"):
            print("---------------------")
            print("2: Batch Order Review")
            print("---------------------")
            c = read_Customer()
            if c:
                print_customer(c, s)
                process_order(c, s)
            return_to_menu()
        elif(choice == "3"):
            print("------------------")
            print("3: Live Order Mode")
            print("------------------")
            print_shop(s)
            print("Please choose from our products listed above:")
            print("---------------------------------------------")
            c = live_order(s)
            if c:
                print_customer(c, s)
                process_order(c, s)
            return_to_menu()
        elif(choice == "0"):
            print("--------------------------------------------------")
            print("\nThank you for shopping at Rosco's, have a nice day.")
            break
        else:
            display_menu()

if __name__ == "__main__":
    main()