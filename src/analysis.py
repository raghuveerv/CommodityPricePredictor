# src/analysis.py
import pandas as pd
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

def calculate_correlation(df):
    correlation, p_value = pearsonr(df['price_year'], df['price_usd'])
    print(f"Pearson correlation coefficient: {correlation}")
    print(f"P-value: {p_value}")

def run_regression(df):
    X = df[['price_year', 'price_month']]
    y = df['price_usd']
    pipeline = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('poly', PolynomialFeatures(degree=2)),
        ('regressor', LinearRegression())
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    print("Model trained successfully.")

def residual_analysis(df):
    # Code for residual analysis, plotting etc.
    pass
