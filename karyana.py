import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import os
import base64

# Database initialization
def init_db():
    conn = sqlite3.connect('karyana_streamlit.db')
    cursor = conn.cursor()
    
    # Inventory Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT UNIQUE,
                        stock INTEGER,
                        price REAL,
                        cost_price REAL DEFAULT 0.0)''')
                        
    # Khata Table (Customers)
    cursor.execute('''CREATE TABLE IF NOT EXISTS khata (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        phone TEXT UNIQUE,
                        balance REAL DEFAULT 0.0)''')
                        
    # Sales Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sale_date TEXT,
                        item_name TEXT,
                        quantity INTEGER,
                        total_sale REAL,
                        total_cost REAL,
                        profit REAL,
                        payment_mode TEXT,
                        customer_name TEXT DEFAULT '')''')
                        
    # Expenses Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        expense_date TEXT,
                        category TEXT,
                        amount REAL,
                        details TEXT)''')
                        
    # Suppliers Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        phone TEXT UNIQUE,
                        company TEXT,
                        balance REAL DEFAULT 0.0)''')
                        
    conn.commit()
    conn.close()

init_db()

# Main App Layout Configuration
st.set_page_config(page_title="AHA Trendy Karyana", layout="wide")

# Helper function to convert local image to base64 for HTML display
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# JS Helper function to trigger browser print menu
def trigger_print(html_content):
    custom_html = f"""
        <html>
        <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            .header {{ text-align: center; margin-bottom: 30px; border-bottom: 2px solid #000; padding-bottom: 10px; }}
            .footer {{ margin-top: 40px; text-align: center; font-size: 12px; color: #555; }}
        </style>
        </head>
        <body>
            {html_content}
            <script>
                window.print();
            </script>
        </body>
        </html>
    """
    components.html(custom_html, height=0, width=0)

# ==================== LOGIN SYSTEM WITH MODERN CSS ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

# Logo file check (will look for logo.jpg or logo.png)
logo_base64 = get_image_base64("logo.jpg") or get_image_base64("logo.png")

