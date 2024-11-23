import streamlit as st
import io
import pandas as pd
from b2sdk.v2 import B2Api, InMemoryAccountInfo, DoNothingProgressListener
import os


# Set the page title to 'Predicted Prices'
st.set_page_config(page_title="Predicted Prices")

# Load data with updated caching method
@st.cache_data
def load_data():
    try:
        account_id = os.getenv('B2_APP_KEY_ID')
        application_key = os.getenv('B2_APP_KEY')
        
        if not account_id or not application_key:
            st.error("Backblaze credentials not found in environment variables")
            return pd.DataFrame()
            
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", account_id, application_key)
        
        # Get bucket and download file
        bucket = b2_api.get_bucket_by_name("Food-Prediction-EDA")
        file_info = bucket.download_file_by_name(
            "predicted_prices.csv",
            DoNothingProgressListener()
        )
        
        # Read file into pandas DataFrame
        file_stream = io.BytesIO()
        file_info.save(file_stream)
        file_stream.seek(0)
        return pd.read_csv(file_stream)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Main function to display the Streamlit app
def main():
    st.title("Predicted Food Prices")
    
    # Load the data
    data = load_data()
    
    if data.empty:
        st.error("Unable to load data. Please check your configuration.")
        return
    
    # Filter options
    countries = sorted(data['country_name'].unique())
    months = sorted(data['price_month'].unique())
    years = sorted(data['price_year'].unique())
    commodities = sorted(data['commodity_category'].unique())
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        selected_country = st.selectbox("Select Country", countries)
        selected_month = st.selectbox("Select Month", months)
    
    with col2:
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
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px;'>
                <h2>Predicted Price</h2>
                <h1 style='color: #1f77b4;'>${avg_price:.2f}</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.warning("No data available for the selected combination.")

if __name__ == "__main__":
    main()