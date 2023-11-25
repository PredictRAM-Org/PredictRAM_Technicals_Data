import streamlit as st
import pandas as pd
import json

# Function to load JSON data for a specific symbol
def load_stock_data(symbol):
    file_path = f"data/{symbol}_data.json"
    with open(file_path, "r") as file:
        return json.load(file)

# Function to create DataFrames from JSON data
def create_dataframes(stock_data):
    symbol_info = stock_data["data"]
    pivot_levels = symbol_info["pivotLevels"]
    sma_data = symbol_info["sma"]
    ema_data = symbol_info["ema"]
    crossover_data = symbol_info["crossover"]
    indicators_data = symbol_info["indicators"]

    pivot_levels_df = pd.DataFrame(
        [(level["key"], level["pivotLevel"]["pivotPoint"],
          level["pivotLevel"]["r1"], level["pivotLevel"]["r2"],
          level["pivotLevel"]["r3"], level["pivotLevel"]["s1"],
          level["pivotLevel"]["s2"], level["pivotLevel"]["s3"]) for level in pivot_levels],
        columns=["Key", "Pivot Point", "R1", "R2", "R3", "S1", "S2", "S3"]
    )

    sma_df = pd.DataFrame([(item["key"], item["value"], item["indication"]) for item in sma_data],
                          columns=["Key", "Value", "Indication"])

    ema_df = pd.DataFrame([(item["key"], item["value"], item["indication"]) for item in ema_data],
                          columns=["Key", "Value", "Indication"])

    crossover_df = pd.DataFrame([
        (item["key"], item["displayValue"], item["indication"], item["period"]) for item in crossover_data
    ], columns=["Key", "Display Value", "Indication", "Period"])

    indicators_df = pd.DataFrame([
        (item["id"], item["displayName"], item["value"], item["indication"]) for item in indicators_data
    ], columns=["ID", "Display Name", "Value", "Indication"])

    return pivot_levels_df, sma_df, ema_df, crossover_df, indicators_df

# Display search input box
search_symbol = st.text_input("Enter stock symbol:")
search_button = st.button("Search")

if search_button:
    # Load and display data for the entered symbol
    try:
        stock_data = load_stock_data(search_symbol)
        pivot_levels_df, sma_df, ema_df, crossover_df, indicators_df = create_dataframes(stock_data)

        # Display information using Streamlit
        st.title(f"Stock Information - {search_symbol}")
        
        st.subheader("Pivot Levels")
        st.table(pivot_levels_df)

        st.subheader("Simple Moving Averages (SMA)")
        st.table(sma_df)

        st.subheader("Exponential Moving Averages (EMA)")
        st.table(ema_df)

        st.subheader("Moving Average Crossovers")
        st.table(crossover_df)

        st.subheader("Technical Indicators")
        st.table(indicators_df)

    except FileNotFoundError:
        st.error("Data not found for the entered symbol. Please enter a valid stock symbol.")