if not st.session_state.logged_in:
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        }
        [data-testid="stHeader"] {
            background: transparent;
        }
        .login-card {
            background-color: #ffffff;
            padding: 30px 40px 40px 40px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            margin-top: 40px;
            text-align: center;
        }
        .login-logo {
            max-width: 140px;
            height: auto;
            margin-bottom: 15px;
            border-radius: 50%;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .login-header {
            color: #1e3a8a;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
            font-size: 28px;
            margin-bottom: 5px;
            margin-top: 10px;
        }
        .login-subtitle {
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 25px;
        }
        div.stButton > button:first-child {
            background-color: #1e3a8a !important;
            color: white !important;
            width: 100% !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 20px !important;
            font-weight: bold !important;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #1d4ed8 !important;
            box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        if logo_base64:
            card_html = f"""
                <div class="login-card">
                    <img src="data:image/jpeg;base64,{logo_base64}" class="login-logo">
                    <h1 class="login-header">AHA TRENDY KARYANA</h1>
                    <p class="login-subtitle">System Login — Dukan Management Software</p>
                </div>
            """
        else:
            card_html = """
                <div class="login-card">
                    <h1 class="login-header">👔 AHA TRENDY KARYANA</h1>
                    <p class="login-subtitle">System Login — Dukan Management Software (Place 'logo.jpg' in folder)</p>
                </div>
            """
            
        st.markdown(card_html, unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div style='background: white; padding: 0px 40px 40px 40px; border-radius: 0 0 15px 15px; margin-top: -30px; box-shadow: 0 15px 25px rgba(0, 0, 0, 0.05);'>", unsafe_allow_html=True)
            username = st.text_input("Username (User ID)", placeholder="Enter username...")
            password = st.text_input("Password", type="password", placeholder="Enter password...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 LOG IN TO SYSTEM"):
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Admin"
                    st.success("🎉 Welcome Admin!")
                    st.rerun()
                elif username == "sales" and password == "sales123":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Salesman"
                    st.success("🎉 Welcome Salesman!")
                    st.rerun()
                else:
                    st.error("❌ Galat Username ya Password! Dubara koshish karen.")
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==================== MAIN DASHBOARD ====================
if logo_base64:
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <img src="data:image/jpeg;base64,{logo_base64}" style="max-width: 75px; height: auto; border-radius: 50%; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
            <h1 style="margin: 0; color: #1e3a8a; font-family: 'Segoe UI', Arial, sans-serif; font-size: 36px; font-weight: 700;">
                AHA Trendy Karyana & General Retail Management System
            </h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.title("💼 AHA Trendy Karyana & General Retail Management System")

st.sidebar.markdown(f"**👤 Current User:** `{st.session_state.user_role.upper()}`")

if st.sidebar.button("🔒 Log Out"):
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.rerun()

st.markdown("---")

if st.session_state.user_role == "Admin":
    menu = ["⚡ Quick Billing (POS)", "📦 Stock Management", "📒 Khata (Udhaar) System", "💸 Expense Tracker", "👥 Supplier Management", "📊 Sales Dashboard"]
else:
    menu = ["⚡ Quick Billing (POS)"]

choice = st.sidebar.selectbox("Menu Select Karen", menu)

def get_db_connection():
    return sqlite3.connect('karyana_streamlit.db')

# ==================== 1. QUICK BILLING (POS) ====================
if choice == "⚡ Quick Billing (POS)":
    st.header("⚡ Fast Billing Dashboard")
    
    conn = get_db_connection()
    df_items = pd.read_sql_query("SELECT * FROM inventory", conn)
    df_customers = pd.read_sql_query("SELECT * FROM khata", conn)
    conn.close()
    
    if df_items.empty:
        st.warning("⚠️ Pehle 'Stock Management' mein ja kar kuch items add karen!")
    else:
        if 'cart' not in st.session_state:
            st.session_state.cart = []
            
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Items Cart Mein Shamil Karen")
            item_selected = st.selectbox("Product Select Karen", df_items['item_name'].tolist())
            
            item_details = df_items[df_items['item_name'] == item_selected].iloc[0]
            current_available_stock = int(item_details['stock'])
            
            st.info(f"📊 **Available Stock:** {current_available_stock} units | **Price:** {item_details['price']} Rs")
            
            quantity = st.number_input("Quantity (Tadaad)", min_value=1, value=1)
            
            if st.button("🛒 Add to Cart"):
                existing_in_cart_qty = 0
                existing = next((i for i in st.session_state.cart if i['name'] == item_selected), None)
                if existing:
                    existing_in_cart_qty = existing['qty']
                
                total_requested_qty = existing_in_cart_qty + quantity
                
                if total_requested_qty > current_available_stock:
                    st.error(f"❌ **Order Fail!** Stock kam hai.")
                else:
                    if existing:
                        existing['qty'] += quantity
                    else:
                        st.session_state.cart.append({
                            "name": item_selected,
                            "price": item_details['price'],
                            "cost_price": item_details['cost_price'],
                            "qty": quantity
                        })
                    st.success(f"✓ {item_selected} x {quantity} cart mein add ho gaya!")
                    st.rerun()

            if st.session_state.cart:
                st.markdown("### 🛍️ Aap ka Cart")
                cart_df = pd.DataFrame(st.session_state.cart)
                cart_df['Total (Rs)'] = cart_df['price'] * cart_df['qty']
                st.table(cart_df[['name', 'price', 'qty', 'Total (Rs)']])
                
                total_amount = cart_df['Total (Rs)'].sum()
                st.metric(label="Total Bill (Rs)", value=f"{total_amount} Rs")
                
                if st.button("❌ Clear Cart"):
                    st.session_state.cart = []
                    st.rerun()
                    
        with col2:
            st.subheader("Checkout / Payment")
            payment_type = st.radio("Payment Mode", ["Cash (Naqd)", "Udhaar (Khata)"])
            
            selected_customer = ""
            if payment_type == "Udhaar (Khata)":
                if df_customers.empty:
                    st.error("Pehle 'Khata System' mein customer register karen!")
                else:
                    customer_options = {f"{row['name']} (Acc: {row['phone']})": row['name'] for idx, row in df_customers.iterrows()}
                    selected_option = st.selectbox("Customer Select Karen (Search by Name/Account)", list(customer_options.keys()))
                    selected_customer = customer_options[selected_option]
            
            if st.button("✅ Confirm & Print Bill"):
                if not st.session_state.cart:
                    st.error("Cart khali hai!")
                else:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    today_str = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                    
                    for prod in st.session_state.cart:
                        cursor.execute("UPDATE inventory SET stock = stock - ? WHERE item_name = ?", (prod['qty'], prod['name']))
                        
                        t_sale = prod['price'] * prod['qty']
                        t_cost = prod['cost_price'] * prod['qty']
                        profit = t_sale - t_cost
                        
                        cust_name_to_save = selected_customer if payment_type == "Udhaar (Khata)" else "Walk-in Customer"
                        
                        cursor.execute('''INSERT INTO sales (sale_date, item_name, quantity, total_sale, total_cost, profit, payment_mode, customer_name)
                                          VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', 
                                       (today_str, prod['name'], prod['qty'], t_sale, t_cost, profit, payment_type, cust_name_to_save))
                    
                    if payment_type == "Udhaar (Khata)" and selected_customer:
                        cursor.execute("UPDATE khata SET balance = balance + ? WHERE name = ?", (total_amount, selected_customer))
                    
                    conn.commit()
                    conn.close()
                    
                    st.balloons()
                    st.success(f"🎉 Bill Kamyabi se generate ho gaya!")
                    st.session_state.cart = []

# ==================== 2. STOCK MANAGEMENT ====================
elif choice == "📦 Stock Management" and st.session_state.user_role == "Admin":
    st.header("📦 Stock Control & Inventory Dashboard")
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Current Stock", "➕ Add New Item", "✏️ Modify Item", "🗑️ Delete Item"])
    
    with tab1:
        conn = get_db_connection()
        df_stock = pd.read_sql_query("SELECT item_name as 'Item Name', stock as 'Remaining Stock', cost_price as 'Kharid Qemat (Cost)', price as 'Retail Price (Rs)' FROM inventory", conn)
        conn.close()
        if df_stock.empty:
            st.info("Stock mein koi saaman nahi hai.")
        else:
            st.dataframe(df_stock, use_container_width=True)
            
    with tab2:
        st.subheader("Naya Item Shamil Karen")
        prod_name = st.text_input("Product Name").strip()
        prod_stock = st.number_input("Stock Quantity", min_value=0, value=10)
        prod_cost = st.number_input("Kharid Qemat (Rs)", min_value=0.0, value=40.0)
        prod_price = st.number_input("Retail Price (Rs)", min_value=0.0, value=50.0)
        
        if st.button("➕ Save Product"):
            if prod_name == "":
                st.error("Naam likhna zaroori hai!")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO inventory (item_name, stock, price, cost_price) VALUES (?, ?, ?, ?)", 
                                   (prod_name, prod_stock, prod_price, prod_cost))
                    conn.commit()
                    st.success("✓ Stock mein shamil ho gaya!")
                except sqlite3.IntegrityError:
                    st.error("⚠️ Pehle se majood hai.")
                finally:
                    conn.close()

    with tab3:
        st.subheader("Majooda Item Modify Karen")
        conn = get_db_connection()
        df_items_mod = pd.read_sql_query("SELECT * FROM inventory", conn)
        conn.close()
        if not df_items_mod.empty:
            mod_item_selected = st.selectbox("Kis item ko modify karna hai?", df_items_mod['item_name'].tolist(), key="mod_select")
            current_details = df_items_mod[df_items_mod['item_name'] == mod_item_selected].iloc[0]
            
            val_stock = max(0, int(current_details['stock']))
            val_cost = max(0.0, float(current_details['cost_price']))
            val_price = max(0.0, float(current_details['price']))
            
            new_name = st.text_input("New Product Name", value=current_details['item_name'])
            new_stock = st.number_input("Set Absolute Stock (Total Available)", min_value=0, value=val_stock)
            new_cost = st.number_input("New Cost Price (Rs)", min_value=0.0, value=val_cost)
            new_price = st.number_input("New Price (Rs)", min_value=0.0, value=val_price)
            
            if st.button("💾 Update Item Details"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE inventory SET item_name = ?, stock = ?, price = ?, cost_price = ? WHERE item_name = ?", 
                               (new_name, new_stock, new_price, new_cost, mod_item_selected))
                conn.commit()
                conn.close()
                st.success("✓ Records modify ho gaye!")
                st.rerun()

    with tab4:
        st.subheader("🗑️ Delete Item")
        conn = get_db_connection()
        df_items_del = pd.read_sql_query("SELECT * FROM inventory", conn)
        conn.close()
        if not df_items_del.empty:
            del_item_selected = st.selectbox("Kis item ko delete karna hai?", df_items_del['item_name'].tolist(), key="del_select")
            if st.button("🗑️ Confirm Delete"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM inventory WHERE item_name = ?", (del_item_selected,))
                conn.commit()
                conn.close()
                st.error(f"🗑️ {del_item_selected} ko nikal diya gaya.")
                st.rerun()

# ==================== 3. KHATA (UDHAAR) SYSTEM (UPDATED WITH MODIFY & DELETE) ====================
elif choice == "📒 Khata (Udhaar) System" and st.session_state.user_role == "Admin":
    st.header("📒 Khata Ledger (Udhaar Management)")
    
    # Paanch tabs bana diye hain taake Udhaar Wapsi, Modify aur Delete sab alag aur aasan ho jaye
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Customer Statement & Ledger", 
        "👤 Register New Customer", 
        "💰 Cash Received (Udhaar Wapsi)",
        "✏️ Modify Customer Details",
        "🗑️ Delete Customer Account"
    ])
    
    conn = get_db_connection()
    df_khata = pd.read_sql_query("SELECT customer_id, name as 'Name', phone as 'Account Number (Mobile)', balance as 'Pending Udhaar (Rs)' FROM khata", conn)
    df_all_sales = pd.read_sql_query("SELECT * FROM sales WHERE customer_name != 'Walk-in Customer'", conn)
    conn.close()
    
    # 3.1 CUSTOMER STATEMENT & LEDGER
    with tab1:
        if df_khata.empty:
            st.info("Abhi tak koi khata account nahi bana.")
        else:
            st.subheader("Summary Ledger")
            st.dataframe(df_khata.drop(columns=['customer_id']), use_container_width=True)
            
            st.markdown("---")
            st.subheader("🔍 Customer Search (Naam ya Account Number se search karen)")
            
            search_options = {f"{row['Name']} (Account Number: {row['Account Number (Mobile)']})": row['Name'] for idx, row in df_khata.iterrows()}
            selected_ledger_option = st.selectbox("Customer Select Karen:", list(search_options.keys()), key="ledger_search_select")
            selected_ledger_cust = search_options[selected_ledger_option]
            
            customer_ledger = df_all_sales[df_all_sales['customer_name'] == selected_ledger_cust].copy()
            current_bal = df_khata[df_khata['Name'] == selected_ledger_cust]['Pending Udhaar (Rs)'].values[0]
            cust_acc_num = df_khata[df_khata['Name'] == selected_ledger_cust]['Account Number (Mobile)'].values[0]
            
            st.metric(label=f"⚠️ {selected_ledger_cust} (Account: {cust_acc_num}) Ka Total Pending Udhaar Balance", value=f"{current_bal:,.2f} Rs")
            
            if customer_ledger.empty:
                st.info(f"ℹ️ {selected_ledger_cust} ka koi detailed record nahi hai.")
            else:
                display_ledger = customer_ledger[['sale_date', 'item_name', 'quantity', 'total_sale', 'payment_mode']].copy()
                display_ledger['total_sale'] = display_ledger['total_sale'].apply(lambda x: abs(x))
                display_ledger.columns = ['📅 Date & Time', '📦 Product / Transaction', '🔢 Qty', '💰 Amount (Rs)', '💳 Type']
                
                st.dataframe(display_ledger.sort_values(by='📅 Date & Time', ascending=False), use_container_width=True)
                
                if st.button("🖨️ Print / Save Ledger As PDF", key="print_ledger"):
                    html_rows = "".join([f"<tr><td>{row['📅 Date & Time']}</td><td>{row['📦 Product / Transaction']}</td><td>{row['🔢 Qty']}</td><td>{row['💰 Amount (Rs)']} Rs</td><td>{row['💳 Type']}</td></tr>" for idx, row in display_ledger.iterrows()])
                    
                    html_content = f"""
                        <div class='header'>
                            <h2>AHA TRENDY KARYANA STORE</h2>
                            <p>TariqAbad, Faisalabad, Pakistan</p>
                            <h3>CUSTOMER STATEMENT / UDHAAR LEDGER</h3>
                        </div>
                        <p><strong>Customer Name:</strong> {selected_ledger_cust}</p>
                        <p><strong>Account Number (Mobile):</strong> {cust_acc_num}</p>
                        <p><strong>Statement Date:</strong> {datetime.now().strftime('%Y-%m-%d %I:%M %p')}</p>
                        <hr/>
                        <table>
                            <thead>
                                <tr><th>Date & Time</th><th>Product / Transaction</th><th>Qty</th><th>Amount</th><th>Type</th></tr>
                            </thead>
                            <tbody>
                                {html_rows}
                            </tbody>
                        </table>
                        <h3 style='text-align: right; margin-top: 20px;'>Total Remaining Balance: {current_bal:,.2f} Rs</h3>
                        <div class='footer'><p>Thank you for your business! Software Generated Statement.</p></div>
                    """
                    trigger_print(html_content)
            
    # 3.2 REGISTER NEW CUSTOMER
    with tab2:
        st.subheader("👤 Naya Customer Register Karen")
        c_name = st.text_input("Customer Name").strip()
        c_phone = st.text_input("Mobile Number (Yeh hi Account Number Banega)").strip()
        
        if st.button("📝 Register Customer"):
            if c_name == "" or c_phone == "":
                st.error("Customer ka naam aur Mobile Number (Account Number) dono likhna zaroori hai.")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute("SELECT name FROM khata WHERE LOWER(name) = LOWER(?)", (c_name,))
                existing_user = cursor.fetchone()
                
                cursor.execute("SELECT phone FROM khata WHERE phone = ?", (c_phone,))
                existing_phone = cursor.fetchone()
                
                if existing_user:
                    st.error(f"⚠️ Yeh naam ('{c_name}') pehle se registered hai! Duplicate account nahi ban sakta.")
                    conn.close()
                elif existing_phone:
                    st.error(f"⚠️ Yeh Mobile Number / Account Number ('{c_phone}') pehle se majood hai!")
                    conn.close()
                else:
                    try:
                        cursor.execute("INSERT INTO khata (name, phone) VALUES (?, ?)", (c_name, c_phone))
                        conn.commit()
                        st.success(f"🎉 Kamyabi Se Register Ho Gaya! \n\n**Naam:** {c_name} \n**Account Number:** {c_phone}")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("⚠️ Database Error: Naam ya Mobile Number pehle se majood hai.")
                    finally:
                        conn.close()
                        
    # 3.3 CASH RECEIVED (UDHAAR WAPSI)
    with tab3:
        st.subheader("💰 Cash Received (Udhaar Wapsi Summary)")
        
        if "khata_success_msg" in st.session_state:
            st.success(st.session_state.khata_success_msg)
            del st.session_state.khata_success_msg
            
        if df_khata.empty:
            st.info("Pehle customer register karen.")
        else:
            cash_back_options = {f"{row['Name']} (Acc: {row['Account Number (Mobile)']})": row['Name'] for idx, row in df_khata.iterrows()}
            selected_cash_option = st.selectbox("Kis customer ne paise wapas kiye?", list(cash_back_options.keys()), key="cash_back_cust")
            cust_select = cash_back_options[selected_cash_option]
            
            amount_paid = st.number_input("Wapas kiye gaye paise (Rs)", min_value=1.0, value=10.0, step=10.0)
            
            if st.button("💵 Update Khata Balance"):
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute("UPDATE khata SET balance = balance - ? WHERE name = ?", (amount_paid, cust_select))
                
                today_str = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                cursor.execute('''INSERT INTO sales (sale_date, item_name, quantity, total_sale, total_cost, profit, payment_mode, customer_name)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', 
                               (today_str, "Cash Received (Udhaar Wapsi)", 1, amount_paid, 0.0, 0.0, "Cash Received", cust_select))
                
                conn.commit()
                conn.close()
                
                st.session_state.khata_success_msg = f"🎉 Successfully Updated! {cust_select} ke khate se {amount_paid:,.2f} Rs received entry save ho gayi hai."
                st.rerun()

    # 3.4 MODIFY CUSTOMER DETAILS
    with tab4:
        st.subheader("✏️ Customer Profile / Balance Modify Karen")
        if df_khata.empty:
            st.info("Modify karne ke liye koi customer profile majood nahi hai.")
        else:
            mod_cust_options = {f"{row['Name']} (Acc: {row['Account Number (Mobile)']}) - Bal: {row['Pending Udhaar (Rs)']} Rs": row['customer_id'] for idx, row in df_khata.iterrows()}
            selected_mod_label = st.selectbox("Kis customer ki details tabdeel karni hain?", list(mod_cust_options.keys()), key="khata_mod_select")
            target_cust_id = mod_cust_options[selected_mod_label]
            
            current_cust_data = df_khata[df_khata['customer_id'] == target_cust_id].iloc[0]
            
            new_cust_name = st.text_input("Naya Name Darj Karen", value=current_cust_data['Name'], key="khata_new_name")
            new_cust_phone = st.text_input("Naya Account/Mobile Number", value=current_cust_data['Account Number (Mobile)'], key="khata_new_phone")
            new_cust_balance = st.number_input("Udhaar Balance Direct Tabdeel Karen (Rs)", value=float(current_cust_data['Pending Udhaar (Rs)']), key="khata_new_bal")
            
            if st.button("💾 Update Customer Profile"):
                if new_cust_name.strip() == "" or new_cust_phone.strip() == "":
                    st.error("Naam aur Phone number khali nahi chor sakte!")
                else:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("""UPDATE khata 
                                          SET name = ?, phone = ?, balance = ? 
                                          WHERE customer_id = ?""", 
                                       (new_cust_name.strip(), new_cust_phone.strip(), new_cust_balance, target_cust_id))
                        conn.commit()
                        st.session_state.khata_success_msg = "✓ Customer details kamyabi se update ho gayi hain!"
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("⚠️ Error: Yeh Naam ya Mobile Number pehle se kisi aur customer ke paas register hai.")
                    finally:
                        conn.close()

    # 3.5 DELETE CUSTOMER ACCOUNT
    with tab5:
        st.subheader("🗑️ Customer Khata Account Hamesha Ke Liye Delete Karen")
        if df_khata.empty:
            st.info("Delete karne ke liye koi account majood nahi hai.")
        else:
            del_cust_options = {f"{row['Name']} (Acc: {row['Account Number (Mobile)']}) - Balance: {row['Pending Udhaar (Rs)']} Rs": row['customer_id'] for idx, row in df_khata.iterrows()}
            selected_del_label = st.selectbox("Kis customer ka account delete karna hai?", list(del_cust_options.keys()), key="khata_del_select")
            target_del_id = del_cust_options[selected_del_label]
            
            st.warning("⚠️ Warning: Account delete karne se customer ka naam aur balance khata list se saaf ho jayega. (Sales record barkrar rahega)")
            if st.button("🗑️ Confirm Delete Customer Khata"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM khata WHERE customer_id = ?", (target_del_id,))
                conn.commit()
                conn.close()
                st.session_state.khata_success_msg = "🗑️ Customer account ledger se kamyabi se delete kar diya gaya hai."
                st.rerun()

# ==================== 4. EXPENSE TRACKER ====================
elif choice == "💸 Expense Tracker" and st.session_state.user_role == "Admin":
    st.header("💸 Dukan Ke Rozana Ke Kharche (Expense Tracker)")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Naya Kharcha Add Karen", 
        "📋 Kharche Ki List (Logs)", 
        "✏️ Modify Expense", 
        "🗑️ Delete Expense"
    ])
    
    if "expense_success_msg" in st.session_state:
        st.success(st.session_state.expense_success_msg)
        del st.session_state.expense_success_msg

    # 4.1 ADD EXPENSE
    with tab1:
        st.subheader("Kharche Ki Tafseel Darj Karen")
        exp_category = st.selectbox("Kharche Ki Category Select Karen", [
            "Bijli Ka Bill (Electricity)", 
            "Dukan Ka Kiraya (Rent)", 
            "Dukan Ke Ladke Ki Salary", 
            "Chai / Mehman Nawazi / Snacks", 
            "Dukan Ka Mutafariq Saman / Stationary",
            "Other (Koi Aur Kharcha)"
        ], key="add_exp_cat")
        exp_amount = st.number_input("Kharche Ki Rakam (Amount in Rs)", min_value=1.0, value=50.0, step=10.0, key="add_exp_amt")
        exp_details = st.text_area("Kharcha Kis Cheez Par Hua? (Details/Remarks)", key="add_exp_det").strip()
        
        if st.button("💾 Save Expense Record"):
            conn = get_db_connection()
            cursor = conn.cursor()
            
            today_date_str = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            cursor.execute("INSERT INTO expenses (expense_date, category, amount, details) VALUES (?, ?, ?, ?)",
                           (today_date_str, exp_category, exp_amount, exp_details))
            
            conn.commit()
            conn.close()
            
            st.session_state.expense_success_msg = f"🎉 Successfully Updated! {exp_category} ka {exp_amount:,.2f} Rs ka kharcha record ho gaya hai."
            st.rerun()
            
    # 4.2 EXPENSE LIST / LOGS
    with tab2:
        st.subheader("📋 Tamam Kharche")
        conn = get_db_connection()
        df_exp_list = pd.read_sql_query("SELECT expense_id, expense_date as '📅 Date & Time', category as '📁 Category', amount as '💰 Amount (Rs)', details as '📝 Details' FROM expenses ORDER BY expense_id DESC", conn)
        conn.close()
        
        if df_exp_list.empty:
            st.info("Abhi tak koi kharcha record nahi kiya gaya.")
        else:
            total_exp_all_time = df_exp_list['💰 Amount (Rs)'].sum()
            st.metric(label="📊 Kul Total Kharche (All Time)", value=f"{total_exp_all_time:,.2f} Rs")
            st.dataframe(df_exp_list.drop(columns=['expense_id']), use_container_width=True)

    # 4.3 MODIFY EXPENSE
    with tab3:
        st.subheader("✏️ Kharcha Modify / Tabdeel Karen")
        conn = get_db_connection()
        df_mod_exp = pd.read_sql_query("SELECT * FROM expenses ORDER BY expense_id DESC", conn)
        conn.close()
        
        if df_mod_exp.empty:
            st.info("Modify karne ke liye koi kharcha majood nahi hai.")
        else:
            exp_options = {f"ID {row['expense_id']} | {row['category']} ({row['amount']} Rs) - {row['expense_date']}": row['expense_id'] for idx, row in df_mod_exp.iterrows()}
            selected_exp_label = st.selectbox("Kis kharche ko modify karna hai?", list(exp_options.keys()), key="mod_exp_select")
            target_exp_id = exp_options[selected_exp_label]
            
            current_exp_data = df_mod_exp[df_mod_exp['expense_id'] == target_exp_id].iloc[0]
            
            categories_list = [
                "Bijli Ka Bill (Electricity)", "Dukan Ka Kiraya (Rent)", 
                "Dukan Ke Ladke Ki Salary", "Chai / Mehman Nawazi / Snacks", 
                "Dukan Ka Mutafariq Saman / Stationary", "Other (Koi Aur Kharcha)"
            ]
            
            if current_exp_data['category'] in categories_list:
                cat_index = categories_list.index(current_exp_data['category'])
            else:
                cat_index = 0
                
            mod_category = st.selectbox("Category Tabdeel Karen", categories_list, index=cat_index, key="mod_exp_cat")
            mod_amount = st.number_input("Rakam Tabdeel Karen (Rs)", min_value=1.0, value=float(current_exp_data['amount']), key="mod_exp_amt")
            mod_details = st.text_area("Details Tabdeel Karen", value=current_exp_data['details'], key="mod_exp_det").strip()
            
            if st.button("💾 Update Expense Details"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""UPDATE expenses 
                                  SET category = ?, amount = ?, details = ? 
                                  WHERE expense_id = ?""", 
                               (mod_category, mod_amount, mod_details, target_exp_id))
                conn.commit()
                conn.close()
                st.session_state.expense_success_msg = "✓ Kharcha kamyabi se update kar diya gaya hai!"
                st.rerun()

    # 4.4 DELETE EXPENSE
    with tab4:
        st.subheader("🗑️ Kharcha Delete / Remove Karen")
        conn = get_db_connection()
        df_del_exp = pd.read_sql_query("SELECT * FROM expenses ORDER BY expense_id DESC", conn)
        conn.close()
        
        if df_del_exp.empty:
            st.info("Delete karne ke liye koi kharcha majood nahi hai.")
        else:
            del_options = {f"ID {row['expense_id']} | {row['category']} ({row['amount']} Rs) - {row['expense_date']}": row['expense_id'] for idx, row in df_del_exp.iterrows()}
            selected_del_label = st.selectbox("Kis kharche ko delete karna hai?", list(del_options.keys()), key="del_exp_select")
            target_del_id = del_options[selected_del_label]
            
            st.warning(f"⚠️ Kya aap waqai is expense record ko hamesha ke liye delete karna chahte hain?")
            if st.button("🗑️ Confirm Delete Expense"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (target_del_id,))
                conn.commit()
                conn.close()
                st.session_state.expense_success_msg = "🗑️ Expense record ko kamyabi se delete kar diya gaya hai."
                st.rerun()

# ==================== 5. SUPPLIER MANAGEMENT ====================
elif choice == "👥 Supplier Management" and st.session_state.user_role == "Admin":
    st.header("👥 Supplier / Wholesaler Management")
    
    tab_sup1, tab_sup2, tab_sup3, tab_sup4, tab_sup5 = st.tabs([
        "👥 Supplier Register & Summary", 
        "✏️ Modify Supplier", 
        "🗑️ Delete Supplier", 
        "📦 Purchase / Stock Inward", 
        "💰 Paid to Supplier"
    ])
    
    if "sup_success_msg" in st.session_state:
        st.success(st.session_state.sup_success_msg)
        del st.session_state.sup_success_msg
        
    conn = get_db_connection()
    df_sups = pd.read_sql_query("SELECT supplier_id, name as 'Supplier Name', phone as 'Mobile / Account', company as 'Company/Wholesale Shop', balance as 'Our Payable Balance (Rs)' FROM suppliers", conn)
    df_inv_list = pd.read_sql_query("SELECT item_name FROM inventory", conn)
    conn.close()
    
    with tab_sup1:
        st.subheader("👤 Naya Supplier Register Karen")
        col_s1, col_s2, col_s3 = st.columns(3)
        s_name = col_s1.text_input("Supplier Name (Contact Person)").strip()
        s_phone = col_s2.text_input("Mobile / Account Number").strip()
        s_company = col_s3.text_input("Company / Shop Name (e.g., ABC Wholesale)").strip()
        
        if st.button("📝 Register Supplier Account"):
            if s_name == "" or s_phone == "":
                st.error("Supplier Name aur Mobile Number dono likhna zaroori hain!")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO suppliers (name, phone, company, balance) VALUES (?, ?, ?, 0.0)", (s_name, s_phone, s_company))
                    conn.commit()
                    st.session_state.sup_success_msg = f"🎉 Supplier '{s_name} ({s_company})' kamyabi se register ho gaya!"
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("⚠️ Yeh Supplier Name ya Mobile Number pehle se database mein majood hai!")
                finally:
                    conn.close()
                    
        st.markdown("---")
        st.subheader("📊 Registered Suppliers List")
        if df_sups.empty:
            st.info("Abhi tak koi wholesale supplier register nahi kiya gaya.")
        else:
            st.dataframe(df_sups[['Supplier Name', 'Mobile / Account', 'Company/Wholesale Shop', 'Our Payable Balance (Rs)']], use_container_width=True)
            
    with tab_sup2:
        st.subheader("✏️ Supplier Ki Details Tabdeel/Modify Karen")
        if df_sups.empty:
            st.info("Koi supplier majood nahi hai jise modify kiya ja sakay.")
        else:
            mod_sup_options = {f"{row['Supplier Name']} ({row['Company/Wholesale Shop']})": row['Supplier Name'] for idx, row in df_sups.iterrows()}
            selected_mod_sup = st.selectbox("Kis Supplier ki details change karni hain?", list(mod_sup_options.keys()), key="sup_mod_sel")
            target_sup_name = mod_sup_options[selected_mod_sup]
            
            current_sup_row = df_sups[df_sups['Supplier Name'] == target_sup_name].iloc[0]
            
            new_sup_name = st.text_input("Edit Supplier Name", value=current_sup_row['Supplier Name'])
            new_sup_phone = st.text_input("Edit Mobile / Account Number", value=current_sup_row['Mobile / Account'])
            new_sup_company = st.text_input("Edit Company / Wholesale Shop", value=current_sup_row['Company/Wholesale Shop'])
            new_sup_balance = st.number_input("Edit Current Outstanding Balance (Rs)", value=float(current_sup_row['Our Payable Balance (Rs)']), min_value=0.0)
            
            if st.button("💾 Update Supplier Records"):
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""UPDATE suppliers 
                                      SET name = ?, phone = ?, company = ?, balance = ? 
                                      WHERE supplier_id = ?""", 
                                   (new_sup_name, new_sup_phone, new_sup_company, new_sup_balance, int(current_sup_row['supplier_id'])))
                    conn.commit()
                    st.session_state.sup_success_msg = f"✓ Supplier '{new_sup_name}' ka record update ho gaya!"
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("❌ Integrity Error: Yeh updated details kisi aur account se match kar rahi hain.")
                finally:
                    conn.close()

    with tab_sup3:
        st.subheader("🗑️ Delete Supplier Account")
        if df_sups.empty:
            st.info("Account clear hai. Koi supplier records majood nahi.")
        else:
            del_sup_options = {f"{row['Supplier Name']} ({row['Company/Wholesale Shop']}) Balance: {row['Our Payable Balance (Rs)']} Rs": row['Supplier Name'] for idx, row in df_sups.iterrows()}
            selected_del_sup = st.selectbox("Kis supplier ko system se delete karna hai?", list(del_sup_options.keys()), key="sup_del_sel")
            target_del_name = del_sup_options[selected_del_sup]
            
            st.warning(f"⚠️ Kya aap waqai '{target_del_name}' ko delete karna chahte hain? Iska ledger data saaf ho jayega.")
            if st.button("🗑️ Confirm Delete Supplier Account"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM suppliers WHERE name = ?", (target_del_name,))
                conn.commit()
                conn.close()
                st.session_state.sup_success_msg = f"🗑️ Supplier '{target_del_name}' ko kamyabi se remove kar diya gaya."
                st.rerun()

    with tab_sup4:
        st.subheader("📦 Purchase / Wholesale Item Se Stock Inward")
        if df_sups.empty:
            st.error("Pehle aik supplier register karen.")
        elif df_inv_list.empty:
            st.error("Pehle 'Stock Management' mein ja kar item create karen.")
        else:
            col_p1, col_p2 = st.columns(2)
            sup_selection_options = {f"{row['Supplier Name']} ({row['Company/Wholesale Shop']})": row['Supplier Name'] for idx, row in df_sups.iterrows()}
            chosen_sup = col_p1.selectbox("Supplier Select Karen", list(sup_selection_options.keys()), key="purchase_sup_select")
            chosen_sup_raw_name = sup_selection_options[chosen_sup]
            
            chosen_item = col_p2.selectbox("Item Select Karen Jiska Stock Aaya Hai", df_inv_list['item_name'].tolist())
            
            col_p3, col_p4 = st.columns(2)
            added_qty = col_p3.number_input("Kitni Quantity Aayi Hai?", min_value=1, value=50)
            wholesale_cost = col_p4.number_input("Per Unit Kharid Cost Qemat (Rs)", min_value=0.0, value=20.0)
            
            total_bill_payable = added_qty * wholesale_cost
            st.markdown(f"### 💸 Total Bill Formed: **{total_bill_payable:,.2f} Rs**")
            
            purchase_payment_mode = st.radio("Is Inward Invoice Ki Payment Kaise Ki?", ["Udhaar Par Liya (Payable Balance Mein Add Ho)", "Cash / Direct Paid (No Khata Entry)"])
            
            if st.button("📥 Record Stock Inward & Bill"):
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute("UPDATE inventory SET stock = stock + ?, cost_price = ? WHERE item_name = ?", (added_qty, wholesale_cost, chosen_item))
                
                if purchase_payment_mode == "Udhaar Par Liya (Payable Balance Mein Add Ho)":
                    cursor.execute("UPDATE suppliers SET balance = balance + ? WHERE name = ?", (total_bill_payable, chosen_sup_raw_name))
                    st.session_state.sup_success_msg = f"🎉 Stock Inward Saved! Total {added_qty} units of '{chosen_item}' added. {total_bill_payable:,.2f} Rs added to {chosen_sup_raw_name}'s ledger account balance."
                else:
                    st.session_state.sup_success_msg = f"🎉 Paid Stock Inward Saved! Total {added_qty} units of '{chosen_item}' updated directly via Cash."
                    
                conn.commit()
                conn.close()
                st.rerun()

    with tab_sup5:
        st.subheader("💰 Supplier Ko Udhaar Wapsi / Payment Entry")
        if df_sups.empty:
            st.info("Koi supplier register nahi hai.")
        else:
            pay_sup_options = {f"{row['Supplier Name']} ({row['Company/Wholesale Shop']}) Pending: {row['Our Payable Balance (Rs)']} Rs": row['Supplier Name'] for idx, row in df_sups.iterrows()}
            selected_pay_sup = st.selectbox("Kis Supplier ko cash payment di hai?", list(pay_sup_options.keys()), key="sup_pay_sel")
            target_pay_name = pay_sup_options[selected_pay_sup]
            
            amount_paid_to_sup = st.number_input("Kitne paise paid kiye? (Rs)", min_value=1.0, value=100.0, step=50.0)
            
            if st.button("💵 Save Payment Entry"):
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute("UPDATE suppliers SET balance = balance - ? WHERE name = ?", (amount_paid_to_sup, target_pay_name))
                
                today_date_str = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                cursor.execute("INSERT INTO expenses (expense_date, category, amount, details) VALUES (?, ?, ?, ?)",
                               (today_date_str, "Supplier Payment / Wholesale Clearing", amount_paid_to_sup, f"Paid to Supplier: {target_pay_name}"))
                               
                conn.commit()
                conn.close()
                st.session_state.sup_success_msg = f"🎉 Entry Recorded! Paid {amount_paid_to_sup:,.2f} Rs to '{target_pay_name}'. Updated balances and synched expenses tracker logs."
                st.rerun()

# ==================== 6. SALES DASHBOARD ====================
elif choice == "📊 Sales Dashboard" and st.session_state.user_role == "Admin":
    st.header("📊 Sales Report & Profit Analysis")
    
    conn = get_db_connection()
    df_sales = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    
    if df_sales.empty:
        st.info("Abhi tak koi sale record nahi hui.")
    else:
        df_sales['total_sale'] = df_sales['total_sale'].astype(float)
        df_sales['profit'] = df_sales['profit'].astype(float)
        
        col1, col2, col3 = st.columns(3)
        
        gross_sales = df_sales[df_sales['item_name'] != "Cash Received (Udhaar Wapsi)"]['total_sale'].sum()
        total_profit = df_sales['profit'].sum()
        cash_received_khata = df_sales[df_sales['payment_mode'] == "Cash Received"]['total_sale'].sum()
        
        col1.metric("🛒 Kul Sales Gross (Revenue)", f"{gross_sales:,.2f} Rs")
        col2.metric("📈 Net Profit (Munafa)", f"{total_profit:,.2f} Rs")
        col3.metric("💰 Recovered Cash (Udhaar Wapsi)", f"{cash_received_khata:,.2f} Rs")
        
        st.markdown("---")
        st.subheader("📋 Transactions Log List")
        
        display_sales = df_sales[['sale_date', 'item_name', 'quantity', 'total_sale', 'profit', 'payment_mode', 'customer_name']].copy()
        display_sales.columns = ['📅 Date & Time', '📦 Product Name', '🔢 Qty', '💰 Sale Total (Rs)', '📈 Earned Profit', '💳 Mode', '👤 Customer Name']
        
        st.dataframe(display_sales.sort_values(by='📅 Date & Time', ascending=False), use_container_width=True)
