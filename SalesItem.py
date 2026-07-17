from Database import conn
class SaleItems:
    @staticmethod
    def create_table():
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sale_items(
                        id SERIAL PRIMARY KEY,
                        sales_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        price DECIMAL(10,2) NOT NULL,
                        CONSTRAINT fk_sale_item_sales
                        FOREIGN KEY (sales_id)
                        REFERENCES sales(id)
                        ON DELETE CASCADE,

                        CONSTRAINT fk_sale_item_product
                        FOREIGN KEY (product_id)
                        REFERENCES products(id)
                        ON DELETE CASCADE)
                        """)
            conn.commit()