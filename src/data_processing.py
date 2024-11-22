# src/data_processing.py
import pandas as pd
from src.constants import column_rename_dict, currency_conversion_dict, commodity_mapping

def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='error')
    df.rename(columns=column_rename_dict, inplace=True)
    return df

def process_data(df, countries):
    return df[df['country_name'].isin(countries)]

def filter_data_by_country(df, countries):
    return df[df['country_name'].isin(countries)]

def clean_data(df):
    df = df.drop_duplicates()
    df = df[df['price_year'] >= 2008]
    #df['month_year'] = df['price_year'].astype(str) + '-' + df['price_month'].astype(str)
    # Convert 'month_year' to a Period type with monthly frequency
    #df['month_year'] = pd.to_datetime(df['month_year'], format='%Y-%m')
    return df

def clean_data_NA(df):
    return None

def currency_conversion(df):
    df['price'] = df.apply(lambda row: row['price'] * currency_conversion_dict.get(row['cur_name'], 1), axis=1)
    return df

def categorize_commodity(df):
    df['commodity_category'] = df['cm_name'].map(commodity_mapping)
    return df

def select_model_columns(df, columns):
    return df[columns].copy()