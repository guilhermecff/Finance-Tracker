import calendar
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go

incomes =['Salary', 'Dividends', 'Savings', 'Other incomes']
expenses = ['Rent', 'Food', 'Transport', 'Leisure', 'Others expenses']
currency = 'USD'
page_title = 'Personal Finance Tracker'
page_icon = '💰'
layout = 'wide'

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])


st.header(f'Data Entry in {currency}')
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox('Select Month', months, key='month')
    col2.selectbox('Select Year', years, key='year')
    
    with st.expander('Incomes'):
        for income in incomes:
            st.number_input(f"{income}:",min_value=0, key=income, format='%i', step=5)
    with st.expander('Expenses'):
        for expense in expenses:
            st.number_input(f"{expense}:",min_value=0, key=expense, format='%i', step=5)

    with st.expander('Comments'):
        comment = st.text_area("", max_chars=500, placeholder="Leave your comments here...")
        
    submitted = st.form_submit_button("Submit")
    if submitted:
        period = str(st.session_state['year']) + '_' + str(st.session_state['month'])
        incomes_values = {income: st.session_state[income] for income in incomes}
        expenses_values = {expense: st.session_state[expense] for expense in expenses}
        
        st.write(f"Data for {period}")
        st.write(f'Incomes: {incomes_values}')
        st.write(f'Expenses: {expenses_values}')
        st.success('Data submitted successfully!')
        
st.header('Data Visualization')
with st.expander('Incomes vs Expenses'):
    period = st.selectbox("Select Period", ["2024_June"])
    submitted = st.button("Plot Data")
    if submitted:
        comment = "This is a test"
        incomes = {'Salary': 1000, 'Dividends': 200, 'Savings': 300, 'Other incomes': 100}
        expenses = {'Rent': 500, 'Food': 200, 'Transport': 100, 'Leisure': 150, 'Others expenses': 50}
        
        total_incomes = sum(incomes.values())
        total_expenses = sum(expenses.values())
        remaining = total_incomes - total_expenses
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Incomes", f"{total_incomes} {currency}")
        col2.metric("Total Expenses", f"{total_expenses} {currency}")
        col3.metric("Remaining", f"{remaining} {currency}")
        st.text(comment)
        
        # Create sankey chart
        label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())

        # Source indices: all incomes point to the total income node
        source = list(range(len(incomes))) + [len(incomes)] * len(expenses)

        # Target indices: total income node flows into each expense
        target = [len(incomes)] * len(incomes) + [len(incomes) + 1 + i for i in range(len(expenses))]

        # Values: incomes and expenses
        value = list(incomes.values()) + list(expenses.values())

        # Data to dict, dict to sankey
        link = dict(source=source, target=target, value=value)
        node = dict(label=label, pad=20, thickness=30, color="#E694FF")
        data = go.Sankey(link=link, node=node)

        # Plot it once
        fig = go.Figure(data)
        fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
        st.plotly_chart(fig, use_container_width=True)
