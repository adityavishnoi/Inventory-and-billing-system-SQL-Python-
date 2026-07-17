import psycopg2

from Database import conn
class Products:
    def __init__(self):
        pass
      
    @staticmethod
    def create_table():
        cur=conn.cursor()

        cur.execute(
            """CREATE TABLE IF NOT EXISTS products(
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            description TEXT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            quantity INTEGER NOT NULL
            )"""
        )
        conn.commit()
        cur.close()

    @staticmethod
    def insert_product(name,description,price,quantity):
        cur=conn.cursor()

        cur.execute(
            """INSERT INTO products(name,description,price,quantity)
            VALUES(%s,%s,%s,%s)
            """,
            (name,description,price,quantity)
        )

        conn.commit()
        cur.close()
    @staticmethod
    def update_product(product_id,name=None,description=None,price=None,quantity=None):
        cur=conn.cursor()

        cur.execute("SELECT * FROM products WHERE id=%s",(product_id))
        product=cur.fetchone()
        if not product:
            print(">>>>> product not found")
            cur.close()
            return
    
        update_fields=[]

        if name:
            update_fields.append(f"name='{name}'")
        if description:
            update_fields.append(f"description='{description}'")
        if price:
            update_fields.append(f"contact='{price}'")
        if quantity:
            update_fields.append(f"quantity='{quantity}'")
        update_query=f"UPDATE products SET {",".join(update_fields)} WHERE id=%s"

        cur.execute(update_query,(product_id,))
        cur.close()
        conn.commit()

    @staticmethod
    def delete_product(pro_id):
        cur=conn.cursor()

        cur.execute(
            """DELETE FROM products WHERE id=%s
            """,
            (pro_id)
        )
        conn.commit()
        cur.close()
    @staticmethod
    def view_all_products():
        cur=conn.cursor()

        cur.execute(
            """SELECT * FROM products"""
        )
        products=cur.fetchall()

        cur.close()
        return products
    @staticmethod
    def view_product_id(prod_id):
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM products WHERE id=%s""",(prod_id))
            product=cur.fetchone()
            return product


    @staticmethod
    def product_menu():
        while True:
            print("1: Create Table ")
            print("2: Insert product ")
            print("3: Update product ")
            print("4: Delete product ")
            print("5: View products ")
            print("6: view single product")
            print("0: Exit ")
            choice = int(input("Enter Choice: "))

            match choice:
                case 1:
                    Products().create_table()
                    print("table created!!")
                case 2:
                    name=input("Enter name : ")
                    description=input("Enter description: ")
                    price=input("Enter price: ")
                    quantity=input("Enter quantity: ")

                    Products().insert_product(name,description,price,quantity)

                    print("product inserted!!")
                case 3:
                    product_id=input("Enter product_id: ")

                    name=input("Enter new name: ")
                    description=input("Enter new description: ")
                    price=input("Enter new price:")
                    quantity=input("Enter new quantity: ")
                    Products().update_product(product_id,name,description,price,quantity)
                    print("product updated!! ")
                case 4:
                    product_id=input("Enter product id: ")
                    Products().delete_product(product_id)
                    print("product deleted!! ")
                case 5:
                    products= Products().view_all_products()
                    print(products)
                    print("products fetched!!")
                case 6:
                    p_id=input("Enter product id: ")
                    prod=Products().view_product_id(p_id)

                    print(prod)
                    print("product fetched!!")
                case 0:
                    print("exiting... ")
                    break
                case _:
                    print("wrong choice!! ")
                    Products().product_menu()


# Product().product_menu()

                    




 