# app.py
from src.data_processing import load_and_prepare_data, filter_data_by_country, clean_data, currency_conversion, select_model_columns, categorize_commodity

from src.analysis import run_regression
from src.models import predict_data
import pandas as pd

# Load and prepare the data
data_path = 'data/wfp_market_food_prices.csv'
M_food_prices = load_and_prepare_data(data_path)

# Filter data for specific countries
countries = ['India', 'Pakistan', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh','Costa Rica', 'El Salvador','Guatemala', 'Honduras', 'Panama', 'Colombia', 'Cambodia', 'Indonesia', "Lao People's Democratic Republic", 'Myanmar', 'Philippines', 'Azerbaijan', 'Jordan', 'Lebanon', 'Syrian Arab Republic']
filtered_data = filter_data_by_country(M_food_prices, countries)

# Clean the data
cleaned_data = clean_data(filtered_data)

# Apply currency conversion
converted_data = currency_conversion(cleaned_data)

#calculate_correlation(converted_data)
model_columns = ['country_name','unit_measure_id','price_month','price_year','commodity_category','price']

converted_data = categorize_commodity(converted_data)

model_data = select_model_columns(converted_data, model_columns)

pipeline, y_test, y_pred, r2, mse  = run_regression(model_data)

predict_till_year = 2026

predicted_prices = predict_data(pipeline,predict_till_year,countries)

predicted_prices.to_csv('data/predicted_prices.csv',index=False)

#residual_analysis(converted_data)
