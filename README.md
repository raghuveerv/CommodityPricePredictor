# CommodityPricePredictor

Link to app: https://global-food-prices.streamlit.app/

## Abstract/ Overview:

The primary goal of this project is to develop a user-friendly web application that empowers users to analyze and predict commodity prices. 
The app offers two key features:

- Price Trend Analysis: Users can explore historical price trends for various commodities across different regions and market types. By visualizing data over time, they gain insights into how geographic location, local market conditions, and market types (e.g., retail, wholesale) influence prices.

- Price Prediction: The app integrates a predictive model to forecast future commodity prices based on historical data. This feature assists users in making strategic decisions about when and where to buy or sell goods, enhancing their ability to optimize costs and maximize profitability.
Stakeholders, including farmers, traders, and market analysts, will find this tool invaluable for planning and decision-making. It provides actionable insights into market dynamics, allowing users to anticipate price fluctuations and make data-driven choices.

## Data Description

Link: https://www.kaggle.com/datasets/jboysen/global-food-prices/data

The dataset used in this project is sourced from Kaggle and contains global food prices across various countries. It includes a mix of numerical, categorical, and temporal data, with columns such as country names, commodity names, market types, prices, units of measurement, and timestamps (month and year).

Originally, the dataset comprised approximately 740,000 rows, covering over 150 countries. To focus the analysis, we divided the data into four regions: Central America, South Asia, Southeast Asia, and the Middle East, each containing its respective set of countries.

Basic data cleaning and preprocessing were performed to enhance data quality and consistency. This included renaming columns for clarity, filtering data by relevant years, removing duplicate entries, and standardizing all prices by converting local currencies to USD. 

## Algorithm Description:

### 1. Price Prediction Algorithm using Random Forest

#### Model Architecture:
* Random Forest Regressor for price prediction
* Key features: country, commodity, month, year, market type
* Ensemble of decision trees reduces overfitting
* Handles both numerical and categorical variables effectively

#### Prediction Process:
* Input: Country, Year, Month, Commodity
* Feature preprocessing:
  - Encode categorical variables
  - Normalize numerical features
* Random Forest prediction based on:
  - Historical patterns
  - Seasonal trends
  - Market conditions
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

## Tools Used:

### Development Tools
* **Python** - Primary programming language for the application
* **Streamlit** - Web application framework for building interactive data apps
* **Pandas** - Data manipulation and analysis
* **NumPy** - Numerical computing and array operations

### Data Storage & Retrieval
* **Backblaze B2** - Cloud storage for hosting datasets
* **b2sdk** - Python SDK for Backblaze B2 integration

### Data Visualization
* **Matplotlib** - Foundation for creating static, animated, and interactive visualizations
* **Seaborn** - Statistical data visualization based on matplotlib
* Features implemented:
  - Line plots for time series analysis
  - Box plots for price distribution
  - Heat maps for correlation analysis
  - Statistical plots for trend analysis

### Styling & UI
* **CSS** - Custom styling for the web interface
* **HTML** - Structural elements and custom components
* **Streamlit Components** - Built-in widgets for interactive elements:
  - Dropdown menus
  - Sliders
  - Data filters

### Environment & Configuration
* **Python-dotenv** - Environment variable management
* **Requirements.txt** - Dependency management

## Ethical Concerns:

### 1. Data Ethics & Representation
**Concerns:**
* Dataset limited to four regions (Central America, South Asia, Southeast Asia, Middle East)
* Currency conversion to USD may mask local economic realities
* Historical data might not reflect current market conditions
* Potential data bias from regional/market gaps

**Mitigation:**
* Clearly document data limitations and regional coverage
* Include local currency options alongside USD
* Regular data updates and validation
* Transparent methodology documentation

### 2. User Access & Fairness
**Concerns:**
* Digital divide limiting access for some stakeholders
* Information asymmetry between large and small-scale users
* Varying levels of data literacy among users
* Language barriers

**Mitigation:**
* Develop mobile-friendly, simple interface
* Provide multi-language support
* Include educational resources and user guides
* Design intuitive visualizations

### 3. Market Impact
**Concerns:**
* Predictions could influence market behavior
* Potential misuse for price speculation
* Impact on small-scale farmers and local markets
* Over-reliance on predictions for critical decisions

**Mitigation:**
* Clear disclaimers about prediction limitations
* Monitor usage patterns for potential misuse
* Partner with agricultural organizations
* Provide context and confidence intervals with predictions

### 4. Responsible Development
**Ongoing Commitments:**
* Regular ethical audits and impact assessments
* Continuous user feedback integration
* Transparency in methodology updates
* Collaboration with market regulators and stakeholders
>>>>>>> main
