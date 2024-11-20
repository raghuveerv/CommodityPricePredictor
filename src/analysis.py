# src/analysis.py
import pandas as pd
import streamlit as st
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def calculate_correlation(df):
    # correlation, p_value = pearsonr(df['price_year'], df['price_usd'])
    # return correlation, p_value
# Ensure price_usd is rounded to two decimal places
    df['price_usd'] = df['price_usd'].round(2)

    # Group by region, commodity, and calculate average price
    region_commodity_prices = df.groupby(['region_name', 'commodity_category'])['price_usd'].mean().reset_index()

    # Get the top 5 most common commodities
    top_commodities = df['commodity_category'].value_counts().nlargest(5).index

    # Filter for these top commodities
    top_commodity_prices = region_commodity_prices[region_commodity_prices['commodity_category'].isin(top_commodities)]

    # Create a pivot table for easier plotting
    pivot_prices = top_commodity_prices.pivot(index='region_name', columns='commodity_category', values='price_usd')

    # Plot
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_prices, annot=True, fmt='.2f', cmap='YlOrRd')
    plt.title('Average Prices (USD) of Top 5 Commodities')
    plt.tight_layout()
    plt.show()
    

    # Print summary statistics
    print("Summary statistics for top 5 commodities across regions:")
    print(pivot_prices.describe())

    # Find the commodity with the highest price variation across regions
    price_variation = pivot_prices.std()
    most_variable_commodity = price_variation.idxmax()
    print(f"\nCommodity with highest price variation across regions: {most_variable_commodity}")
    print(f"Price range: ${pivot_prices[most_variable_commodity].min():.2f} - ${pivot_prices[most_variable_commodity].max():.2f}")

    # Calculate percentage difference between highest and lowest price for each commodity
    for commodity in top_commodities:
        min_price = pivot_prices[commodity].min()
        max_price = pivot_prices[commodity].max()
        pct_difference = ((max_price - min_price) / min_price) * 100
        print(f"\n{commodity}:")
        print(f"Lowest price: ${min_price:.2f} (Region: {pivot_prices[commodity].idxmin()})")
        print(f"Highest price: ${max_price:.2f} (Region: {pivot_prices[commodity].idxmax()})")
        print(f"Percentage difference: {pct_difference:.2f}%")
    
    return plt,min_price 
@st.cache_data
def run_regression(df):
   
    features = ['country_name', 'unit_measure_id', 'price_month', 'price_year', 'commodity_category']
    target = 'price_usd'

    X = df[features]
    y = df[target]

    encoder = OneHotEncoder(handle_unknown="ignore")
    # One-hot encode categorical features and scale numerical features
    preprocessor = ColumnTransformer(transformers=[
    ('cat', OneHotEncoder(), ['country_name','unit_measure_id' , 'commodity_category']),
    ('num', StandardScaler(), ['price_month', 'price_year'])
    ])


        # Polynomial degree (adjust this as needed)
    poly = PolynomialFeatures(degree=2)

    # Create a pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('poly', poly),
        ('regressor', LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    print("Model trained successfully.")

    y_pred = pipeline.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return pipeline, y_test, y_pred, r2, mse

@st.cache_data
def residual_analysis(df):
    # Code for residual analysis, plotting etc.
    pass


