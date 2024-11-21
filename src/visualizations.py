# src/visualizations.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_price_trend(df):
    """Generate a line plot for price trends over time by country."""
    # Rename columns and convert to datetime format
    df['date'] = pd.to_datetime(df[['price_year', 'price_month']]
                                .rename(columns={'price_year': 'year', 'price_month': 'month'})
                                .assign(day=1))
    
    plt.figure(figsize=(20, 10))
    sns.lineplot(data=df, x='date', y='price', hue='country_name', marker="o")
    plt.title('Price Trend Over Time by Country')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.xticks(rotation=45)
    plt.grid(True)
    return plt.gcf()  # Return the figure object

def plot_boxplot_by_country(df):
    """Generate a boxplot for price distribution by country."""
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=df, x='country_name', y='price')
    plt.title('Price Distribution by Country')
    plt.xlabel('Country')
    plt.ylabel('Price in USD')
    plt.xticks(rotation=45)
    return plt.gcf()  # Return the figure object

def plot_commodity_price(df, commodity_name):
    """Generate a line plot for a specific commodity's price trend over time."""
    # Filter for the selected commodity
    df_commodity = df[df['cm_name'] == commodity_name]
    # Rename columns and convert to datetime format
    df_commodity['date'] = pd.to_datetime(df_commodity[['price_year', 'price_month']]
                                          .rename(columns={'price_year': 'year', 'price_month': 'month'})
                                          .assign(day=1))
    
    plt.figure(figsize=(20, 10))
    sns.lineplot(data=df_commodity, x='date', y='price', hue='country_name', marker="o")
    plt.title(f'{commodity_name} Price Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.xticks(rotation=45)
    plt.grid(True)
    return plt.gcf()  # Return the figure object
