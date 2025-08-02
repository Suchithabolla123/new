import streamlit as st
from streamlit_option_menu import option_menu
from config import DEFAULT_STEPS, MAX_STEPS
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import datetime
import io
from PyPDF2 import PdfReader

# Load Gemini API Key from secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Set page config
st.set_page_config(page_title="Personal Finance Assistant", layout="wide")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Finance Tools",
        options=[
            "Chatbot",
            "Statement Analysis",
            "Discount Tracker",
            "Due Dates",
            "SIP Planner",
            "Premium Summary",
            "Stock Suggester",
            "Dashboard",
        ],
        icons=[
            "chat-dots",
            "file-earmark-text",
            "tags",
            "calendar-check",
            "graph-up",
            "umbrella",
            "search",
            "bar-chart",
        ],
        menu_icon="tools",
        default_index=0,
        styles={
            "container": {"padding": "5px"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link-selected": {"background-color": "#ff4b4b", "font-weight": "bold"},
        },
    )

# Chatbot
if selected == "Chatbot":
    st.title("💬 Gemini AI Chatbot")
    user_input = st.text_input("Ask something about your finances...", "")
    steps = st.slider("Set response length (tokens)", 10, MAX_STEPS, DEFAULT_STEPS)
    if user_input:
        with st.spinner("Generating response..."):
            try:
                response = model.generate_content(user_input)
                st.success("Response:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# Statement Analysis
elif selected == "Statement Analysis":
    st.title("📄 Statement Analysis")
    uploaded_file = st.file_uploader("Upload your bank statement PDF", type=["pdf"])
    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        st.text_area("Extracted Text", text, height=300)
        st.info("Text extracted. You can use this in Chatbot to ask for analysis!")

# Discount Tracker
elif selected == "Discount Tracker":
    st.title("🏷️ Discount Tracker")
    st.subheader("Enter item name to see best price (simulated)")

    item = st.text_input("Enter Item Name (e.g., onion, samsung phone)")

    dummy_prices = {
        "onion": {"DMart": 28, "Reliance": 30, "Flipkart": 32},
        "samsung phone": {"Amazon": 24999, "Flipkart": 24500, "Reliance": 26000},
        "milk": {"DMart": 52, "Reliance": 55, "Amazon": 60},
        "rice": {"Amazon": 80, "Flipkart": 78, "DMart": 76}
    }

    if item.lower() in dummy_prices:
        prices = dummy_prices[item.lower()]
        best_store = min(prices, key=prices.get)
        best_price = prices[best_store]

        st.success(f"✅ Best Price: {best_store} - ₹{best_price}")

        st.write("### 📊 All Prices:")
        for store, price in prices.items():
            st.write(f"- {store}: ₹{price}")
    elif item:
        st.warning("No data found for this item. Try 'onion', 'samsung phone', etc.")

# Due Dates
elif selected == "Due Dates":
    st.title("🗕️ Due Dates Tracker")
    with st.form("due_date_form"):
        task = st.text_input("Task / Payment")
        due_date = st.date_input("Due Date")
        submitted = st.form_submit_button("Add Reminder")
        if submitted:
            st.success(f"Reminder added for: {task} due on {due_date}")

# SIP Planner
elif selected == "SIP Planner":
    st.title("📈 SIP Planner")
    monthly = st.number_input("Monthly Investment (₹)", min_value=0.0)
    rate = st.slider("Expected Annual Return (%)", 0.0, 20.0, 12.0)
    years = st.slider("Investment Duration (Years)", 1, 30, 10)

    if st.button("Calculate SIP"):
        r = rate / 100 / 12
        n = years * 12
        future_value = monthly * (((1 + r) ** n - 1) / r) * (1 + r)
        st.success(f"Future Value: ₹{future_value:,.2f}")

# Premium Summary
elif selected == "Premium Summary":
    st.title("🛁 Premium Summary")
    premium_type = st.selectbox("Select Premium Type", ["Health", "Life", "Vehicle"])
    amount = st.number_input("Premium Amount (₹)", min_value=0.0)
    frequency = st.selectbox("Frequency", ["Monthly", "Quarterly", "Yearly"])
    st.success(f"{premium_type} insurance premium of ₹{amount} every {frequency}")

# Stock Suggester
elif selected == "Stock Suggester":
    st.title("🔍 Stock Suggester")
    festival = st.selectbox("Choose Festival", ["Diwali", "Ugadi", "Christmas"])
    if st.button("Suggest Stocks"):
        if festival == "Diwali":
            st.write("- Reliance Industries\n- Titan\n- DMart")
        elif festival == "Ugadi":
            st.write("- TCS\n- ITC\n- HUL")
        else:
            st.write("- Zomato\n- Amazon\n- Apple")

# Dashboard
elif selected == "Dashboard":
    st.title("📊 Dashboard")
    st.write("Here's a sample chart based on dummy expenses:")
    df = pd.DataFrame({
        "Category": ["Food", "Transport", "Utilities", "Shopping"],
        "Amount": [5000, 3000, 4000, 7000]
    })
    fig = px.pie(df, values='Amount', names='Category', title='Monthly Expenses Breakdown')
    st.plotly_chart(fig)
