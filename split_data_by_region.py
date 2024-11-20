from src.data_processing import process_data, load_and_prepare_data
import pandas as pd
from src.constants import column_rename_dict, currency_conversion_dict, commodity_mapping
all_food_data = "data/wfp_market_food_prices.csv"

# Load and prepare the data
df_all_food_data = load_and_prepare_data(all_food_data)

# Define regions and countries
regions = {
    "South Asia": ['India', 'Pakistan', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh'],  # South Asia
    "Central America": ['Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Panama', 'Colombia'],  # Central America
    "Middle East": ['Azerbaijan', 'Jordan', 'Lebanon', 'Syrian Arab Republic', 'Turkey', 'Yemen'],  # Middle East
    "South East Asia": ['Cambodia', 'Indonesia', "Lao People's Democratic Republic", 'Myanmar', 'Philippines', 'Timor-Leste']  # Southeast Asia
}

# Process and save filtered data for each region
for region in regions:
    selected_countries = regions[region]
    filtered_data = process_data(df_all_food_data, selected_countries)
    df = pd.DataFrame(filtered_data)
    df.rename(columns=column_rename_dict, inplace=True)
    df = df.drop_duplicates()
    df = df[df['price_year'] >= 2008]
    df['price'] = df.apply(lambda row: row['price'] * currency_conversion_dict.get(row['cur_name'], 1), axis=1)
    # Save the DataFrame to a CSV file
    df.to_csv(f'data/wfp_{region}.csv', index=False)
