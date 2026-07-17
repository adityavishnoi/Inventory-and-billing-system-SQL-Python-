import psycopg2
from Database import conn
class Customers:
    def __init__(self):
        pass
        # self.name=name
        # self.contact=contact
    
    @staticmethod
    def create_table():
        cur=conn.cursor()

        cur.execute(
            """CREATE TABLE IF NOT EXISTS customers(
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            contact VARCHAR(15) NOT NULL
            )"""
        )
        conn.commit()
        cur.close()

    @staticmethod
    def insert_customer(name,contact):
        cur=conn.cursor()

        cur.execute(
            """INSERT INTO customers(name,contact)
            VALUES(%s,%s)
            """,
            (name,contact)
        )

        conn.commit()
        cur.close()
    @staticmethod
    def update_customer(customer_id,name=None,contact=None):
        cur=conn.cursor()

        cur.execute("SELECT * FROM customers WHERE id=%s",(customer_id))
        customer=cur.fetchone()
        if not customer:
            print(">>>>> customer not found")
            cur.close()
            return
    
        update_fields=[]

        if name:
            update_fields.append(f"name='{name}'")
        if contact:
            update_fields.append(f"contact='{contact}'")
        update_query=f"UPDATE customers SET {",".join(update_fields)} WHERE id=%s"

        cur.execute(update_query,(customer_id,))
        cur.close()
        conn.commit()

    @staticmethod
    def delete_customer(cus_id):
        cur=conn.cursor()

        cur.execute(
            """DELETE FROM customers WHERE id=%s
            """,
            (cus_id)
        )
        conn.commit()
        cur.close()
    @staticmethod
    def get_all_customers():
        cur=conn.cursor()

        cur.execute(
            """SELECT * FROM customers"""
        )
        customers=cur.fetchall()

        cur.close()
        return customers
    @staticmethod
    def customer_menu():
        
        while True:
            print("1: Create Table ")
            print("2: Insert Customer ")
            print("3: Update Customer ")
            print("4: Delete Customer ")
            print("5: View Customers ")
            print("0: Exit ")
            choice = int(input("Enter Choice: "))

            match choice:
                case 1:
                    Customers().create_table()
                    print("table created!!")
                case 2:
                    name=input("Enter name : ")
                    contact=input("Enter contact: ")

                    Customers().insert_customer(name,contact)

                    print("customer inserted!!")
                case 3:
                    customer_id=input("Enter customer id: ")

                    name=input("Enter name: ")
                    contact=input("Enter contact: ")

                    Customers().update_customer(customer_id,name,contact)
                    print("Customer updated!! ")
                case 4:
                    customer_id=input("Enter customer id: ")
                    Customers().delete_customer(customer_id)
                    print("customer deleted!! ")
                case 5:
                    customers= Customers().get_all_customers()
                    print(customers)
                    print("Customers fetched!!")
                case 0:
                    print("exiting ")
                    break
                case _:
                    print("wrong choice!! ")
                    Customers().customer_menu()


# Customer().customer_menu()

                    




 