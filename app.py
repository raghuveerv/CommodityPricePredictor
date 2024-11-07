# app.py
from src.data_processing import load_and_prepare_data, process_data, clean_data, currency_conversion
from src.visualizations import plot_price_trend, plot_boxplot_by_country, plot_commodity_price
from src.analysis import calculate_correlation, run_regression, residual_analysis
import pandas as pd

# Load and prepare the data
data_path = 'data/wfp_market_food_prices.csv'
M_food_prices = load_and_prepare_data(data_path)

# Filter data for specific countries
countries = ['India', 'Pakistan', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh']
filtered_data = process_data(M_food_prices, countries)

# Clean the data
cleaned_data = clean_data(filtered_data)

# Apply currency conversion
converted_data = currency_conversion(cleaned_data)

# Generate visualizations
plot_price_trend(converted_data)
plot_boxplot_by_country(converted_data)
plot_commodity_price(converted_data, 'Wheat flour')
plot_commodity_price(converted_data, 'Rice')

# Run analyses
calculate_correlation(converted_data)
run_regression(converted_data)
residual_analysis(converted_data)
