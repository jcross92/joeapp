import streamlit as st
import pandas as pd
from datetime import date
import io

# --- 1. CONFIGURATION AND INITIAL STATE ---

st.set_page_config(
    page_title="Personal Goal Tracker (MVP)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for data persistence
if 'pnl_data' not in st.session_state:
    # Example starting data for P&L
    st.session_state.pnl_data = pd.DataFrame(
        [
            {'Date': date(2025, 11, 25), 'Description': 'Salary', 'Amount': 5000.00, 'Category': 'Income'},
            {'Date': date(2025, 11, 28), 'Description': 'Mortgage Payment', 'Amount': -1500.00, 'Category': 'Housing'},
            {'Date': date(2025, 11, 29), 'Description': 'Groceries', 'Amount': -85.50, 'Category': 'Food'},
        ]
    ).sort_values(by='Date', ascending=False)
    
if 'habits' not in st.session_state:
    # Habits with a default status for today
    st.session_state.habits = {
        'Code for 30 minutes': False,
        'Read bedtime story': False,
        'Walk the cat (joke!)': False,
        'No spend day': False,
    }

if 'kpis' not in st.session_state:
    # A simple way to track metrics over time (Date and Value)
    st.session_state.kpis = {
        'Weight (kg)': [{'Date': date(2025, 12, 1), 'Value': 85.2}, {'Date': date(2025, 12, 3), 'Value': 84.9}],
        'Norwich City Score': [{'Date': date(2025, 11, 30), 'Value': 3}, {'Date': date(2025, 12, 3), 'Value': 1}],
    }

# Common categories for P&L
FINANCE_CATEGORIES = ['Income', 'Housing', 'Food', 'Transport', 'Family Activity', 'Work', 'F1 Tickets', 'Other']


# --- 2. LAYOUT AND NAVIGATION ---

st.title("🎯 The Corporate Development Director's Personal Tracker")
st.caption("A simple MVP for tracking Finance, Habits, and KPIs.")
st.markdown("---")

# Use a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["1. Personal P&L", "2. Habits Tracker", "3. Key KPIs"])
st.sidebar.markdown("---")
st.sidebar.write("*(Deployment tip: Push this code and the `requirements.txt` file to GitHub for easy hosting on Streamlit Cloud!)*")


# --- 3. PAGE CONTENT ---

if page == "1. Personal P&L":
    st.header("💰 Financial P&L: Transactions")
    st.info("Challenge yourself: The goal here is to get your CSV data into this table and categorize it.")

    # CSV Upload Feature
    st.subheader("Import Transactions via CSV")
    uploaded_file = st.file_uploader("Upload your bank CSV or intermediary file (e.g., from Snoop):", type=["csv"])

    if uploaded_file is not None:
        try:
            # Read the CSV file into a temporary DataFrame
            temp_df = pd.read_csv(uploaded_file)
            
            st.success(f"Successfully loaded {len(temp_df)} rows from the CSV.")
            
            # Simple assumption: CSV has 'Date', 'Description', and 'Amount' columns.
            required_cols = ['Date', 'Description', 'Amount']
            
            if all(col in temp_df.columns for col in required_cols):
                # Prompt the user to confirm categorization for new data
                st.subheader("Confirm & Categorize Imported Data")
                
                new_transactions = []
                # Use st.dataframe for an editable view of the new data before confirming
                for index, row in temp_df.iterrows():
                    # For a real app, you'd use a more efficient categorization loop,
                    # but for MVP we show the data.
                    
                    # Store data after potential categorization (simplified for this MVP)
                    new_transactions.append({
                        'Date': pd.to_datetime(row['Date']).date(),
                        'Description': row['Description'],
                        'Amount': row['Amount'],
                        # In a real app, you'd prompt the user for this category
                        'Category': st.selectbox(
                            f"Category for: {row['Description']} (£{row['Amount']:.2f})", 
                            options=FINANCE_CATEGORIES,
                            key=f"cat_{index}"
                        )
                    })

                if st.button(f"Add {len(new_transactions)} transactions to P&L"):
                    # Convert new data to DataFrame and concatenate
                    new_df = pd.DataFrame(new_transactions)
                    st.session_state.pnl_data = pd.concat([st.session_state.pnl_data, new_df], ignore_index=True)
                    st.session_state.pnl_data = st.session_state.pnl_data.sort_values(by='Date', ascending=False)
                    st.success("Transactions added and categorized!")
            else:
                st.error(f"Error: Your CSV must contain columns named: {', '.join(required_cols)}")
                st.dataframe(temp_df.head())

        except Exception as e:
            st.error(f"An error occurred while reading the CSV: {e}")

    # Display P&L Summary
    st.subheader("Transaction History")
    
    # Calculate key metrics
    total_income = st.session_state.pnl_data[st.session_state.pnl_data['Amount'] > 0]['Amount'].sum()
    total_expense = st.session_state.pnl_data[st.session_state.pnl_data['Amount'] < 0]['Amount'].sum()
    net_total = total_income + total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"£{total_income:,.2f}", delta_color="normal")
    col2.metric("Total Expenses", f"£{abs(total_expense):,.2f}", delta_color="inverse")
    col3.metric("Net Total", f"£{net_total:,.2f}", delta=f"£{net_total:,.2f}")


    st.dataframe(st.session_state.pnl_data.style.format({'Amount': '£{:,.2f}'}), use_container_width=True)


