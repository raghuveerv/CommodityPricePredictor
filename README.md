# CommodityPricePredictor

## Abstract/ Overview:

The primary goal of this project is to develop a user-friendly web application that empowers users to analyze and predict commodity prices. 
The app offers two key features:

- Price Trend Analysis: Users can explore historical price trends for various commodities across different regions and market types. By visualizing data over time, they gain insights into how geographic location, local market conditions, and market types (e.g., retail, wholesale) influence prices.

- Price Prediction: The app integrates a predictive model to forecast future commodity prices based on historical data. This feature assists users in making strategic decisions about when and where to buy or sell goods, enhancing their ability to optimize costs and maximize profitability.
Stakeholders, including farmers, traders, and market analysts, will find this tool invaluable for planning and decision-making. It provides actionable insights into market dynamics, allowing users to anticipate price fluctuations and make data-driven choices.

## Data Description

The dataset used in this project is sourced from Kaggle and contains global food prices across various countries. It includes a mix of numerical, categorical, and temporal data, with columns such as country names, commodity names, market types, prices, units of measurement, and timestamps (month and year).

Originally, the dataset comprised approximately 740,000 rows, covering over 150 countries. To focus the analysis, we divided the data into four regions: Central America, South Asia, Southeast Asia, and the Middle East, each containing its respective set of countries.

Basic data cleaning and preprocessing were performed to enhance data quality and consistency. This included renaming columns for clarity, filtering data by relevant years, removing duplicate entries, and standardizing all prices by converting local currencies to USD. 

## Algorithm Description

### 1. Price Prediction Algorithm

#### Dataset Preprocessing:
* Filter historical price data by region/country
* Normalize prices to account for inflation and currency differences
* Group by commodity categories

#### Prediction Process:
* Input: Country, Year, Month, Commodity
* Apply filtering conditions simultaneously
* Calculate predicted price based on:
  - Historical price trends
  - Seasonal patterns
  - Regional market conditions
* Output: Predicted price value

### 2. Data Analysis Algorithm

#### Time Series Analysis:
* Split data into temporal components
* Calculate moving averages
* Identify seasonal patterns
* Detect price trends

#### Statistical Processing:
* Compute correlation between time and prices
* Generate summary statistics:
  - Mean prices by region
  - Price volatility
  - Year-over-year changes
* Calculate confidence intervals

### 3. Visualization Algorithm

#### Price Trend Generation:
* Group data by time periods
* Apply smoothing techniques
* Plot time series with:
  - X-axis: Timeline
  - Y-axis: Normalized prices
  - Color coding by region/commodity

#### Distribution Analysis:
* Calculate statistical measures:
  - Quartiles
  - Median values
  - Price ranges
* Generate box plots for price distribution
* Highlight outliers

### 4. Interactive Filtering Algorithm

#### User Input Processing:
* Capture selection parameters
* Validate input combinations
* Update data subset

#### Real-time Update:
* Recalculate statistics
* Refresh visualizations
* Update predictions

