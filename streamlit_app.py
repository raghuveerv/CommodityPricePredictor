# streamlit_app.py
import streamlit as st
import io
import pandas as pd
from b2sdk.v2 import B2Api, InMemoryAccountInfo, DoNothingProgressListener

# Set the page title to 'Predicted Prices'
st.set_page_config(page_title="Predicted Prices")

# Page title

# # Sidebar for user inputs
# st.sidebar.header("User Inputs")
# data_path = 'data/wfp_market_food_prices.csv'

# # Load data and perform initial processing
# st.subheader("Dataset Overview")
# M_food_prices = load_and_prepare_data(data_path)
# st.write("### Original Data")
# st.write(M_food_prices.head())

# # Filter data by region

# regions = ['South-Asia', 'Central-America', 'Middle-East']
# selected_region = st.sidebar.selectbox("Select Region", regions)
# filtered_data = process_data(M_food_prices, selected_countries)


# # Filter data by countries
# countries = ['India', 'Pakistan', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh']
# selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)
# filtered_data = process_data(M_food_prices, selected_countries)

# # Data cleaning and currency conversion
# cleaned_data = clean_data(filtered_data)
# converted_data = currency_conversion(cleaned_data)

# # Display filtered data
# st.write("### Filtered Data (USD Converted)")
# st.write(converted_data.head())

# # Generate visualizations
# st.subheader("Visualizations")

# # Price trend line chart
# st.write("#### Price Trend Over Time by Country")
# st.pyplot(plot_price_trend(converted_data))

# # Boxplot by country
# st.write("#### Price Distribution by Country (USD)")
# st.pyplot(plot_boxplot_by_country(converted_data))

# # Commodity-specific price trends
# commodity = st.sidebar.selectbox("Select Commodity", converted_data['cm_name'].unique())
# st.write(f"#### {commodity} Price Trend Over Time")
# st.pyplot(plot_commodity_price(converted_data, commodity))

# # Statistical Analysis Section
# st.subheader("Statistical Analysis")

# # Correlation calculation
# st.write("#### Pearson Correlation between Year and Price (USD)")
# correlation, p_value = calculate_correlation(converted_data)
# st.write(f"Pearson correlation coefficient: {correlation}")
# st.write(f"P-value: {p_value}")

# # Regression Analysis
# st.write("#### Regression Analysis")
# run_regression(converted_data)
# st.write("Model trained successfully. See console output for model details.")

# # Residual Analysis
# st.write("#### Residual Analysis")
# residual_analysis(converted_data)
# st.write("Residual analysis complete. See console output for details.")

# # Run the app using:
# # streamlit run streamlit_app.py


# page = st_navbar(["Predict Price", "Exploratory Data Analysis", "Model details"])
# st.write(page)

# Load data with updated caching method
@st.cache_data
def load_data():
    # account_id = '0054cde0cafa8260000000002' # can be the keyID 
    # application_key = 'K005ZTPUCjICGyTcMRzq9eL5MBeiJDQ'
    # info = InMemoryAccountInfo()
    # b2_api = B2Api(info)
    # b2_api.authorize_account("production", account_id, application_key)
    # bucket = b2_api.get_bucket_by_name("World-Food-Data")
    # # Download the file by ID
    # file_info = bucket.download_file_by_name("predicted_prices.csv")
    # file_stream = io.BytesIO()
    # file_info.save(file_stream)
    # file_stream.seek(0)
    return pd.read_csv("https://raw.githubusercontent.com/raghuveerv/CommodityPricePredictor/refs/heads/Pranav's-work/data/predicted_prices.csv")

# Main function to display the Streamlit app
def main():
    st.title("Predicted Food Prices")
    
    # Load the data
    data = load_data()

    # Filter options
    countries = data['country_name'].unique()
    months= sorted(data['price_month'].unique())
    years = sorted(data['price_year'].unique())
    commodities = data['commodity_category'].unique()
    
    selected_country = st.selectbox("Select Country", countries)
    selected_month = st.selectbox("Select Month", months)
    selected_year = st.selectbox("Select Year", years)
    selected_commodity = st.selectbox("Select Commodity Type", commodities)

    # Filter data based on selections
    filtered_data = data[
        (data['country_name'] == selected_country) & 
        (data['price_year'] == selected_year) &
        (data['price_month'] == selected_month) &
        (data['commodity_category'] == selected_commodity)
    ]

    # Display the price in the center
    if not filtered_data.empty:
        avg_price = filtered_data['predicted_price'].mean()
        st.markdown(f"<h1 style='text-align: center;'>Price: ${avg_price:.2f}</h1>", unsafe_allow_html=True)
    else:
        st.write("No data available for the selected country, year, and commodity type.")

if __name__ == "__main__":
    main()
