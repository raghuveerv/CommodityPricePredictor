import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def plot_price_trend(df):
    """Generate a line plot for price trends over time by country with Streamlit integration."""
    # Prepare data
    df['date'] = pd.to_datetime(df[['price_year', 'price_month']]
                               .rename(columns={'price_year': 'year', 'price_month': 'month'})
                               .assign(day=1))
    
    # Create plot
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.lineplot(data=df, x='date', y='price', hue='country_name', marker="o")
    plt.title('Price Trend Over Time by Country')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # Generate insights
    overall_trend = np.polyfit(range(len(df['date'].unique())), 
                              df.groupby('date')['price'].mean(), 1)[0]
    trend_direction = "increasing" if overall_trend > 0 else "decreasing"
    
    stats_by_country = df.groupby('country_name')['price'].agg(['mean', 'std', 'min', 'max'])
    highest_price_country = stats_by_country['max'].idxmax()
    lowest_price_country = stats_by_country['min'].idxmin()
    most_volatile_country = stats_by_country['std'].idxmax()
    
    # Display insights in Streamlit
    with st.expander("📊 View Price Trend Insights"):
        st.markdown(f"""
        **Key Insights:**
        - 📈 Overall price trend is **{trend_direction}** across all countries
        - 🔺 Highest recorded price was in **{highest_price_country}**
        - 🔻 Lowest recorded price was in **{lowest_price_country}**
        - 📊 **{most_volatile_country}** shows the highest price volatility
        """)
    
    return fig

@st.cache_data
def plot_boxplot_by_country(df):
    """Generate a boxplot for price distribution by country with Streamlit integration."""
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.boxplot(data=df, x='country_name', y='price')
    plt.title('Price Distribution by Country')
    plt.xlabel('Country')
    plt.ylabel('Price in USD')
    plt.xticks(rotation=45)
    
    # Calculate statistics
    stats = df.groupby('country_name')['price'].agg(['median', 'mean', 'std', 'skew'])
    
    highest_median = stats['median'].idxmax()
    lowest_median = stats['median'].idxmin()
    most_spread = stats['std'].idxmax()
    most_skewed = stats['skew'].abs().idxmax()
    
    # Display insights in Streamlit
    with st.expander("📊 View Price Distribution Insights"):
        st.markdown(f"""
        **Key Insights:**
        - 📊 Median prices are highest in **{highest_median}** and lowest in **{lowest_median}**
        - 📈 **{most_spread}** shows the widest price spread, indicating high variability
        - 📉 **{most_skewed}** has the most skewed price distribution, suggesting frequent price extremes
        
        **Price Statistics by Country:**
        """)
        
        # Create a formatted DataFrame for display
        display_stats = stats.round(2)
        display_stats.columns = ['Median Price', 'Mean Price', 'Std Dev', 'Skewness']
        st.dataframe(display_stats)
    
    return fig

@st.cache_data
def plot_commodity_price(df, commodity_name):
    """Generate a line plot for a specific commodity's price trend with Streamlit integration."""
    # Filter for the selected commodity
    df_commodity = df[df['cm_name'] == commodity_name]
    
    # Prepare data
=======
    df_commodity = df[df['commodity_category'] == commodity_name]
    # Rename columns and convert to datetime format

    df_commodity['date'] = pd.to_datetime(df_commodity[['price_year', 'price_month']]
                                        .rename(columns={'price_year': 'year', 'price_month': 'month'})
                                        .assign(day=1))
    
    # Create plot
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.lineplot(data=df_commodity, x='date', y='price', hue='country_name', marker="o")
    plt.title(f'{commodity_name} Price Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # Generate insights
    start_date = df_commodity['date'].min()
    end_date = df_commodity['date'].max()
    
    # Calculate total price change
    price_series = df_commodity.groupby('date')['price'].mean()
    total_change = ((price_series.iloc[-1] - price_series.iloc[0]) / price_series.iloc[0] * 100)
    
    price_stats = df_commodity.groupby('country_name')['price'].agg(['mean', 'std'])
    most_expensive_market = price_stats['mean'].idxmax()
    most_stable_market = price_stats['std'].idxmin()
    
    # Seasonal analysis
    df_commodity['month'] = df_commodity['date'].dt.month
    monthly_avg = df_commodity.groupby('month')['price'].mean()
    peak_month = monthly_avg.idxmax()
    trough_month = monthly_avg.idxmin()
    
    # Display insights in Streamlit
    with st.expander(f"📊 View {commodity_name} Price Insights"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Time Period Analysis:**
            - 📅 Analysis period: {start_date.strftime('%Y-%m')} to {end_date.strftime('%Y-%m')}
            - 📈 Total price change: {total_change:.1f}%
            """)
            
        with col2:
            st.markdown(f"""
            **Market Analysis:**
            - 🏪 Highest prices: **{most_expensive_market}**
            - 📊 Most stable market: **{most_stable_market}**
            """)
        
        st.markdown(f"""
        **Seasonal Patterns:**
        - 📈 Peak prices typically occur in month {peak_month}
        - 📉 Lowest prices typically occur in month {trough_month}
        """)
        
        # Show price statistics table
        st.markdown("**Price Statistics by Country:**")
        display_stats = price_stats.round(2)
        display_stats.columns = ['Average Price', 'Price Volatility']
        st.dataframe(display_stats)
    
    return fig