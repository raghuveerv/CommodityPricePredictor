import io
import streamlit as st
from b2sdk.v2 import B2Api, InMemoryAccountInfo, DoNothingProgressListener
from src.data_processing import load_and_prepare_data, process_data, clean_data, currency_conversion, categorize_commodity
from src.visualizations import plot_price_trend, plot_boxplot_by_country, plot_commodity_price
from src.analysis import calculate_correlation_with_insights, run_regression, residual_analysis, display_data_insights
import pandas as pd
import os
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
