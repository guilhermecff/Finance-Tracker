# Finance-Tracker

# Personal Finance Tracker 💰

This project is a web application for tracking personal finances, built using Streamlit, Plotly, and MongoDB. The application allows users to input their income and expenses, store them in a MongoDB database, and visualize the data using interactive charts.

## Features

- **Data Entry**: Users can input their income and expenses for each month, categorize them, and add comments. The data is stored in a MongoDB database via the MongoDB Data API.
- **Data Visualization**: Users can visualize their income and expenses for selected periods using interactive Sankey charts, which help in understanding the flow of money.

## Technologies Used

- **Streamlit**: Used for creating the web application interface.
- **Plotly**: Used for generating interactive charts and visualizations.
- **MongoDB**: Used as the database for storing income and expense records.
- **Python**: Core programming language used for the backend logic.
- **Streamlit Option Menu**: Used for creating a user-friendly navigation menu.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Finance-Tracker.git
   cd Finance-Tracker


## Usage

- **Data Entry**:
  1. Navigate to the **Data Entry** tab in the application.
  2. Select the desired month and year from the dropdown menus.
  3. Enter your income and expenses in the respective fields, categorized under **Incomes** and **Expenses**.
  4. Add any comments in the **Comments** section if needed.
  5. Click the **Submit** button to save your entries to the database.

- **Data Visualization**:
  1. Switch to the **Data Visualization** tab.
  2. Select a period (month and year) from the available options to view the data.
  3. Click the **Plot Data** button to generate an interactive Sankey chart.
  4. Analyze the flow of income and expenses, and view the summary metrics (Total Incomes, Total Expenses, Remaining).
  5. Comments associated with the selected period are displayed for additional context.

The Sankey chart provides a visual representation of the flow of funds, allowing users to easily track where their money is coming from and where it is being spent.

