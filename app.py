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

    # Ensure numeric values for mean calculation
    pivot_levels_df[["Pivot Point", "R1", "R2", "R3", "S1", "S2", "S3"]] = pivot_levels_df[["Pivot Point", "R1", "R2", "R3", "S1", "S2", "S3"]].apply(pd.to_numeric, errors='coerce')

    # Calculate averages for Classic, Fibonacci, and Camarilla
    classic_avg = pivot_levels_df[["Pivot Point", "R1", "R2", "R3", "S1", "S2", "S3"]].mean(axis=1)
    fibonacci_avg = pivot_levels_df[["R1", "R2", "R3", "S1", "S2", "S3"]].apply(lambda x: x / 2).mean(axis=1)
    camarilla_avg = pivot_levels_df[["Pivot Point", "R1", "R2", "R3", "S1", "S2", "S3"]].apply(lambda x: x / 4).mean(axis=1)

    averages_df = pd.DataFrame({
        "Key": pivot_levels_df["Key"],
        "Classic Avg": classic_avg,
        "Fibonacci Avg": fibonacci_avg,
        "Camarilla Avg": camarilla_avg
    })

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

    # Calculate Stoploss and Target based on Pivot Levels
    stoploss_target_df = pd.DataFrame({
        "Key": pivot_levels_df["Key"],
        "Stoploss": pivot_levels_df["S1"],
        "Target": pivot_levels_df["R1"]
    })

    # Calculate Average of Stoploss and Target
    stoploss_target_avg = pd.DataFrame({
        "Average Stoploss": stoploss_target_df["Stoploss"].mean(),
        "Average Target": stoploss_target_df["Target"].mean()
    }, index=[0])

    return pivot_levels_df, averages_df, sma_df, ema_df, crossover_df, indicators_df, stoploss_target_df, stoploss_target_avg

# Display search input box
search_symbol = st.text_input("Enter stock symbol:")
search_button = st.button("Search")

if search_button:
    # Load and display data for the entered symbol
    try:
        stock_data = load_stock_data(search_symbol)
        pivot_levels_df, averages_df, sma_df, ema_df, crossover_df, indicators_df, stoploss_target_df, stoploss_target_avg = create_dataframes(stock_data)

        # Display information using Streamlit
        st.title(f"Stock Information - {search_symbol}")
        
        st.subheader("Pivot Levels")
        st.table(pivot_levels_df)

        st.subheader("Averages of Pivot Levels")
        st.table(averages_df)

        st.subheader("Simple Moving Averages (SMA)")
        st.table(sma_df)

        st.subheader("Exponential Moving Averages (EMA)")
        st.table(ema_df)

        st.subheader("Moving Average Crossovers")
        st.table(crossover_df)

        st.subheader("Technical Indicators")
        st.table(indicators_df)

        st.subheader("Stoploss and Target based on Pivot Levels")
        st.table(stoploss_target_df)

        st.subheader("Average Stoploss and Target")
        st.table(stoploss_target_avg)

    except FileNotFoundError:
        st.error("Data not found for the entered symbol. Please enter a valid stock symbol.")
