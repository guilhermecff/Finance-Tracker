import calendar
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and URL from environment variables
API_KEY = os.getenv("API_KEY")
MONGO_API_URL = os.getenv("MONGO_API_URL")

# Define income and expense categories
incomes = ['Salary', 'Dividends', 'Savings', 'Other incomes']
expenses = ['Rent', 'Food', 'Transport', 'Leisure', 'Others expenses']
currency = 'USD'
page_title = 'Personal Finance Tracker'
page_icon = '💰'
layout = 'wide'

# Configure the Streamlit app
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# Define years and months for selection
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

# Hide default Streamlit style
hide_streamlit_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                        </style>
                    """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Function to make POST requests to MongoDB Data API
def mongo_api_post(endpoint, payload):
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    response = requests.post(f"{MONGO_API_URL}/{endpoint}", headers=headers, data=json.dumps(payload))
    return response.json()

# Menu options
selected = option_menu(menu_title=None, options=["Data Entry", "Data Visualization"], icons=["📝", "📊"], orientation='horizontal')

if selected == "Data Entry":
    st.header(f'Data Entry in {currency}')
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        month = col1.selectbox('Select Month', months, key='month')
        year = col2.selectbox('Select Year', years, key='year')

        # Income inputs
        with st.expander('Incomes'):
            income_data = {income: st.number_input(f"{income}:", min_value=0, key=income, format='%i', step=5) for income in incomes}

        # Expense inputs
        with st.expander('Expenses'):
            expense_data = {expense: st.number_input(f"{expense}:", min_value=0, key=expense, format='%i', step=5) for expense in expenses}

        # Comments input
        with st.expander('Comments'):
            comment = st.text_area("", max_chars=500, placeholder="Leave your comments here...")

        # Submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            period = f"{year}_{month}"
            income_record = {'period': period, **income_data, 'comments': comment}
            expense_record = {'period': period, **expense_data, 'comments': comment}

            # Insert data into MongoDB using Data API
            income_payload = {
                "collection": "incomes",     # Collection name
                "database": "Finance", # Database name
                "dataSource": "Finance",      # Data source/cluster name
                "document": income_record
            }
            expense_payload = {
                "collection": "expenses",     # Collection name
                "database": "Finance", # Database name
                "dataSource": "Finance",      # Data source/cluster name
                "document": expense_record
            }

            # Make API calls to insert data
            income_response = mongo_api_post("insertOne", income_payload)
            expense_response = mongo_api_post("insertOne", expense_payload)

            # Check responses
            if income_response.get("insertedId") and expense_response.get("insertedId"):
                st.write(f"Data for {period}")
                st.write(f'Incomes: {income_data}')
                st.write(f'Expenses: {expense_data}')
                st.success('Data submitted successfully!')
            else:
                st.error('Failed to submit data. Please check the API responses and try again.')

if selected == "Data Visualization":
    st.header('Data Visualization')
    with st.expander('Incomes vs Expenses'):
        # Fetch unique periods from the database
        find_periods_payload = {
            "collection": "incomes",
            "database": "Finance",
            "dataSource": "Finance",
            "projection": {"period": 1, "_id": 0}
        }
        periods_response = mongo_api_post("find", find_periods_payload)


        # Check if 'documents' exists and handle accordingly
        if "documents" in periods_response:
            periods = sorted(set(doc['period'] for doc in periods_response["documents"]))
        else:
            st.error('Failed to fetch periods. Please check the API response structure.')
            periods = []

        period = st.selectbox("Select Period", periods)

        # Plot data on button click
        if st.button("Plot Data"):
            # Retrieve data from MongoDB using Data API
            income_payload = {
                "collection": "incomes",
                "database": "Finance",
                "dataSource": "Finance",
                "filter": {"period": period}
            }
            expense_payload = {
                "collection": "expenses",
                "database": "Finance",
                "dataSource": "Finance",
                "filter": {"period": period}
            }

            # Make API calls to retrieve data
            incomes_response = mongo_api_post("findOne", income_payload)
            expenses_response = mongo_api_post("findOne", expense_payload)

            # Check if data was retrieved successfully
            incomes = incomes_response.get("document", {})
            expenses = expenses_response.get("document", {})

            # Ensure numeric values and handle only numeric fields
            def parse_numeric(value):
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return 0

            total_incomes = sum(parse_numeric(incomes.get(income, 0)) for income in incomes if income in incomes and income != 'period' and income != 'comments')
            total_expenses = sum(parse_numeric(expenses.get(expense, 0)) for expense in expenses if expense in expenses and expense != 'period' and expense != 'comments')
            remaining = total_incomes - total_expenses

            # Display metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Incomes", f"{total_incomes} {currency}")
            col2.metric("Total Expenses", f"{total_expenses} {currency}")
            col3.metric("Remaining", f"{remaining} {currency}")

            # Display comments (assuming comments are stored separately)
            comments = incomes.get('comments', 'No comments available.')
            st.text(comments)

            # Create Sankey chart
            label = list(incomes.keys())[1:-1] + ["Total Income"] + list(expenses.keys())[1:-1]

            # Source indices: all incomes point to the total income node
            source = list(range(len(incomes) - 2)) + [len(incomes) - 2] * (len(expenses) - 2)

            # Target indices: total income node flows into each expense
            target = [len(incomes) - 2] * (len(incomes) - 2) + [len(incomes) + i - 2 for i in range(1, len(expenses) - 1)]

            # Values: incomes and expenses
            value = [parse_numeric(incomes.get(inc, 0)) for inc in list(incomes.keys())[1:-1]] + [parse_numeric(expenses.get(exp, 0)) for exp in list(expenses.keys())[1:-1]]

            # Data to dict, dict to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            data = go.Sankey(link=link, node=node)

            # Plot it once
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)

