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


def calculate_correlation(df):
    correlation, p_value = pearsonr(df['price_year'], df['price_usd'])
    return correlation, p_value

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


