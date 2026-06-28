import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

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
                        
    # Khata Table (Phone/Account Number unique kiya gaya hai)
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
                        
    conn.commit()
    conn.close()

init_db()

# Main App Layout Configuration
st.set_page_config(page_title="AHA Trendy Karyana", layout="wide")

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

# ==================== LOGIN SYSTEM ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

if not st.session_state.logged_in:
    st.title("🔐 Karyana App - System Login")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username (User ID)")
        password = st.text_input("Password", type="password")
        
        if st.button("🚪 Log In"):
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
    st.stop()

# ==================== MAIN DASHBOARD ====================
st.title("🛒 Karyana & General Retail Management System")
st.sidebar.markdown(f"**👤 Current User:** `{st.session_state.user_role.upper()}`")

if st.sidebar.button("🔒 Log Out"):
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.rerun()

st.markdown("---")

if st.session_state.user_role == "Admin":
    menu = ["⚡ Quick Billing (POS)", "📦 Stock Management", "📒 Khata (Udhaar) System", "💸 Expense Tracker", "📊 Sales Dashboard"]
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
            
            quantity = st.number_input("Quantity (Tadaad)", min_value=1, value=10)
            
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
                    # Dropdown mein search asan karne ke liye Account Number aur Naam sath dikhaye hain
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
        prod_stock = st.number_input("Stock Quantity", min_value=1, value=10)
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
            new_name = st.text_input("New Product Name", value=current_details['item_name'])
            new_stock = st.number_input("Set Absolute Stock", min_value=0, value=int(current_details['stock']))
            new_cost = st.number_input("New Cost Price (Rs)", min_value=0.0, value=float(current_details['cost_price']))
            new_price = st.number_input("New Retail Price (Rs)", min_value=0.0, value=float(current_details['price']))
            
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
        st.subheader("❌ Delete Item")
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

