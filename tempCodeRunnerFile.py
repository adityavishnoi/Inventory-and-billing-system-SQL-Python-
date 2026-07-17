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
        print(total)
    Sales().generate_bill(1)