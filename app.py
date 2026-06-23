import streamlit as st
import pandas as pd

st.set_page_config(page_title="AHA TRENDY - Tracking", page_icon="📦")

st.title("📦 AHA TRENDY")
st.subheader("Online Order Tracking System")

# ⚠️ APNI GOOGLE SHEET KA URL YAHAN PASTE KAREIN
# Yaad rahe ke URL ke aakhir mai '/edit?usp=sharing' ko hata kar '/export?format=csv' likhna hai
SHEET_ID = "1gp6LhD-Kc_kDN7ErBw3R04YNvlyr_AGkeTUYPBBkp8U"
GOOGLE_SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=10) # Har 10 second baad data refresh ho sakega
def load_data():
    try:
        df = pd.read_csv(GOOGLE_SHEET_URL)
        df.columns = df.columns.str.strip()
        df['Order ID'] = df['Order ID'].astype(str).str.strip()
        df['Mobile'] = df['Mobile'].astype(str).str.strip()
        return df
    except Exception as e:
        st.error("Database se connect nahi ho pa raha.")
        return None

data = load_data()

if data is not None:
    search_input = st.text_input("Apna Order ID ya Mobile Number likhein:", placeholder="e.g. 1001")

    if search_input:
        search_input = search_input.strip()
        result = data[(data['Order ID'] == search_input) | (data['Mobile'] == search_input)]
        
        if not result.empty:
            row = result.iloc[0]
            st.markdown("---")
            st.markdown(f"### 📋 Order Details")
            st.write(f"**Customer Name:** {row['Customer Name']}")
            st.write(f"**Item (Commodity):** {row['Commodity']}")
            st.write(f"**Total Amount:** RS. {row['Amount']}")
            
            # Status check
            status = str(row['Status']).strip().lower()
            if status == 'delivered':
                st.success(f"🟢 Status: Delivered")
            elif status == 'dispatched':
                st.info(f"🚚 Status: Dispatched (In Transit)")
            elif status == 'pending':
                st.warning(f"⏳ Status: Pending (Preparing)")
            else:
                st.error(f"ℹ️ Status: {row['Status']}")
        else:
            st.error("❌ Koi record nahi mila. Bara-e-maharbani sahi ID enter karein.")
