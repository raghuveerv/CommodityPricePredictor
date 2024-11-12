# app.py
from src.data_processing import load_and_prepare_data, filter_data_by_country, clean_data, currency_conversion, select_model_columns, categorize_commodity
from src.visualizations import plot_price_trend, plot_boxplot_by_country, plot_commodity_price
from src.analysis import calculate_correlation, run_regression, residual_analysis
from src.models import predict_data
import pandas as pd

# Load and prepare the data
data_path = 'data/wfp_market_food_prices.csv'
M_food_prices = load_and_prepare_data(data_path)

# Filter data for specific countries
countries = ['India', 'Pakistan', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh']
filtered_data = filter_data_by_country(M_food_prices, countries)

# Clean the data
cleaned_data = clean_data(filtered_data)

# Apply currency conversion
converted_data = currency_conversion(cleaned_data)

# Generate visualizations
# plot_priceend(converted_data)_tr
# plot_boxplot_by_country(converted_data)
# plot_commodity_price(converted_data, 'Wheat flour')
# plot_commodity_price(converted_data, 'Rice')

# Run analyses
#calculate_correlation(converted_data)
model_columns = ['country_name','unit_measure_id','price_month','price_year','commodity_category','price_usd']

converted_data = categorize_commodity(converted_data)

model_data = select_model_columns(converted_data, model_columns)

pipeline, y_test, y_pred, r2, mse  = run_regression(model_data)

predict_till_year = 2026

predicted_prices = predict_data(pipeline,predict_till_year,countries)

predicted_prices.to_csv('data/predicted_prices.csv',index=False)

#residual_analysis(converted_data)
