import psycopg2
from Database import conn
class Sales:
    def __init__(self):
        pass
      
    @staticmethod
    def create_table():
        cur=conn.cursor()

        cur.execute(
            """CREATE TABLE IF NOT EXISTS sales(
            id SERIAL PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            date DATE NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            CONSTRAINT fk_sales_customer 
            FOREIGN KEY (customer_id)
            REFERENCES customers(id)
            ON DELETE CASCADE
            )"""
        )
        conn.commit()
        cur.close()

    @staticmethod
    def insert_sales(customer_id,date,total_amount):
        cur=conn.cursor()

        cur.execute(
            """INSERT INTO sales(customer_id,date,total_amount)
            VALUES(%s,%s,%s)
            """,
            (customer_id,date,total_amount)
        )

        conn.commit()
        cur.close()


    @staticmethod
    def update_sales(sales_id,customer_id=None,date=None,total_amount=None):
        cur=conn.cursor()

        cur.execute("SELECT * FROM sales WHERE id=%s",(sales_id))
        sales=cur.fetchone()
        if not sales:
            print(">>>>> Sales not found")
            cur.close()
            return
    
        update_fields=[]

        if customer_id:
            update_fields.append(f"customer_id='{customer_id}'")
        if date:
            update_fields.append(f"date='{date}'")
        if total_amount:
            update_fields.append(f"total_amount='{total_amount}'")
        
        update_query=f"UPDATE sales SET {",".join(update_fields)} WHERE id=%s"

        cur.execute(update_query,(sales_id,))
        cur.close()
        conn.commit()


    @staticmethod
    def delete_sales(sale_id):
        cur=conn.cursor()

        cur.execute(
            """DELETE FROM sales WHERE id=%s
            """,
            (sale_id)
        )
        conn.commit()
        cur.close()
    
   
    @staticmethod
    def generate_bill(sale_id):
        with conn.cursor() as cur:
            # Changed 'Sales' to 'sale_items' and 'id' to 'sales_id'
            cur.execute("""SELECT * FROM sale_items WHERE sales_id=%s""", (sale_id,))
            sale_items = cur.fetchall()
            total = 0

            # item[3] is quantity, item[4] is price in the sale_items table
            for item in sale_items:
                total += item[4] * item[3]
            return total
            

    @staticmethod
    def view_all_sales():
        cur=conn.cursor()

        cur.execute(
            """SELECT * FROM sales"""
        )
        sales=cur.fetchall()

        cur.close()
        return sales

    @staticmethod
    def view_sale_id(sale_id):
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM sales WHERE id=%s""",(sale_id))
            sale=cur.fetchone()
            return sale

    #Analytical Query
    @staticmethod
    def view_sales_by_date(start_date,end_date):
        with conn.cursor() as cur:
            cur.execute("""SELECT SUM(total_amount) FROM sales WHERE date BETWEEN %s AND %s""",(start_date,end_date))
            sales=cur.fetchall()
        return sales

    @staticmethod
    def get_top_selling_products():
        with conn.cursor() as cur: 
            cur.execute("""
                SELECT product_id, SUM(quantity) AS total_quantity 
                FROM sale_items 
                GROUP BY product_id 
                ORDER BY total_quantity DESC
                LIMIT 5
            """)
            top_selling = cur.fetchall()
        return top_selling
    
    @staticmethod
    def get_sales_by_customer(customer_id):
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM sales WHERE customer_id=%s""",(customer_id))
            sales=cur.fetchall()
        return sales

    @staticmethod
    def sales_menu():
        
        while True:
            print("1: Create Table ")
            print("2: Insert Sales ")
            print("3: Update Sales ")
            print("4: Delete Sales ")
            print("5: View Sales ")
            print("6: View single Sales")
            print("7: Get sales by date")
            print("8: Get top selling products")
            print("9: Get sales by customer")
            print("10: Generate bill")
            print("0: Exit ")
            choice = int(input("Enter Choice: "))

            match choice:
                case 1:
                    Sales().create_table()
                    print("table created!!")
                case 2:
                    customer_id=input("Enter customer id : ")
                    date=input("Enter date: ")
                    total_amount=input("Enter total amount: ")
                    

                    Sales().insert_sales(customer_id,date,total_amount)

                    print("Sales inserted!!")
                case 3:
                    sales_id=input("Enter sales id: ")

                    customer_id=input("Enter customer id : ")
                    date=input("Enter date: ")
                    total_amount=input("Enter total amount: ")
                    

                    Sales().update_sales_Sales(customer_id,date,total_amount)
                    print("Sales updated!! ")
                case 4:
                    sales_id=input("Enter Sales id: ")
                    Sales().delete_Sales(sales_id)
                    print("Sales deleted!! ")
                case 5:
                    sales= Sales().view_all_Sales()
                    print(sales)
                    print("Sales fetched!!")
                case 6:
                    s_id=input("Enter Sales id: ")
                    sale=Sales().view_Sales_id(s_id)

                    print(sale)
                    print("Sales fetched!!")

                case 7:
                    start_date=input("Enter start date: ")
                    end_date=input("Enter end date: ")

                    sale=Sales().view_sales_by_date(self,start_date,end_date)
                    print(sale)
                    print("Sales fetched!!")
                case 8:
                    sale=Sales().get_top_selling_products()
                    print(sale)
                    print("Sales fetched!!")
                case 9:
                    custm_id=input("Enter customer_id: ")
                    sale=Sales().get_sales_by_customer(custm_id)
                    print(sale)
                    print("Sales fetched!!")
                case 10:
                    sale_id=input("Enter sales id: ")
                    bill=Sales().generate_bill(sale_id)
                    print(bill)


                case 0:
                    print("exiting... ")
                    break
                case _:
                    print("-"*50)
                    print("wrong choice!! ")
                    print("-"*50)
                    Sales().sales_menu()


# Sales().sales_menu()

                    




 