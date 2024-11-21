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

def calculate_correlation(df):
    correlation, p_value = pearsonr(df['price_year'], df['price_usd'])
    return correlation, p_value

@st.cache_data

def run_regression(df):
    features = ['country_name', 'unit_measure_id', 'price_month', 'price_year', 'commodity_category']
    target = 'price_usd'
    
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


