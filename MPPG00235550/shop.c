#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Data Structures
// Establishing the data structures to be placed within the shop's various functions:
// The data includes products, products' stock, the shop and its customers.

// Products, including their names and prices.
struct Product {
    char* name;
    double price;
};

// Product Stock, including referencing Product struct info, holding the quantity of each product.
struct ProductStock {
    struct Product product;
    int quantity;
};

// Shop, which holds its cash, also referencing Product Stock info.
struct Shop {
    double cash;
    struct ProductStock stock[20];
    int index;
};

// Customer, including their names, budgets and shopping lists.
struct Customer {
    char* name;
    double budget;
    struct ProductStock shoppingList[10];
    int index;
};

// This function is used to print the shop's products' names and prices passed in as arguments.
void printProduct(struct Product p) {
    printf("Product Name: %s \nProduct Price: €%.2f\n", p.name, p.price);
    printf("--------------\n");
}

// This function is used to create and stock up the shop via the stock.csv inventory.
struct Shop createAndStockShop() {
    // declaring variables
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    fp = fopen("../stock.csv", "r"); // opens and reads stock.csv
    if(fp == NULL)                   // if no data is read, the shop program will shut down.
        exit(EXIT_FAILURE);

        read = getline(&line, &len, fp); // read variable set up to read through a file.
        float cash = atof(line); // cash variable converting string to float number.

        struct Shop shop = {cash};
    
    while((read = getline(&line, &len, fp)) != -1) {
        // strings are tokenized via strtok to retrieve the names,
        // the prices & the quantities from all lines in stock.csv
        char *n = strtok(line, ",");
        char *p = strtok(NULL, ",");
        char *q = strtok(NULL, ",");
        // quantities & prices are converted to integers & floats respectively.
        int quantity = atoi(q);
        double price = atof(p);
        // malloc allows for memory allocation of the names of all products.
        char *name = malloc(sizeof(char) * 50);
        strcpy(name, n);
        // establishing the structs for products & stock
        struct Product product = {name, price};
        struct ProductStock stockItem = {product, quantity};
        // shop's index is incremented for each item in csv_file.
        shop.stock[shop.index++] = stockItem;
    }
    return shop;
}

// This function prints the shop's cash in hand, also displays the levels of stock for all products.
void printShop(struct Shop *s) {
    printf("The shop has €%.2f cash in hand\n", s -> cash);
    for(int i = 0; i < s -> index; i++) {
        printProduct(s -> stock[i].product);
        printf("The shop has %d in stock.\n", s -> stock[i].quantity);
    printf("----------------\n");
    }
}

// This function displays the main menu, allowing users to navigate through all available options.
void displayMenu() {
    fflush(stdin); // this will flush the output buffer
    printf("\n");
    printf("\t\tWelcome to Rosco's. How may we help you?");
    printf("\t\t----------------------------------------");
    printf("\t\t\tPress 1 for Shop Inventory");
    printf("\t\t\tPress 2 for Batch Order Review");
    printf("\t\t\tPress 3 for Live Order Mode");
    printf("\t\t\tPress 0 to Exit");
}

// This function allows the user to return to the main menu.
void returnToMenu() {
    fflush(stdin);
    char menu;
    printf("\nPress Enter to return to the main menu: ");
    scanf("%c", &menu);
    if(menu){
        displayMenu();
    }
}

// reading in customers from CSV file
struct Customer readCustomer() {
    FILE * fp;
    // allocating memory for the customer file name
    char *filename = malloc(sizeof(char) * 20);
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    printf("Please enter a customer's file name: ");
    scanf("%s", filename);

    // found customer's name is concatenated with the .csv extension.
    strcat(filename, ".csv");
    char filepath[40] = "../";
    strcat(filepath, filename);

    read = getline(&line, &len, fp);
    // strings are tokenised via strtok to retrieve
    // customer names and budgets from the csv file.
    char *n = strtok(line, ",");
    char *b = strtok(NULL, ",");
    char *name = malloc(sizeof(char) * 100);
    // strcpy is used to avoid overwriting during strtok.
    strcpy(name, n);
    // customer budgets are converted to double integer (eg, €5.50).
    double budget = atof(b);
    // creating customer struct with name and budget within.
    struct Customer customer = {name, budget};

    // the while loop is used to read through the entire CSV file
    while((read = getline(&line, &len, fp)) != -1) {
        char *n = strtok(line, ",");
        char *q = strtok(NULL, ",");
        int quantity = atoi(q);
        char *pname = malloc(sizeof(char) * 20);
        strcpy(pname, n);
        struct Product product = {pname};
        struct ProductStock cusItem = {product, quantity};
        // increment the index in a customer's shopping list
        customer.shoppingList[customer.index++] = cusItem;
    }
    return customer;
}

