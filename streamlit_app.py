# streamlit_app.py

import streamlit as st
from src.data_processing import load_and_prepare_data, process_data, clean_data, currency_conversion
from src.visualizations import plot_price_trend, plot_boxplot_by_country, plot_commodity_price
from src.analysis import calculate_correlation, run_regression, residual_analysis
import pandas as pd

# Page title
st.title("Food Price Analysis Dashboard")

# Sidebar for user inputs
st.sidebar.header("User Inputs")
data_path = 'data/wfp_market_food_prices.csv'

# Load data and perform initial processing
st.subheader("Dataset Overview")
M_food_prices = load_and_prepare_data(data_path)
st.write("### Original Data")
st.write(M_food_prices.head())

# Filter data by countries
countries = ['India', 'Pakistan', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh']
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)
filtered_data = process_data(M_food_prices, selected_countries)

# Data cleaning and currency conversion
cleaned_data = clean_data(filtered_data)
converted_data = currency_conversion(cleaned_data)

# Display filtered data
st.write("### Filtered Data (USD Converted)")
st.write(converted_data.head())

# Generate visualizations
st.subheader("Visualizations")

# Price trend line chart
st.write("#### Price Trend Over Time by Country")
st.pyplot(plot_price_trend(converted_data))

# Boxplot by country
st.write("#### Price Distribution by Country (USD)")
st.pyplot(plot_boxplot_by_country(converted_data))

# Commodity-specific price trends
commodity = st.sidebar.selectbox("Select Commodity", converted_data['cm_name'].unique())
st.write(f"#### {commodity} Price Trend Over Time")
st.pyplot(plot_commodity_price(converted_data, commodity))

# Statistical Analysis Section
st.subheader("Statistical Analysis")

# Correlation calculation
st.write("#### Pearson Correlation between Year and Price (USD)")
correlation, p_value = calculate_correlation(converted_data)
st.write(f"Pearson correlation coefficient: {correlation}")
st.write(f"P-value: {p_value}")

# Regression Analysis
st.write("#### Regression Analysis")
run_regression(converted_data)
st.write("Model trained successfully. See console output for model details.")

# Residual Analysis
st.write("#### Residual Analysis")
residual_analysis(converted_data)
st.write("Residual analysis complete. See console output for details.")

# Run the app using:
# streamlit run streamlit_app.py
