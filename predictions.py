import streamlit as st
import io
import pandas as pd
from b2sdk.v2 import B2Api, InMemoryAccountInfo, DoNothingProgressListener
import os
import subprocess
import sys

from dotenv import load_dotenv
load_dotenv()
class DataLoader:
    def __init__(self):
        self.data = None
    
    def load_data(self):
        self.data = self._load_data_static()
        return self.data
    
    @staticmethod
    @st.cache_data
    def _load_data_static():
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
    
    def filter_data(self, country, year, month, commodity):
        if self.data is None:
            return pd.DataFrame()
            
        filtered_data = self.data[
            (self.data['country_name'] == country) &
            (self.data['price_year'] == year) &
            (self.data['price_month'] == month) &
            (self.data['commodity_category'] == commodity)
        ]
        return filtered_data

class FoodPriceUI:
    def __init__(self):
        st.set_page_config(
            page_title="Food Price Predictions",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self.apply_custom_css()
        
    def apply_custom_css(self):
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
    
    def create_sidebar(self):
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
    
    def create_header(self):
        st.markdown("""
            <div class="main-header">
                <h1 class="main-title">Food Price Predictions</h1>
                <p>Price forecasting for global food commodities</p>
            </div>
        """, unsafe_allow_html=True)
    
    def create_filters(self, data):
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="filter-title">Select Parameters</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            country = st.selectbox(
                "🌍 Country",
                options=sorted(data['country_name'].unique()),
                key="country_select"
            )
        with col2:
            month = st.selectbox(
                "📅 Month",
                options=sorted(data['price_month'].unique()),
                key="month_select"
            )
        with col3:
            year = st.selectbox(
                "📆 Year",
                options=sorted(data['price_year'].unique()),
                key="year_select"
            )
        with col4:
            commodity = st.selectbox(
                "🏷️ Commodity Type",
                options=sorted(data['commodity_category'].unique()),
                key="commodity_select"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        return country, month, year, commodity
    
    def display_price(self, filtered_data, country, month, year, commodity):
        if not filtered_data.empty:
            avg_price = filtered_data['predicted_price'].mean()
            _, price_col, _ = st.columns([1, 2, 1])
            
            with price_col:
                st.markdown(f"""
                    <div class="price-container">
                        <div class="price-header">Predicted Price</div>
                        <div class="price-value">${avg_price:.2f}</div>
                        <p style="color: #B0BEC5;">{commodity} in {country}<br>for Month {month}, {year}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No data available for the selected combination.")
    
    def display_user_guide(self):
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

            <p style="color: white;">The predicted price will be displayed automatically based on your selections.</p>
            </div>
            """, unsafe_allow_html=True)

def main():
    # Initialize classes
    ui = FoodPriceUI()
    data_loader = DataLoader()
    
    # Setup UI components
    ui.create_sidebar()
    ui.create_header()
    
    # Load and process data
    data = data_loader.load_data()
    if not data.empty:
        # Create filters and get user selections
        country, month, year, commodity = ui.create_filters(data)
        
        # Filter data and display results
        filtered_data = data_loader.filter_data(country, year, month, commodity)
        ui.display_price(filtered_data, country, month, year, commodity)
        
        # Display user guide
        ui.display_user_guide()
    else:
        st.error("Unable to load data. Please check your configuration.")

if __name__ == "__main__":
    main()