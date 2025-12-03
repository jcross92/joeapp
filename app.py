import streamlit as st

st.set_page_config(layout="wide")
st.title("🎯 Personal Goal Tracker")
st.markdown("---")

# Use a sidebar for navigation (Simple MVP)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["1. Personal P&L", "2. Habits Tracker", "3. Key KPIs"])

if page == "1. Personal P&L":
    st.header("💰 Financial P&L")
    st.markdown("*(Placeholder for CSV upload and P&L calculations)*")
    st.text_area("Load your bank data CSV here...") # Simple place to paste data

elif page == "2. Habits Tracker":
    st.header("✅ Daily Habits")
    st.markdown("*(Use checkboxes to track daily progress)*")
    st.checkbox("Code for 30 mins")
    st.checkbox("Go for a walk")
    st.checkbox("Read to the children") # Personalization nod

elif page == "3. Key KPIs":
    st.header("📈 Key Performance Indicators")
    st.markdown("*(Input current metrics and view history)*")
    st.number_input("Current Weight (kg)", min_value=1, step=1)
    st.number_input("Current Net Worth (£)", step=1000)
    
st.sidebar.markdown("---")
st.sidebar.info("App powered by Streamlit.")
