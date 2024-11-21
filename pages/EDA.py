import io
import streamlit as st
from b2sdk.v2 import B2Api, InMemoryAccountInfo, DoNothingProgressListener
from src.data_processing import load_and_prepare_data, process_data, clean_data, currency_conversion
from src.visualizations import plot_price_trend, plot_boxplot_by_country, plot_commodity_price
from src.analysis import calculate_correlation_with_insights, run_regression, residual_analysis, display_data_insights

# Page title
st.title("Exploratory Data Analysis Dashboard")

# account_id = '0054cde0cafa8260000000002' # can be the keyID 
# application_key = 'K005ZTPUCjICGyTcMRzq9eL5MBeiJDQ'
# info = InMemoryAccountInfo()
# b2_api = B2Api(info)
# b2_api.authorize_account("production", account_id, application_key)

# bucket = b2_api.get_bucket_by_name("World-Food-Data")

# # Download the file by ID
# file_info = bucket.download_file_by_name("wfp_market_food_prices.csv")

# file_stream = io.BytesIO()

# file_info.save(file_stream)

# file_stream.seek(0)
# Load data and perform initial processing
st.subheader("Dataset Overview")

regions = {
    "South_Asia": ['India', 'Pakistan', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh'],  # South Asia
    "Central_America": ['Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Panama', 'Colombia'],  # Central America
    "Middle_East": ['Azerbaijan', 'Jordan', 'Lebanon', 'Syrian Arab Republic', 'Turkey', 'Yemen'], #Middle East
    "South_East_Asia": ['Cambodia', 'Indonesia', "Lao People's Democratic Republic", 'Myanmar', 'Philippines', 'Timor-Leste']
}
# Sidebar selection for regions
selected_region = st.sidebar.selectbox("Select Region", list(regions.keys()), index=0)
selected_countries = regions[selected_region]
M_food_prices = load_and_prepare_data(f"https://raw.githubusercontent.com/raghuveerv/CommodityPricePredictor/refs/heads/main/data/wfp_{selected_region}.csv")

# Data cleaning and currency conversion
cleaned_data = clean_data(M_food_prices)
converted_data = currency_conversion(cleaned_data)

# Your existing code
st.write("### Filtered Data (USD Converted)")
st.write(converted_data.head())

# Add this line to display insights
display_data_insights(converted_data)

# Generate visualizations
st.subheader("Visualizations")

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
st.write("#### Correlation Analysis: Year vs Price")
correlation, p_value = calculate_correlation_with_insights(converted_data)

# Regression Analysis
# st.write("#### Regression Analysis")
# run_regression(converted_data)
# st.write("Model trained successfully. See console output for model details.")

# Residual Analysis
# st.write("#### Residual Analysis")
# residual_analysis(converted_data)
# st.write("Residual analysis complete. See console output for details.")

# Run the app using:
# streamlit run streamlit_app.py