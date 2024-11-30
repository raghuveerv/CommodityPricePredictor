import streamlit as st
import io
import pandas as pd
from b2sdk.v2 import B2Api, InMemoryAccountInfo, DoNothingProgressListener
import os
import subprocess
import sys
def install_dotenv():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])

# Call the function to install
install_dotenv()
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page layout
st.set_page_config(
    page_title="Food Price Predictions",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with dark theme
st.markdown("""
    <style>
    /* Base styling */
    body {
        background-color: #121212;
        color: #e0e0e0;
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Main container styling */
    .main {
        padding: 0 2rem;
        background-color: #121212;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    /* Filter section styling */
    .filter-section {
        background-color: #1E1E1E;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border: 1px solid #2C2C2C;
    }
    
    .filter-title {
        color: #4CAF50;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    /* Selectbox styling */
    .stSelectbox div > div input {
        color: #e0e0e0 !important;
        background-color: #2C2C2C !important;
        border-color: #404040 !important;
    }

    .stSelectbox div > div {
        background-color: #2C2C2C !important;
        color: #e0e0e0 !important;
    }

    .stSelectbox label {
        color: #4CAF50 !important;
        font-weight: 600;
        margin-bottom: 5px;
    }

    /* Price display styling */
    .price-container {
        background-color: #1E1E1E;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        text-align: center;
        margin: 2rem 0;
        border: 1px solid #2C2C2C;
        transition: transform 0.3s ease;
    }
    
    .price-container:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 25px rgba(0, 0, 0, 0.4);
    }
    
    .price-header {
        color: #4CAF50;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .price-value {
        font-size: 3.5rem;
        font-weight: 700;
        color: #81C784;
        margin: 1rem 0;
    }
    
    /* Warning and error styling */
    .stWarning {
        background-color: #332D1A;
        border: 1px solid #856404;
        border-radius: 10px;
        padding: 1rem;
        color: #FFE699;
    }
    
    .stError {
        background-color: #2D1A1A;
        border: 1px solid #721C24;
        border-radius: 10px;
        padding: 1rem;
        color: #F8D7DA;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #1E1E1E;
    }
    ::-webkit-scrollbar-thumb {
        background: #4CAF50;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

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
        
        bucket = b2_api.get_bucket_by_name("Food-Prediction-EDA")
        file_info = bucket.download_file_by_name(
            "predicted_prices.csv",
            DoNothingProgressListener()
        )
        
        file_stream = io.BytesIO()
        file_info.save(file_stream)
        file_stream.seek(0)
        return pd.read_csv(file_stream)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def create_sidebar():
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h1>🌾 Food Price Predictor</h1>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <div style="width: 100px; height: 100px; background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); 
                    border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 3em; font-weight: bold;">FP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <p style="color: #000000; text-align: center; padding: 0 15px;">
    Predict food commodity prices across different countries, months, and years.
    </p>
    """, unsafe_allow_html=True)

def main():
    # Create sidebar
    create_sidebar()
    
    # Header section
    st.markdown("""
        <div class="main-header">
            <h1 class="main-title">Food Price Predictions</h1>
            <p>Price forecasting for global food commodities</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    
    if data.empty:
        st.error("Unable to load data. Please check your configuration.")
        return
    
    # Filter section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="filter-title">Select Parameters</h2>', unsafe_allow_html=True)
    
    # Create four columns for filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_country = st.selectbox(
            "🌍 Country",
            options=sorted(data['country_name'].unique()),
            key="country_select"
        )
    
    with col2:
        selected_month = st.selectbox(
            "📅 Month",
            options=sorted(data['price_month'].unique()),
            key="month_select"
        )
    
    with col3:
        selected_year = st.selectbox(
            "📆 Year",
            options=sorted(data['price_year'].unique()),
            key="year_select"
        )
    
    with col4:
        selected_commodity = st.selectbox(
            "🏷️ Commodity Type",
            options=sorted(data['commodity_category'].unique()),
            key="commodity_select"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter and display data
    filtered_data = data[
        (data['country_name'] == selected_country) &
        (data['price_year'] == selected_year) &
        (data['price_month'] == selected_month) &
        (data['commodity_category'] == selected_commodity)
    ]
    
    if not filtered_data.empty:
        avg_price = filtered_data['predicted_price'].mean()
        
        # Create centered price display
        _, price_col, _ = st.columns([1, 2, 1])
        
        with price_col:
            st.markdown(
                f"""
                <div class="price-container">
                    <div class="price-header">Predicted Price</div>
                    <div class="price-value">${avg_price:.2f}</div>
                    <p style="color: #B0BEC5;">{selected_commodity} in {selected_country}<br>for Month {selected_month}, {selected_year}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("No data available for the selected combination.")

    # Add user guide
    with st.expander("📖 How to Use This App"):
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; border: 1px solid #2C2C2C;">
        <h3 style="color: #4CAF50;">🎯 Purpose</h3>
        <p style="color: white;">This application predicts food commodity prices across different countries, months, and years.</p>

        <h3 style="color: #4CAF50;">🔍 How to Use</h3>
        <ol style="color: white;">
            <li>Select a country from the dropdown</li>
            <li>Choose the month of interest</li>
            <li>Select the year</li>
            <li>Pick a commodity type</li>
        </ol>

        <p style="color: white;>The predicted price will be displayed automatically based on your selections.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()