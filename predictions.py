# streamlit_app.py
import streamlit as st
import io
import pandas as pd
from b2sdk.v2 import B2Api, InMemoryAccountInfo, DoNothingProgressListener

# Set the page title to 'Predicted Prices'
st.set_page_config(page_title="Predicted Prices")


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
