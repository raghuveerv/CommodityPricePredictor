import streamlit as st
import pandas as pd
import base64
import os
from b2sdk.v2 import InMemoryAccountInfo, B2Api, DoNothingProgressListener
import io
import folium
from folium import plugins
import geopandas as gpd
from dotenv import load_dotenv

# Set page configuration with a dark theme
st.set_page_config(
    page_title="Global Food Price Predictor", 
    page_icon="🌾", 
    layout="wide", 
    initial_sidebar_state="expanded"
)


# Custom CSS for enhanced aesthetics
st.markdown("""
<style>
    /* Base styling */
    body {
        background-color: #121212;
        color: #e0e0e0;
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }
    
    .st-c3 {
    color: #e0e0e0 !important; /* Ensure the text is light and visible */
    background-color: #2C2C2C !important; /* Match the dropdown background */
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        border-right: 2px solid #2C2C2C;
    }

    /* Sidebar header */
    .sidebar-header {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
        border-radius: 0 0 15px 15px;
    }

    .sidebar-header h1 {
        color: white;
        margin: 0;
        font-size: 1.5em;
        font-weight: 700;
    }

        /* Fix for input box displaying selected dropdown text */
    .stSelectbox div > div input {
        color: #e0e0e0 !important; /* Light text for visibility */
        background-color: #2C2C2C !important; /* Match the background */
        border-color: #404040 !important; /* Border color */
    }

    /* Additional Fix: Styling for the input box */
    .stSelectbox div > div input:focus {
        color: #e0e0e0 !important;
        background-color: #2C2C2C !important;
        border-color: #4CAF50 !important; /* Green border on focus */
    }

    /* Dropdown options styling */
    .stSelectbox div[role="listbox"] div[role="option"] {
        color: #e0e0e0 !important;
        background-color: #1E1E1E !important;
    }

    .stSelectbox div[role="listbox"] {
        color: #e0e0e0 !important;
        background-color: #1E1E1E !important;
    }

    /* Selectbox label styling */
    .stSelectbox label {
        color: #4CAF50;
        font-weight: 600;
        margin-bottom: 5px;
    }

    /* Price display */
    .price-display {
        background-color: #1E1E1E;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #2C2C2C;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }

    .price-display:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 25px rgba(0,0,0,0.4);
    }

    /* User guide styling */
    .user-guide {
        background-color: #1E1E1E;
        border: 1px solid #2C2C2C;
        border-radius: 15px;
        padding: 20px;
    }

    /* Expander styling */
    .stExpander {
        border: 1px solid #2C2C2C;
        border-radius: 10px;
        background-color: #1E1E1E;
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

# Load data with updated caching method
load_dotenv()
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

def create_sidebar():
    # Custom sidebar with enhanced styling
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h1>🌾 Food Price Predictor</h1>
    </div>
    """, unsafe_allow_html=True)

    # Add an elegant logo or decorative element
    st.sidebar.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <div style="width: 100px; height: 100px; background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); 
                    border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 3em; font-weight: bold;">FP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar description
    st.sidebar.markdown("""
    <p style="color: #B0BEC5; text-align: center; padding: 0 15px;">
    Predict food commodity prices across different countries, months, and years.
    </p>
    """, unsafe_allow_html=True)

def main():
    # Create custom sidebar
    create_sidebar()
    
    # Main content
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Global Food Price Predictor</h1>", unsafe_allow_html=True)
    
    
    
    # Load the data
    data = load_data()

    # Create columns for layout
    col1, col2, col3, col4 = st.columns(4)
    
    # Filter options with enhanced layout
    with col1:
        selected_country = st.selectbox("Select Country", data['country_name'].unique())
    
    with col2:
        selected_month = st.selectbox("Select Month", sorted(data['price_month'].unique()))
    
    with col3:
        selected_year = st.selectbox("Select Year", sorted(data['price_year'].unique()))
    
    with col4:
        selected_commodity = st.selectbox("Select Commodity", data['commodity_category'].unique())

    # Filter data based on selections
    filtered_data = data[
        (data['country_name'] == selected_country) & 
        (data['price_year'] == selected_year) &
        (data['price_month'] == selected_month) &
        (data['commodity_category'] == selected_commodity)
    ]

    # Price display with custom styling
    if not filtered_data.empty:
        avg_price = filtered_data['predicted_price'].mean()
        st.markdown(f"""
        <div class="price-display">
            <h2 style="color: #4CAF50; margin-bottom: 10px;">Predicted Price</h2>
            <h1 style="color: #81C784; font-size: 3em; margin: 0;">${avg_price:.2f}</h1>
            <p style="color: #B0BEC5; font-size: 0.9em;">
                {selected_commodity} in {selected_country} for {selected_month} {selected_year}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No data available for the selected criteria.")

    # User Guide Section
    with st.expander("📖 How to Use This App"):
        st.markdown("""
        <div class="user-guide">
        <h3 style="color: #4CAF50;">🎯 Purpose of the App</h3>
        <p>This application helps you predict food commodity prices across different countries, months, and years. It provides a user-friendly interface to explore and understand potential future food prices.</p>

        <h3 style="color: #4CAF50;">🔍 How to Navigate</h3>
        <ol>
            <li><strong>Select Country</strong>: Choose the country for which you want to predict food prices.</li>
            <li><strong>Select Month</strong>: Pick the specific month of interest.</li>
            <li><strong>Select Year</strong>: Choose the year for your price prediction.</li>
            <li><strong>Select Commodity</strong>: Pick the type of food commodity you're interested in.</li>
        </ol>

        <h3 style="color: #4CAF50;">📊 Interpreting Results</h3>
        <p>Once you've made your selections, the app will display:</p>
        <ul>
            <li>A predicted price for the selected commodity</li>
            <li>The exact details of your selection (commodity type, country, month, and year)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()