elif page == "2. Habits Tracker":
    st.header("✅ Daily Habits")
    st.info("Remember to pick up good habits! Like reading to your children (born 2022 & 2025).")

    today = date.today().strftime("%A, %B %d, %Y")
    st.subheader(f"Habits for Today ({today})")

    # Display and update habits using session state
    for habit, status in st.session_state.habits.items():
        # Use a callback function to update the session state when the checkbox changes
        def update_habit_state(h):
            st.session_state.habits[h] = st.session_state.habits.get(h, False)

        st.session_state.habits[habit] = st.checkbox(
            habit, 
            value=status, 
            key=habit, 
            on_change=update_habit_state, 
            args=(habit,)
        )
        
    st.markdown("---")
    st.subheader("Add a New Habit")
    new_habit = st.text_input("Enter new habit:")
    if st.button("Add Habit"):
        if new_habit and new_habit not in st.session_state.habits:
            st.session_state.habits[new_habit] = False
            st.success(f"Habit '{new_habit}' added!")
            # Rerun the app to refresh the habit list
            st.rerun()

elif page == "3. Key KPIs":
    st.header("📈 Key Performance Indicators (Metrics)")
    st.info("Tracking your key metrics: weight, net worth, and how Norwich City is performing!")

    # KPI Input Form
    st.subheader("Log a New Metric")
    kpi_name = st.selectbox("Select KPI to Log:", options=list(st.session_state.kpis.keys()))
    kpi_value = st.number_input(f"Enter current value for {kpi_name}:", format="%.2f", step=0.1)
    kpi_date = st.date_input("Date of measurement:", value="today")

    if st.button("Log Metric Value"):
        if kpi_value and kpi_name:
            st.session_state.kpis[kpi_name].append({'Date': kpi_date, 'Value': kpi_value})
            st.success(f"Logged {kpi_name}: {kpi_value} on {kpi_date}")
            st.rerun()

    st.markdown("---")
    st.subheader("KPI History")

    # Display charts for each KPI
    for kpi, history in st.session_state.kpis.items():
        if history:
            df = pd.DataFrame(history).sort_values(by='Date')
            st.subheader(f"{kpi} Trend")
            
            # Simple logic to show current status vs. previous
            latest_value = df['Value'].iloc[-1]
            previous_value = df['Value'].iloc[-2] if len(df) > 1 else latest_value
            
            # Customizing the KPI card based on the type of metric (e.g., lower is better for weight)
            delta_direction = "inverse" if "Weight" in kpi else "normal"
            
            st.metric(
                label=f"Latest {kpi}", 
                value=f"{latest_value:.2f}",
                delta=f"{latest_value - previous_value:.2f}",
                delta_color=delta_direction
            )
            
            st.line_chart(df, x='Date', y='Value', use_container_width=True)
            
# --- END OF APP ---
