from Database import connection
#Database connection establise
connection()

from Customers import Customers
from Sales import Sales
from Products import Products
from SalesItem import SaleItems

def main_manu():
    while True:
        print("1: Customers management")
        print("2: Product management")
        print("3: Sales management")
        print("4: Sale_item management")
        print("0: Exit")

        choice =int(input("Enter choice: "))

        match choice:
            case 1:
                Customers().customer_menu()
            case 2:
                Products().product_menu()
            case 3:
                Sales().sales_menu()
            case 4:
                SaleItems().create_table()
            case 0:
                break
            case _:
                print("Wrong Choice")
if __name__=="__main__":
    main_manu()
