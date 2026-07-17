# 🛒 E-Commerce Management System

A robust, full-stack inventory and sales management dashboard built with Python, Streamlit, and PostgreSQL. This application provides a seamless graphical user interface (GUI) to manage customers, track inventory, record sales, and generate detailed itemized invoices.

---

## ✨ Key Features

* **📊 Interactive Dashboard:** Get a bird's-eye view of your business with KPI metrics (Total Revenue, Total Orders, Total Customers), a Sales Trend line chart, and a Top Selling Products bar chart.
* **👥 Customer Management:** Complete CRUD (Create, Read, Update, Delete) operations to manage your customer database.
* **📦 Inventory Management:** Keep track of your product catalog, including descriptions, pricing, and stock quantities.
* **📈 Sales Tracking:** Record new sales and link them to specific customers and dates.
* **🧾 Advanced Billing & Analytics:** 
  * Generate detailed, itemized receipts that automatically join customer data and product details.
  * Query total revenue over custom date ranges.
  * Look up comprehensive purchase histories for individual customers.
* **⚙️ Auto-Initialization:** A built-in feature to automatically create all necessary PostgreSQL tables directly from the UI.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (for building the interactive web app dashboard)
* **Backend:** Python 3
* **Database:** PostgreSQL (Relational Database)
* **Libraries:** `pandas` (for data manipulation and chart rendering), `psycopg2` (PostgreSQL database adapter)

---

## 🗄️ Database Schema

The system utilizes a fully relational SQL database with four primary tables:
1. **`customers`**: Stores customer names and contact info.
2. **`products`**: Stores product names, descriptions, prices, and stock levels.
3. **`sales`**: Records top-level transaction data (Customer ID, Date, Total Amount).
4. **`sale_items`**: A junction table linking specific sales to specific products, capturing historical quantities and prices.

---