// this function prints customer information along with their shopping lists
void printCustomer(struct Customer *cus, struct Shop *shop) {
    printf("Customer Name: %s \nCustomer Budget: €%.2f\n", cus -> name, cus -> budget);
    printf("Customer Order:\n");
    // this for loop goes through all items on a customer's shopping list
    for(int i = 0; i < cus -> index; i++) {
        printProduct(cus -> shoppingList[i].product);
        printf("%s ordered %d unit(s) of the above product(s)\n", cus -> name, cus -> shoppingList[i].quantity);
        printf("--------------------------\n");
    }
    printf("Please wait while we check our available stock...\n");
    printf("------------------------------------------------");
    printf("Rosco's have the following items in stock:\n");
    for(int i = 0; i < cus -> index; i++) {
        char *cusProduct = cus -> shoppingList[i].product.name;
        double cusProductPrice = cus -> shoppingList[i].product.price;
        for(int j = 0; j < shop -> index; j++) {
            char *shopProduct = shop -> stock[j].product.name;
            double shopProductPrice = shop -> stock[j].product.price;
            if(strcmp(cusProduct, shopProduct) == 0) {
                cusProductPrice = shopProductPrice;
                printf("%d units of %s at €%.2f per unit, for a total cost of €%.2f\n", cus -> shoppingList[i].quantity, cusProduct, shopProductPrice, cus -> shoppingList[i].quantity* shopProductPrice);
            }
        }
    }
}

// this struct is used to represent a live customer shopping
struct Customer liveCustomer() {
    printf("3: Live Order Mode\n");
    char *productName = (char*) malloc(10 * sizeof(char));
    char *pq = (char*) malloc(3 * sizeof(char));
    char *cusName = malloc(sizeof(char) * 30);
    char *b = (char*) malloc(10 * sizeof(char));
    printf("Please enter your name: ");
    scanf("%s", cusName);
    printf("Welcome to Rosco's, %s.\n", cusName);
    printf("Please enter your budget: €");
    scanf("%s", b);
    double budget = atof(b);
    printf("Your budget is €%lf\n", budget);
    struct Customer customer = {cusName, budget};
    if(budget == 0) {
        printf("Error: please enter your budget as a number.\n");
        returnToMenu();
    }
    else {
        printf("Please enter the name of the product you are looking to buy: ");
        scanf("%s", productName);
        printf("Please enter the quantity of %s you are looking to buy: ", productName);
        struct Product product = {productName};
        scanf("%s", pq);
        int productQuantity = atoi(pq);
        printf("You are looking for %d of %s\n", productQuantity, productName);
        struct ProductStock cusItem = {product, productQuantity};
        customer.shoppingList[customer.index++] = cusItem;
        if(productQuantity == 0)
        {
            printf("Error: please enter a quantity as an integer.\n");
            returnToMenu();
        }
    }
    return customer;
}

// this struct processes the orders
struct Shop processingOrder(struct Shop *shop, struct Customer *cus) {
    printf("Processing your order, please wait.\n");
    printf("-----------------------------------\n");
    double startingcash = 0;
    startingcash = shop -> cash;
    double startingWallet = cus -> budget;
    double totalCost = 0;
    for(int i = 0; i < cus -> index; i++) {
        char *cusItem = malloc(sizeof(char) * 30);
        strcpy(cusItem, cus -> shoppingList[i].product.name);
        for(int j = 0; j < shop -> index; j++) {
            char *shopItem = malloc(sizeof(char) * 30);
            strcpy(shopItem, shop -> stock[j].product.name);
            if(strcmp(cusItem, shopItem) == 0) {
                int cusQty = cus -> shoppingList[i].quantity;
                int shopQty = shop -> stock[j].quantity;
                double price = shop -> stock[j].product.price;
                double totalProductCost = 0;
                if(shopQty >= cusQty) {
                    totalProductCost = price * cusQty;
                    if(cus -> budget >= totalProductCost) {
                        shop -> cash += totalProductCost;
                        cus -> budget -= totalProductCost;
                        printf("€%.2f has been deducted from the customer's funds for %d unit(s) of %s.\n\n", totalProductCost, cusQty, cusItem);
                        shop -> stock[j].quantity = shop -> stock[j].quantity - cusQty;
                    }
                    else if((cus -> budget < totalProductCost)) {
                        printf("Error: insufficient funds, the customer has €%.2f, €%.2f is required for %s.\n", cus -> budget, totalProductCost, cusItem);
                    }
                }
                else if(strcmp(cusItem, shopItem) != 0) {
                    printf("");
                }
            }
        }
    }
    return *shop;
}

int main(void) {
    struct Shop shop = createAndStockShop();
    displayMenu();
    int choice = -1;
    while(choice != 0) {
        printf("Please select an option from the main menu: \t");
        scanf("%d", &choice);
    
    if(choice == 1) {
        printf("1: Shop Inventory\n");
        printShop(&shop);
        returnToMenu();
    }
    else if(choice == 2) {
        printf("2: Batch Order Review");
        printf("-------------\n");
        struct Customer customer = readCustomer();
        if(customer.budget == 0) {
            returnToMenu();
        }
        else {
            printCustomer(&customer, &shop);
            processingOrder(&shop, &customer);
            printf("Updating Balance\n-------------\nCustomer %s has €%.2f remaining.\n", customer.name, customer.budget);
            returnToMenu();
        }
    }
    else if(choice == 3) {
        printf("3: Live Order Mode");
        printf("Please choose from our products listed below: \n");
        printShop(&shop);
        struct Customer c = liveCustomer();
        printCustomer(&c, &shop);
        processingOrder(&shop, &c);
        printf("The customer has €%.2f remaining.", c.name, c.budget);
        returnToMenu();
    }
    else {
        returnToMenu();
    }
}
printf("Thank you for shopping at Rosco's, have a nice day.\n");
return 0;
}