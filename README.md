# Global Food Price Analysis and Prediction

## Abstract
This project develops a web application for analyzing and predicting global food prices. The tool provides insights into historical price trends and forecasts future prices for various commodities across regions and market types (Retail, Wholesale, Producer, Farm Gate). Using data-driven analysis and machine learning models, we aim to assist stakeholders—such as farmers, traders, policymakers, and researchers—in making informed decisions that address challenges like food security, price volatility, and market planning.

## Stakeholder Benefits
Our tool benefits various stakeholders:
- **Farmers**: Informed decisions on crop selection and timing of sales.
- **Traders**: Optimization of buying and selling strategies.
- **Policymakers**: Insights into regional price disparities for food security planning.
- **Researchers**: Access to organized datasets for advanced analysis.
- **Consumers**: Clear visualization of trends to make informed purchasing decisions.

The application stands out in its ability to:
- Visualize historical price trends.
- Compare prices across regions and commodities.
- Provide accurate, data-driven predictions of future price movements.

## Data Description
The analysis relies on the **Global Food Prices Dataset** from [Kaggle](https://www.kaggle.com/datasets/jboysen/global-food-prices/data), containing:
- **Country/Region Information**: Geographic indicators for regional comparisons.
- **Commodity Data**: Prices of food items like rice, pork, chicken, and more.
- **Market Types**: Retail, wholesale, and producer-level market prices.
- **Price Details**: In both local currency and USD.
- **Timestamps**: Month and year of recorded prices.

### Data Cleaning and Preprocessing
1. **Filtering**: Focused on five countries: Cambodia, Lao People's Democratic Republic, Myanmar, Philippines, Timor-Leste.
2. **Deduplication**: Removed duplicate entries for consistency.
3. **Handling Missing Values**: Kept the missing values as it was not affecting the predictions.
4. **Standardization**: Converted prices to USD to allow global comparisons.
5. **Feature Engineering**: Added new features like:
   - Year and month indicators.
   - Seasonal flags for detecting seasonal trends.

## Algorithm Description
### Exploratory Data Analysis (EDA)
- **Trend Analysis**: Time series decomposition to identify long-term trends and seasonality.
- **Regional Comparisons**: Analyzed regional differences and patterns.
- **Correlation Analysis**: Studied the relationship between variables such as price, region, and market type.
- **Distribution Analysis**: Investigated price distribution across regions and commodities.

### Predictive Modeling
- **Baseline Model**: Linear Regression to establish basic predictive performance.
- **Advanced Models**:
  - **Random Forest Regressor**: For capturing complex interactions between features.
  - **XGBoost**: For accurate predictions using boosted decision trees.
- **Feature Engineering**:
  - Lag features and rolling averages for time series forecasting.
  - Temporal features like seasonality indicators.
- **Validation**: Time series cross-validation to evaluate model performance.

### Visualization Algorithms
- **Time Series Plots**: For understanding price trends over time.
- **Box Plots**: To visualize the distribution of prices and detect outliers.
- **Heatmaps**: Correlation analysis for features like commodity type, region, and market conditions.

## Tools Used
- **Programming Language**: Python
- **Data Analysis and Processing**:
  - Pandas and NumPy: For efficient data manipulation and computations.
  - Statsmodels: For time series analysis and trend decomposition.
- **Visualization**:
  - Matplotlib and Seaborn: For generating detailed, interactive plots.
- **Machine Learning**:
  - Scikit-learn: Implemented machine learning models.
  - XGBoost: Enhanced predictive accuracy through boosting.
- **Web Application**:
  - Streamlit: Built an interactive, user-friendly web interface.
  - Backblaze B2: Cloud storage for hosting datasets.
- **Development Environment**:
  - Google Colab: For EDA and iterative development.

## Ethical Concerns

### Data Knowledge
- **Concern**:  
  - Certain anomalies in the dataset, such as wages being listed as a commodity and "day" appearing as a unit of measurement, raise questions about the reliability and context of these entries.  
- **Mitigation**:  
  - While these inconsistencies did not impact the predictions, further validation and consolidation with original data sources or additional datasets are   needed to understand and address these anomalies.
    
### Price Conversion Inconsistency  
- **Concern**:  
  - The current price conversion values are static, and do not reflect real-time exchange rates. This could lead to discrepancies in pricing data when comparing across different currencies.  
- **Mitigation**:  
  - To address this issue, dynamic price conversions can be implemented by integrating an API, such as [exchangeratesapi](https://exchangeratesapi.io/), to fetch up-to-date exchange rates. This will ensure that the price conversions are accurate and reflect the current market rates.
    
### Data Representation
- **Concern**: 
  -Limited regional coverage might not represent global trends.
- **Mitigation**:
  - Documented data limitations in the app.
  - Plans to incorporate additional datasets for better global representation.

### Prediction Accuracy
- **Concern**: Over-reliance on predictions [not accurate] may lead to poor decision-making.
- **Mitigation**:
  - Include confidence intervals for predictions.

### Accessibility
- **Concern**: Digital divide might limit access for certain users.
- **Mitigation**:
  - Designed a mobile-friendly, intuitive interface.
  - Provided descriptions for the user to understand what the buttons do.

---

## Commit Guidelines
We followed best practices for version control:
- Regular commits after implementing features or fixing bugs.
- Clear and descriptive commit messages to maintain a robust version history.

---

This web application empowers users with actionable insights into food prices, contributing to better decision-making and fostering transparency in global commodity markets.
