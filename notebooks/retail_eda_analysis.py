# =================================================================
# RETAIL STORE PERFORMANCE & EXPLORATORY DATA ANALYSIS (EDA)
# Toolstack: Python (Pandas, NumPy, Matplotlib, Seaborn)
# Author: Soumya
# =================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual styling for charts
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# -----------------------------------------------------------------
# 1. DATA LOADING & INSPECTION
# -----------------------------------------------------------------
def load_data(file_path):
    """Loads dataset and prints basic structural info."""
    df = pd.read_csv(file_path)
    print("Dataset Shape:", df.shape)
    print("\nColumn Information:")
    print(df.info())
    print("\nMissing Values:")
    print(df.isnull().sum())
    return df

# -----------------------------------------------------------------
# 2. DATA CLEANING & PREPROCESSING
# -----------------------------------------------------------------
def clean_data(df):
    """Handles missing values, date formats, and derived features."""
    # Convert date column to datetime format
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Fill or drop missing values if present
    df['category_name'] = df['category_name'].fillna('Uncategorized')
    
    # Extract temporal features for time-series analysis
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month_name()
    df['month_num'] = df['order_date'].dt.month
    
    # Calculate Total Amount per transaction if not already present
    if 'total_amount' not in df.columns:
        df['total_amount'] = df['quantity'] * df['unit_price']
        
    return df

# -----------------------------------------------------------------
# 3. EXPLORATORY DATA ANALYSIS (EDA) & SUMMARY METRICS
# -----------------------------------------------------------------
def generate_kpis(df):
    """Calculates high-level executive performance metrics."""
    total_revenue = df['total_amount'].sum()
    total_orders = df['order_id'].nunique()
    avg_order_value = df['total_amount'].mean()
    unique_customers = df['customer_id'].nunique()
    
    print("=" * 40)
    print(" EXECUTIVE KPI SUMMARY ")
    print("=" * 40)
    print(f"Total Revenue (INR)     : ₹{total_revenue:,.2f}")
    print(f"Total Orders Processed  : {total_orders:,}")
    print(f"Average Order Value     : ₹{avg_order_value:,.2f}")
    print(f"Total Unique Customers  : {unique_customers:,}")
    print("=" * 40)

def category_performance(df):
    """Analyzes sales performance across product categories."""
    cat_summary = df.groupby('category_name').agg(
        Total_Revenue=('total_amount', 'sum'),
        Order_Count=('order_id', 'nunique'),
        Avg_Order_Value=('total_amount', 'mean')
    ).reset_index().sort_values(by='Total_Revenue', ascending=False)
    
    cat_summary['Revenue_Share_%'] = (cat_summary['Total_Revenue'] / df['total_amount'].sum()) * 100
    return cat_summary

# -----------------------------------------------------------------
# 4. MAIN EXECUTION PIPELINE (SAMPLE RUN)
# -----------------------------------------------------------------
if __name__ == "__main__":
    print("Retail EDA Pipeline Script Ready.")
