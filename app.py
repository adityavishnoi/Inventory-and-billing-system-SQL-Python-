import streamlit as st
import pandas as pd
from datetime import date
from Database import conn
from Customers import Customers
from Sales import Sales
from Products import Products
from SalesItem import SaleItems

# --- Page Configuration ---
st.set_page_config(page_title="E-Commerce Management", layout="wide", page_icon="🛒")

def main():
    # --- Sidebar ---
    st.sidebar.title("🛒 E-Commerce App")
    st.sidebar.markdown("---")
    
    # Navigation
    menu = st.sidebar.radio("Navigate to:", [
        "🏠 Dashboard", 
        "👥 Customers", 
        "📦 Products", 
        "📈 Sales", 
        "📊 Analytics & Billing"
    ])

    st.sidebar.markdown("---")
    if st.sidebar.button("⚠️ Initialize / Create Tables"):
        try:
            Customers.create_table()
            Products.create_table()
            Sales.create_table()
            SaleItems.create_table()
            st.sidebar.success("All tables created successfully!")
        except Exception as e:
            st.sidebar.error(f"Error creating tables: {e}")

    # ==========================================
    # 0. DASHBOARD (NEW!)
    # ==========================================
    if menu == "🏠 Dashboard":
        st.title("🏠 Business Dashboard")
        st.markdown("Welcome to your E-Commerce overview.")
        
        try:
            with conn.cursor() as cur:
                # Fetch Top-Level Metrics
                cur.execute("SELECT SUM(total_amount), COUNT(id) FROM sales")
                sales_metrics = cur.fetchone()
                total_rev = sales_metrics[0] if sales_metrics[0] else 0
                total_orders = sales_metrics[1] if sales_metrics[1] else 0
                
                cur.execute("SELECT COUNT(id) FROM customers")
                total_cust = cur.fetchone()[0]

            # Display KPI Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Total Revenue", f"${total_rev:,.2f}")
            col2.metric("📦 Total Orders", total_orders)
            col3.metric("👥 Total Customers", total_cust)
            
            st.markdown("---")
            
            # Charts Layout
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.subheader("📈 Sales Trend (Revenue over Time)")
                try:
                    query = "SELECT date, SUM(total_amount) as revenue FROM sales GROUP BY date ORDER BY date"
                    df_trend = pd.read_sql_query(query, conn)
                    if not df_trend.empty:
                        df_trend.set_index("date", inplace=True)
                        st.line_chart(df_trend)
                    else:
                        st.info("Not enough data for trend line.")
                except Exception as e:
                    st.warning("Chart error: Ensure tables exist and contain data.")

            with chart_col2:
                st.subheader("🏆 Top Selling Products")
                try:
                    query = """
                        SELECT p.name, SUM(si.quantity) as sold 
                        FROM sale_items si 
                        JOIN products p ON si.product_id = p.id 
                        GROUP BY p.name 
                        ORDER BY sold DESC LIMIT 5
                    """
                    df_top = pd.read_sql_query(query, conn)
                    if not df_top.empty:
                        df_top.set_index("name", inplace=True)
                        st.bar_chart(df_top)
                    else:
                        st.info("Not enough data for product chart.")
                except Exception:
                    st.warning("Chart error: Ensure tables exist and contain data.")
                    
        except Exception as e:
            st.error(f"Could not load dashboard data: {e}")

    # ==========================================
    # 1. CUSTOMERS MANAGEMENT
    # ==========================================
    elif menu == "👥 Customers":
        st.title("👥 Customer Management")
        tab1, tab2, tab3, tab4 = st.tabs(["📋 View Customers", "➕ Add Customer", "✏️ Update Customer", "🗑️ Delete Customer"])

        with tab1:
            try:
                customers = Customers.get_all_customers()
                if customers:
                    df = pd.DataFrame(customers, columns=["ID", "Name", "Contact"])
                    st.dataframe(df, width=800, hide_index=True)
                else:
                    st.info("No customers found.")
            except Exception as e:
                st.error(f"Error fetching customers: {e}")

        with tab2:
            with st.form("add_customer"):
                name = st.text_input("Customer Name")
                contact = st.text_input("Contact Number")
                if st.form_submit_button("Add Customer"):
                    if name and contact:
                        Customers.insert_customer(name, contact)
                        st.success(f"Customer '{name}' added successfully!")
                    else:
                        st.warning("Please fill out all fields.")

        with tab3:
            with st.form("update_customer"):
                c_id = st.number_input("Customer ID", min_value=1, step=1)
                new_name = st.text_input("New Name (leave blank to keep unchanged)")
                new_contact = st.text_input("New Contact (leave blank to keep unchanged)")
                if st.form_submit_button("Update Customer"):
                    Customers.update_customer(str(c_id), name=new_name if new_name else None, contact=new_contact if new_contact else None)
                    st.success(f"Customer ID {c_id} updated successfully!")

        with tab4:
            with st.form("delete_customer"):
                c_id = st.number_input("Customer ID to delete", min_value=1, step=1)
                if st.form_submit_button("Delete Customer"):
                    Customers.delete_customer(str(c_id))
                    st.success(f"Customer ID {c_id} deleted successfully!")

    # ==========================================
    # 2. PRODUCTS MANAGEMENT
    # ==========================================
    elif menu == "📦 Products":
        st.title("📦 Product Management")
        tab1, tab2, tab3, tab4 = st.tabs(["📋 View Products", "➕ Add Product", "✏️ Update Product", "🗑️ Delete Product"])

        with tab1:
            try:
                products = Products.view_all_products() 
                if products:
                    df = pd.DataFrame(products, columns=["ID", "Name", "Description", "Price", "Stock Qty"])
                    st.dataframe(df, width=1000, hide_index=True)
                else:
                    st.info("No products found.")
            except Exception as e:
                st.error(f"Error fetching products: {e}")

        with tab2:
            with st.form("add_product"):
                name = st.text_input("Product Name")
                desc = st.text_area("Description")
                price = st.number_input("Price", min_value=0.0, step=1.0)
                qty = st.number_input("Quantity", min_value=0, step=1)
                if st.form_submit_button("Add Product"):
                    if name and desc:
                        Products.insert_product(name, desc, price, qty)
                        st.success(f"Product '{name}' added successfully!")
                    else:
                        st.warning("Please fill out all fields.")

        with tab3:
            with st.form("update_product"):
                p_id = st.number_input("Product ID", min_value=1, step=1)
                new_name = st.text_input("New Name (optional)")
                new_desc = st.text_area("New Description (optional)")
                new_price = st.number_input("New Price (0.0 to ignore)", min_value=0.0, step=1.0)
                new_qty = st.number_input("New Quantity (0 to ignore)", min_value=0, step=1)
                if st.form_submit_button("Update Product"):
                    Products.update_product(
                        str(p_id), name=new_name if new_name else None,
                        description=new_desc if new_desc else None,
                        price=new_price if new_price > 0 else None,
                        quantity=new_qty if new_qty > 0 else None
                    )
                    st.success(f"Product ID {p_id} updated successfully!")

        with tab4:
            with st.form("delete_product"):
                p_id = st.number_input("Product ID to delete", min_value=1, step=1)
                if st.form_submit_button("Delete Product"):
                    Products.delete_product(str(p_id))
                    st.success(f"Product ID {p_id} deleted successfully!")

    # ==========================================
    # 3. SALES MANAGEMENT
    # ==========================================
    elif menu == "📈 Sales":
        st.title("📈 Sales Management")
        tab1, tab2, tab3, tab4 = st.tabs(["📋 View Sales", "➕ Record Sale", "✏️ Update Sale", "🗑️ Delete Sale"])

        with tab1:
            try:
                sales = Sales.view_all_sales()
                if sales:
                    df = pd.DataFrame(sales, columns=["Sale ID", "Customer ID", "Date", "Total Amount"])
                    st.dataframe(df, width=800, hide_index=True)
                else:
                    st.info("No sales records found.")
            except Exception as e:
                st.error(f"Error fetching sales: {e}")

        with tab2:
            with st.form("add_sale"):
                c_id = st.number_input("Customer ID", min_value=1, step=1)
                sale_date = st.date_input("Sale Date", value=date.today())
                total = st.number_input("Total Amount", min_value=0.0, step=1.0)
                if st.form_submit_button("Record Sale"):
                    Sales.insert_sales(str(c_id), sale_date, total)
                    st.success("Sale recorded successfully!")

        with tab3:
            with st.form("update_sale"):
                s_id = st.number_input("Sale ID to update", min_value=1, step=1)
                new_c_id = st.text_input("New Customer ID (leave blank to ignore)")
                new_date = st.date_input("New Date")
                new_total = st.number_input("New Total Amount (0.0 to ignore)", min_value=0.0, step=1.0)
                if st.form_submit_button("Update Sale"):
                    Sales.update_sales(
                        str(s_id), customer_id=new_c_id if new_c_id else None,
                        date=new_date, total_amount=new_total if new_total > 0 else None
                    )
                    st.success(f"Sale ID {s_id} updated successfully!")

        with tab4:
            with st.form("delete_sale"):
                s_id = st.number_input("Sale ID to delete", min_value=1, step=1)
                if st.form_submit_button("Delete Sale"):
                    Sales.delete_sales(str(s_id))
                    st.success(f"Sale ID {s_id} deleted successfully!")

    # ==========================================
    # 4. ANALYTICS & BILLING (UPGRADED!)
    # ==========================================
    elif menu == "📊 Analytics & Billing":
        st.title("📊 Analytics & Detailed Billing")
        tab1, tab2, tab3 = st.tabs(["🧾 Detailed Bill", "📅 Sales by Date", "👤 Customer Sales"])

        with tab1:
            st.subheader("Generate Detailed Receipt")
            st.markdown("Enter a Sale ID to pull full customer and itemized data.")
            
            s_id = st.number_input("Enter Sale ID", min_value=1, step=1, key="bill_sale_id")
            if st.button("Generate Receipt 🖨️"):
                try:
                    with conn.cursor() as cur:
                        # Fetch Sale & Customer details
                        cur.execute("""
                            SELECT s.id, s.date, s.total_amount, c.id, c.name, c.contact 
                            FROM sales s
                            JOIN customers c ON s.customer_id = c.id
                            WHERE s.id = %s
                        """, (s_id,))
                        invoice_data = cur.fetchone()

                        if invoice_data:
                            # Fetch Itemized Product Details
                            cur.execute("""
                                SELECT p.name, si.quantity, si.price, (si.quantity * si.price) as subtotal
                                FROM sale_items si
                                JOIN products p ON si.product_id = p.id
                                WHERE si.sales_id = %s
                            """, (s_id,))
                            items_data = cur.fetchall()

                            # --- UI RENDER FOR RECEIPT ---
                            st.markdown("---")
                            st.markdown(f"### 🧾 INVOICE #00{invoice_data[0]}")
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.write(f"**👤 Customer Name:** {invoice_data[4]}")
                                st.write(f"**🆔 Customer ID:** {invoice_data[3]}")
                                st.write(f"**📞 Contact:** {invoice_data[5]}")
                            with col_b:
                                st.write(f"**📅 Date:** {invoice_data[1]}")
                                st.write("**🏢 E-Commerce Inc.**")
                            
                            st.markdown("#### Itemized Bill:")
                            if items_data:
                                df_items = pd.DataFrame(items_data, columns=["Product Name", "Qty", "Unit Price ($)", "Subtotal ($)"])
                                st.table(df_items)  # Renders as a beautiful static table
                                
                                # Using the backend function for mathematical total verification
                                bill_total = Sales.generate_bill(s_id)
                                st.success(f"**Grand Total:** ${bill_total:,.2f}")
                            else:
                                st.warning("No items found for this sale ID in the 'sale_items' table.")
                            st.markdown("---")
                            
                        else:
                            st.error("Sale ID not found. Please ensure the Sale ID exists.")

                except Exception as e:
                    st.error(f"Database Error: {e}")

        with tab2:
            st.subheader("Revenue by Date Range")
            col1, col2 = st.columns(2)
            with col1:
                start_d = st.date_input("Start Date")
            with col2:
                end_d = st.date_input("End Date")
                
            if st.button("Fetch Sales Summary"):
                try:
                    sales_data = Sales.view_sales_by_date(start_d, end_d)
                    if sales_data and sales_data[0] is not None:
                        st.info(f"Total Revenue from {start_d} to {end_d}: **${sales_data[0]:,.2f}**")
                    else:
                        st.warning("No sales found in this date range.")
                except Exception as e:
                    st.error(f"Error executing query: {e}")

        with tab3:
            st.subheader("Lookup Customer Purchase History")
            c_id = st.number_input("Enter Customer ID", min_value=1, step=1, key="cust_hist_id")
            if st.button("Fetch History"):
                try:
                    c_sales = Sales.get_sales_by_customer(str(c_id))
                    if c_sales:
                        df_history = pd.DataFrame(c_sales, columns=["Sale ID", "Customer ID", "Date", "Total Amount"])
                        st.dataframe(df_history, width=800, hide_index=True)
                        st.success(f"Found {len(c_sales)} past orders for this customer.")
                    else:
                        st.info("No sales found for this customer.")
                except Exception as e:
                    st.error(f"Error executing query: {e}")

if __name__ == "__main__":
    main()