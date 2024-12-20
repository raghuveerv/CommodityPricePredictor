import io 
import streamlit as st
from b2sdk.v2 import B2Api, InMemoryAccountInfo, DoNothingProgressListener
from src.data_processing import load_and_prepare_data, process_data, clean_data, currency_conversion, categorize_commodity
from src.visualizations import plot_price_trend, plot_boxplot_by_country, plot_commodity_price
from src.analysis import calculate_correlation_with_insights, run_regression, residual_analysis, display_data_insights
import pandas as pd
import os
<<<<<<< HEAD
import matplotlib.pyplot as plt
import seaborn as sns



# Page configuration
st.set_page_config(
    page_title="Food Price EDA Dashboard", 
    page_icon="🍽️", 
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

        
    /* Main title */
    .main-title {
        text-align: center;
        color: #4CAF50;
        margin-bottom: 30px;
        font-weight: 700;
    }

    /* Section headers */
    .section-header {
        color: #4CAF50;
        border-bottom: 2px solid #2E7D32;
        padding-bottom: 10px;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Selectbox styling */
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

    /* Data display */
    .data-display {
        background-color: #1E1E1E;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #2C2C2C;
        margin-bottom: 20px;
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

# Predefined regions
regions = {
    "South_Asia": ['India', 'Pakistan', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh'],
    "Central_America": ['Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Panama', 'Colombia'],
    "Middle_East": ['Azerbaijan', 'Jordan', 'Lebanon', 'Syrian Arab Republic', 'Turkey', 'Yemen'],
    "South_East_Asia": ['Cambodia', 'Indonesia', "Lao People's Democratic Republic", 'Myanmar', 'Philippines', 'Timor-Leste']
}

# Create custom sidebar
def create_sidebar():
    """Create a custom sidebar with enhanced styling"""
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h1>🍽️ Food Price Explorer</h1>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar description
    st.sidebar.markdown("""
    <p style="color: #B0BEC5; text-align: center; padding: 0 15px;">
    Explore and analyze global food price trends across different regions and commodities.
    </p>
    """, unsafe_allow_html=True)

# Load data from Backblaze
@st.cache_data
def load_data(selected_region):
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
            f"wfp_{selected_region}.csv",
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

# Create main app
def main():
    create_sidebar()

    # Main title with custom styling
    st.markdown("<h1 class='main-title'>Food Price Exploratory Data Analysis</h1>", unsafe_allow_html=True)

    # Region selection
    selected_region = st.sidebar.selectbox("Select Region", list(regions.keys()), index=0)
    selected_countries = regions[selected_region]

    # Data loading and processing
    M_food_prices = load_data(selected_region)

    M_food_prices = categorize_commodity(M_food_prices)

    cleaned_data = clean_data(M_food_prices)
    converted_data = currency_conversion(cleaned_data)

    # Commodity selection
    commodity = st.sidebar.selectbox("Select Commodity", M_food_prices['cm_name'].unique() if not M_food_prices.empty else [])

    # Data Overview Section
    st.markdown("<h2 class='section-header'>📊 Data Overview</h2>", unsafe_allow_html=True)
    
    if not M_food_prices.empty:
        st.markdown("<div class='data-display'>", unsafe_allow_html=True)
        st.dataframe(M_food_prices.head(), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Basic Statistics
        st.markdown("<h2 class='section-header'>📈 Basic Statistics</h2>", unsafe_allow_html=True)
        
        # Create two columns for statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='data-display'>", unsafe_allow_html=True)
            st.write("### Price Statistics")
            st.write(M_food_prices['price'].describe())
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='data-display'>", unsafe_allow_html=True)
            st.write("### Commodity Distribution")
            commodity_counts = M_food_prices['cm_name'].value_counts()
            st.bar_chart(commodity_counts)
            st.markdown("</div>", unsafe_allow_html=True)

        # Visualization Section
        st.markdown("<h2 class='section-header'>🖼️ Visualizations</h2>", unsafe_allow_html=True)
        
        # Price Distribution Boxplot
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#121212')
        ax.set_facecolor('#1E1E1E')
        sns.boxplot(x='cm_name', y='price', data=M_food_prices, ax=ax, palette='Greens')
        ax.set_title('Price Distribution by Commodity', color='#4CAF50')
        ax.set_xlabel('Commodity', color='#B0BEC5')
        ax.set_ylabel('Price', color='#B0BEC5')
        ax.tick_params(colors='#B0BEC5')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Boxplot by country
        st.write("#### Price Distribution by Country (USD)")
        st.pyplot(plot_boxplot_by_country(converted_data))

        st.write("#### Commodity Price Correlation Analysis")

        # Commodity-specific price trends
        st.write(f"#### {commodity} Price Trend Over Time")
        st.pyplot(plot_commodity_price(converted_data, commodity))
    else:
        st.error("No data available for the selected region.")

if __name__ == "__main__":
    main()
=======

# Page configuration
st.set_page_config(
    page_title="Food Price EDA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
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
    
    /* Section styling */
    .section-container {
        background-color: #1E1E1E;
        padding: 0.5rem;
        border-radius: 15px;
        border: 1px solid #2C2C2C;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* DataFrame styling */
    .dataframe {
        background-color: #2C2C2C;
        border: none;
        border-radius: 10px;
        color: #e0e0e0;
    }
    
    .dataframe th {
        background-color: #4CAF50;
        color: white;
        padding: 12px;
    }
    
    .dataframe td {
        background-color: #2C2C2C;
        color: #e0e0e0;
        padding: 10px;
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
    
    /* Plot styling */
    .plot-container {
        background-color: #1E1E1E;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #2C2C2C;
    }
    
    /* Section headers */
    h3, h4 {
        color: #4CAF50 !important;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2C2C2C;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        border-right: 1px solid #2C2C2C;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
        border-radius: 0 0 15px 15px;
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
def load_data(selected_region):
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
            f"wfp_{selected_region}.csv",
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
        <h1>📊 EDA Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div style="text-align: center; padding: 0 15px; margin-bottom: 20px; color: #B0BEC5;">
        Explore and analyze food price data across different regions
    </div>
    """, unsafe_allow_html=True)

def main():
    # Create sidebar
    create_sidebar()
    
    # Main header
    st.markdown("""
        <div class="main-header">
            <h1 class="main-title">Exploratory Data Analysis Dashboard</h1>
            <p>Comprehensive analysis of global food prices and trends</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Region selection
    regions = {
        "South_Asia": ['India', 'Pakistan', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh'],
        "Central_America": ['Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Panama', 'Colombia'],
        "Middle_East": ['Azerbaijan', 'Jordan', 'Lebanon', 'Syrian Arab Republic', 'Turkey', 'Yemen'],
        "South_East_Asia": ['Cambodia', 'Indonesia', "Lao People's Democratic Republic", 'Myanmar', 'Philippines', 'Timor-Leste']
    }
    
    selected_region = st.sidebar.selectbox("🌎 Select Region", list(regions.keys()), index=0)
    selected_countries = regions[selected_region]
    
    # Load and process data
    M_food_prices = load_data(selected_region)
    cleaned_data = clean_data(M_food_prices)
    converted_data = currency_conversion(cleaned_data)
    
    # Display filtered data
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown("### 📋 Filtered Data by Region")
    st.write(converted_data.head())
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display insights
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    display_data_insights(converted_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Correlation analysis
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown("### 📈 Correlation Analysis: Year vs Price")
    correlation, p_value = calculate_correlation_with_insights(converted_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Price trend visualization
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Price Trend Over Time by Country")
    st.pyplot(plot_price_trend(converted_data))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Boxplot visualization
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown("### 📦 Price Distribution by Country (USD)")
    st.pyplot(plot_boxplot_by_country(converted_data))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Commodity analysis
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown("### 🏷️ Commodity Price Analysis")
    commodity = st.sidebar.selectbox("📊 Select Commodity", converted_data['cm_name'].unique())
    st.markdown(f"#### {commodity} Price Trend Over Time")
    st.pyplot(plot_commodity_price(converted_data, commodity))
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
# Run the app using:
# streamlit run predictions.py
>>>>>>> Pranav-branch
