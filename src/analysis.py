# src/analysis.py
import pandas as pd
import streamlit as st
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score

import numpy as np

@st.cache_data
def calculate_correlation_with_insights(df):
    """
    Calculate correlation between year and price with detailed insights.
    Returns correlation statistics and interpretation.
    """
    correlation, p_value = pearsonr(df['price_year'], df['price'])
    
    # Calculate additional statistics for insights
    yearly_avg = df.groupby('price_year')['price'].mean()
    total_change = ((yearly_avg.iloc[-1] - yearly_avg.iloc[0]) / yearly_avg.iloc[0]) * 100
    
    # Determine correlation strength
    def get_correlation_strength(corr):
        abs_corr = abs(corr)
        if abs_corr < 0.3:
            return "weak"
        elif abs_corr < 0.7:
            return "moderate"
        else:
            return "strong"
    
    # Determine statistical significance
    is_significant = p_value < 0.05
    
    # Calculate year-over-year changes
    yoy_changes = yearly_avg.pct_change() * 100
    max_increase = yoy_changes.max()
    max_decrease = yoy_changes.min()
    max_increase_year = yoy_changes.idxmax()
    max_decrease_year = yoy_changes.idxmin()
    
    # Format insights based on analysis
    with st.expander("📊 View Correlation Analysis Insights"):
        # Main correlation statistics
        st.markdown(f"""
        **Correlation Statistics:**
        - 📈 Correlation coefficient: **{correlation:.3f}**
        - 🎯 P-value: **{p_value:.4f}**
        """)
        
        # Interpretation
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Interpretation:**")
            st.markdown(f"""
            - 💫 The correlation is **{get_correlation_strength(correlation)}**
            - 🎯 The relationship is statistically {'significant' if is_significant else 'not significant'}
            - 📈 The correlation is {'positive' if correlation > 0 else 'negative'}
            """)
        
        with col2:
            st.markdown("**Price Trends:**")
            st.markdown(f"""
            - 📊 Total price change: **{total_change:.1f}%**
            - ⬆️ Largest yearly increase: **{max_increase:.1f}%** ({max_increase_year})
            - ⬇️ Largest yearly decrease: **{max_decrease:.1f}%** ({max_decrease_year})
            """)
        
        # Detailed interpretation
        st.markdown("**What This Means:**")
        
        interpretation = []
        
        # Correlation direction interpretation
        if correlation > 0:
            interpretation.append("- 📈 Prices tend to **increase** over the years")
        else:
            interpretation.append("- 📉 Prices tend to **decrease** over the years")
        
        # Statistical significance interpretation
        if is_significant:
            interpretation.append("- ✅ This trend is **statistically significant**, suggesting a reliable pattern")
        else:
            interpretation.append("- ⚠️ This trend is **not statistically significant**, suggesting high variability")
        
        # Strength interpretation
        strength = get_correlation_strength(correlation)
        if strength == "strong":
            interpretation.append("- 💪 The relationship is **strong**, indicating consistent price changes over time")
        elif strength == "moderate":
            interpretation.append("- 📊 The relationship is **moderate**, showing some consistency in price changes")
        else:
            interpretation.append("- 🔄 The relationship is **weak**, suggesting highly variable price changes")
        
        # Price volatility interpretation
        if abs(max_increase) > 20 or abs(max_decrease) > 20:
            interpretation.append("- ⚠️ Significant price volatility observed with large year-over-year changes")
        
        st.markdown("\n".join(interpretation))
        
        # Show yearly price trends
        st.markdown("\n**Yearly Price Trends:**")
        yearly_trend_df = pd.DataFrame({
            'Average Price': yearly_avg.round(2),
            'YoY Change %': yoy_changes.round(2)
        })
        st.dataframe(yearly_trend_df)
    
    return correlation, p_value

def display_data_insights(df):
    """
    Display key insights for the dataset focusing on essential information.
    """
    
    with st.expander("📊 View Dataset Insights", expanded=True):
        # Basic dataset information
        st.markdown(f"""
        **Dataset Overview:**
        - 🔢 Total Records: {len(df):,}
        - 📅 Time Period: {df['price_year'].min()} - {df['price_year'].max()}
        - 🌍 Countries: {df['country_name'].nunique()}
        - 🛒 Commodities: {df['cm_name'].nunique()}
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Price Analysis
            st.markdown("**Price Summary (USD)**")
            price_stats = {
                'Average Price': f"${df['price'].mean():.2f}",
                'Median Price': f"${df['price'].median():.2f}",
                'Price Range': f"${df['price'].min():.2f} - ${df['price'].max():.2f}",
                'Price Volatility': f"{df['price'].std():.2f}"
            }
            for key, value in price_stats.items():
                st.markdown(f"- {key}: **{value}**")
        
        with col2:
            # Top commodities and markets
            st.markdown("**Key Findings**")
            # Most expensive commodity
            top_commodity = df.groupby('cm_name')['price'].mean().idxmax()
            top_commodity_price = df.groupby('cm_name')['price'].mean().max()
            
            # Most expensive market
            top_market = df.groupby('country_name')['price'].mean().idxmax()
            top_market_price = df.groupby('country_name')['price'].mean().max()
            
            st.markdown(f"""
            - 📈 Most Expensive Commodity: **{top_commodity}** (${top_commodity_price:.2f})
            - 🏪 Highest Price Market: **{top_market}** (${top_market_price:.2f})
            - 📅 Most Recent Update: **{df['price_year'].max()}-{df['price_month'].max()}**
            - 🌐 Data Points per Country: **{len(df) // df['country_name'].nunique():,}** (avg)
            """)

    return None

=======
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
    target = 'price'
    
    X = df[features]
    y = df[target]
    
    # One-hot encode categorical features and scale numerical features
    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(handle_unknown="ignore"), ['country_name','unit_measure_id', 'commodity_category']),
        ('num', StandardScaler(), ['price_month', 'price_year'])
    ])
    
    # Create pipeline with Random Forest
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=100,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            max_depth=None,
            bootstrap=True,
            random_state=42,
            n_jobs=-1  # Use all CPU cores
        ))
    ])
    
    # Optional: Perform hyperparameter tuning
    param_dist = {
        'regressor__n_estimators': [100, 200, 300],
        'regressor__max_depth': [None, 10, 20, 30],
        'regressor__min_samples_split': [2, 5, 10],
        'regressor__min_samples_leaf': [1, 2, 4]
    }
    
    random_search = RandomizedSearchCV(
        pipeline,
        param_distributions=param_dist,
        n_iter=10,
        cv=3,
        random_state=42,
        n_jobs=-1
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Fit the model
    random_search.fit(X_train, y_train)
    pipeline = random_search.best_estimator_
    print("Model trained successfully.")
    print(f"Best parameters: {random_search.best_params_}")
    
    # Make predictions
    y_pred = pipeline.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return pipeline, y_test, y_pred, r2, mse

@st.cache_data
def residual_analysis(df):
    # Code for residual analysis, plotting etc.
    pass


