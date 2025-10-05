"""
Data cleaning and preprocessing utilities.
"""
import pandas as pd
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean stock price data by handling missing values and outliers.
    
    Args:
        df: Raw stock price DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    if df is None or df.empty:
        return df
    
    df = df.copy()
    
    # Remove rows with all NaN values
    df.dropna(how='all', inplace=True)
    
    # Forward fill missing values (use previous valid value)
    df.fillna(method='ffill', inplace=True)
    
    # If still have NaN at the beginning, backward fill
    df.fillna(method='bfill', inplace=True)
    
    # Ensure numeric columns are proper type
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'adjusted_close']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def detect_outliers(df: pd.DataFrame, column: str, threshold: float = 3.0) -> pd.Series:
    """
    Detect outliers using z-score method.
    
    Args:
        df: DataFrame with data
        column: Column name to check for outliers
        threshold: Z-score threshold (default 3.0)
        
    Returns:
        Boolean Series indicating outliers
    """
    if column not in df.columns:
        return pd.Series([False] * len(df))
    
    mean = df[column].mean()
    std = df[column].std()
    
    z_scores = np.abs((df[column] - mean) / std)
    return z_scores > threshold


def normalize_data(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Normalize specified columns to 0-1 range.
    
    Args:
        df: DataFrame with data
        columns: List of column names to normalize
        
    Returns:
        DataFrame with normalized columns
    """
    df = df.copy()
    
    for col in columns:
        if col in df.columns:
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val > min_val:
                df[col] = (df[col] - min_val) / (max_val - min_val)
    
    return df


def aggregate_to_period(df: pd.DataFrame, period: str = 'W') -> pd.DataFrame:
    """
    Aggregate daily data to a different period (weekly, monthly, etc.).
    
    Args:
        df: DataFrame with daily data and datetime index
        period: Pandas period alias ('W' for weekly, 'M' for monthly, etc.)
        
    Returns:
        Aggregated DataFrame
    """
    if 'date' in df.columns:
        df = df.set_index('date')
    
    agg_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }
    
    # Only include columns that exist
    agg_dict = {k: v for k, v in agg_dict.items() if k in df.columns}
    
    df_agg = df.resample(period).agg(agg_dict)
    
    return df_agg.reset_index()