# ==================== 3. KHATA (UDHAAR) SYSTEM ====================
elif choice == "📒 Khata (Udhaar) System" and st.session_state.user_role == "Admin":
    st.header("📒 Khata Ledger (Udhaar Management)")
    tab1, tab2, tab3 = st.tabs(["👥 Customer Statement & Ledger", "👤 Register New Customer", "💰 Cash Received (Udhaar Wapsi)"])
    
    conn = get_db_connection()
    df_khata = pd.read_sql_query("SELECT name as 'Name', phone as 'Account Number (Mobile)', balance as 'Pending Udhaar (Rs)' FROM khata", conn)
    df_all_sales = pd.read_sql_query("SELECT * FROM sales WHERE customer_name != 'Walk-in Customer'", conn)
    conn.close()
    
    with tab1:
        if df_khata.empty:
            st.info("Abhi tak koi khata account nahi bana.")
        else:
            st.subheader("Summary Ledger")
            st.dataframe(df_khata, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🔍 Customer Search (Naam ya Account Number se search karen)")
            
            # Dropdown options mein Naam aur Account Number dono show kiya hai search asani ke liye
            search_options = {f"{row['Name']} (Account Number: {row['Account Number (Mobile)']})": row['Name'] for idx, row in df_khata.iterrows()}
            selected_ledger_option = st.selectbox("Customer Select Karen:", list(search_options.keys()))
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
                
                # Check for duplicate customer name (Case-insensitive)
                cursor.execute("SELECT name FROM khata WHERE LOWER(name) = LOWER(?)", (c_name,))
                existing_user = cursor.fetchone()
                
                # Check for duplicate phone/account number
                cursor.execute("SELECT phone FROM khata WHERE phone = ?", (c_phone,))
                existing_phone = cursor.fetchone()
                
                if existing_user:
                    st.error(f"⚠️ Yeh naam ('{c_name}') pehle se registered hai! Duplicate account nahi ban sakta.")
                    conn.close()
                elif existing_phone:
                    st.error(f"⚠️ Yeh Mobile Number / Account Number ('{c_phone}') pehle se majood hai! Aik number par do account nahi ban sakte.")
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

# ==================== 4. EXPIENSE TRACKER ====================
elif choice == "💸 Expense Tracker" and st.session_state.user_role == "Admin":
    st.header("💸 Dukan Ke Rozana Ke Kharche (Expense Tracker)")
    
    tab1, tab2 = st.tabs(["➕ Naya Kharcha Add Karen", "📋 Kharche Ki List (Logs)"])
    
    if "expense_success_msg" in st.session_state:
        st.success(st.session_state.expense_success_msg)
        del st.session_state.expense_success_msg

    with tab1:
        st.subheader("Kharche Ki Tafseel Darj Karen")
        exp_category = st.selectbox("Kharche Ki Category Select Karen", [
            "Bijli Ka Bill (Electricity)", 
            "Dukan Ka Kiraya (Rent)", 
            "Dukan Ke Ladke Ki Salary", 
            "Chai / Mehman Nawazi / Snacks", 
            "Dukan Ka Mutafariq Saman / Stationary",
            "Other (Koi Aur Kharcha)"
        ])
        exp_amount = st.number_input("Kharche Ki Rakam (Amount in Rs)", min_value=1.0, value=50.0, step=10.0)
        exp_details = st.text_area("Kharcha Kis Cheez Par Hua? (Details/Remarks)").strip()
        
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
            
    with tab2:
        st.subheader("📋 Tamam Kharche")
        conn = get_db_connection()
        df_exp_list = pd.read_sql_query("SELECT expense_date as '📅 Date & Time', category as '📁 Category', amount as '💰 Amount (Rs)', details as '📝 Details' FROM expenses ORDER BY expense_id DESC", conn)
        conn.close()
        
        if df_exp_list.empty:
            st.info("Abhi tak koi kharcha record nahi kiya gaya.")
        else:
            total_exp_all_time = df_exp_list['💰 Amount (Rs)'].sum()
            st.metric(label="📊 Kul Total Kharche (All Time)", value=f"{total_exp_all_time:,.2f} Rs")
            st.dataframe(df_exp_list, use_container_width=True)

# ==================== 5. SALES DASHBOARD ====================
elif choice == "📊 Sales Dashboard" and st.session_state.user_role == "Admin":
    st.header("📊 Sales & Profit Analysis Dashboard")
    
    conn = get_db_connection()
    df_sales = pd.read_sql_query("SELECT * FROM sales", conn)
    df_expenses = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    
    if df_sales.empty:
        st.info("📊 Abhi tak koi sale record nahi hui.")
    else:
        df_sales['clean_date'] = df_sales['sale_date'].apply(lambda x: x.split(" ")[0])
        if not df_expenses.empty:
            df_expenses['clean_date'] = df_expenses['expense_date'].apply(lambda x: x.split(" ")[0])
        else:
            df_expenses['clean_date'] = pd.Series(dtype='str')
        
        st.subheader("🔍 Filter Reports")
        selected_date = st.date_input("Tareekh select karen", datetime.now().date())
        selected_date_str = selected_date.strftime("%Y-%m-%d")
        
        filtered_df = df_sales[df_sales['clean_date'] == selected_date_str]
        filtered_exp = df_expenses[df_expenses['clean_date'] == selected_date_str] if not df_expenses.empty else pd.DataFrame()
        
        if filtered_df.empty and (filtered_exp.empty or filtered_exp.empty):
            st.warning(f"⚠️ Selected Tareekh ({selected_date_str}) par na koi sale hui hai aur na koi kharcha.")
        else:
            st.markdown("### 📈 Summary Metrics")
            m1, m2, m3, m4 = st.columns(4)
            
            actual_sales_df = filtered_df[filtered_df['payment_mode'] != "Cash Received"]
            wapsi_df = filtered_df[filtered_df['payment_mode'] == "Cash Received"]
            
            total_sales_val = actual_sales_df['total_sale'].sum()
            gross_profit_val = actual_sales_df['profit'].sum()
            cash_sales = actual_sales_df[actual_sales_df['payment_mode'] == "Cash (Naqd)"]['total_sale'].sum()
            udhaar_sales = actual_sales_df[actual_sales_df['payment_mode'] == "Udhaar (Khata)"]['total_sale'].sum()
            total_wapsi_collection = wapsi_df['total_sale'].sum()
            
            day_expenses_total = filtered_exp['amount'].sum() if not filtered_exp.empty else 0.0
            net_profit_val = gross_profit_val - day_expenses_total
            
            m1.metric(label="💰 Total Sales (New Bills)", value=f"{total_sales_val:,.2f} Rs")
            m2.metric(label="💸 Day Total Expenses (🔴 Minus)", value=f"{day_expenses_total:,.2f} Rs")
            m3.metric(label="💚 Pure Net Profit (Kharche Nikal Kar)", value=f"{net_profit_val:,.2f} Rs")
            m4.metric(label="💰 Recovered Cash (Udhaar Wapsi)", value=f"{total_wapsi_collection:,.2f} Rs")
            
            st.markdown("---")
            
            col_sales, col_exp = st.columns([2, 1])
            
            with col_sales:
                st.subheader("📋 Day Sales Log Table")
                log_df = filtered_df[['sale_date', 'item_name', 'quantity', 'total_sale', 'profit', 'payment_mode', 'customer_name']].copy()
                log_df.columns = ['📅 Date & Time', '📦 Item / Action', '🔢 Qty', '💰 Amount', '💚 Net Profit', '💳 Mode', '👤 Customer']
                st.dataframe(log_df, use_container_width=True)
                
            with col_exp:
                st.subheader("📉 Day Expenses Log Table")
                if filtered_exp.empty:
                    st.info("Is tareekh ka koi kharcha nahi hai.")
                else:
                    show_exp_df = filtered_exp[['expense_date', 'category', 'amount']].copy()
                    show_exp_df.columns = ['📅 Date & Time', '📁 Category', '💰 Amount']
                    st.dataframe(show_exp_df, use_container_width=True)
            
            if st.button("🖨️ Print / Save Daily Sales & Expense Summary As PDF", key="print_daily_sales"):
                html_rows = "".join([f"<tr><td>{row['📅 Date & Time']}</td><td>{row['📦 Item / Action']}</td><td>{row['🔢 Qty']}</td><td>{row['💰 Amount']} Rs</td><td>{row['💚 Net Profit']} Rs</td><td>{row['💳 Mode']}</td></tr>" for idx, row in log_df.iterrows()])
                
                html_content = f"""
                    <div class='header'>
                        <h2>AHA TRENDY KARYANA STORE</h2>
                        <p>TariqAbad, Faisalabad, Pakistan</p>
                        <h3>DAILY SALES & EXPENSE STATEMENT</h3>
                    </div>
                    <p><strong>Report Date:</strong> {selected_date_str}</p>
                    <hr/>
                    <div style='margin-bottom: 20px;'>
                        <p><strong>Total New Sales:</strong> {total_sales_val:,.2f} Rs</p>
                        <p><strong>Total Day Expenses:</strong> {day_expenses_total:,.2f} Rs</p>
                        <p><strong>Pure Net Profit:</strong> {net_profit_val:,.2f} Rs</p>
                        <p><strong>Recovered Udhaar Today:</strong> {total_wapsi_collection:,.2f} Rs</p>
                    </div>
                    <table>
                        <thead>
                            <tr><th>Date & Time</th><th>Item / Action</th><th>Qty</th><th>Amount</th><th>Net Profit</th><th>Mode</th></tr>
                        </thead>
                        <tbody>
                            {html_rows}
                        </tbody>
                    </table>
                    <div class='footer'><p>End of Report - Software Generated Statement.</p></div>
                """
                trigger_print(html_content)