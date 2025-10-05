"""
Feature engineering for financial data analysis.
"""
import pandas as pd
import numpy as np
from typing import Optional


def calculate_returns(df: pd.DataFrame, column: str = 'close') -> pd.DataFrame:
    """
    Calculate daily returns.
    
    Args:
        df: DataFrame with price data
        column: Price column to use for calculation
        
    Returns:
        DataFrame with returns column added
    """
    df = df.copy()
    df['daily_return'] = df[column].pct_change()
    return df


def calculate_moving_averages(
    df: pd.DataFrame, 
    column: str = 'close',
    windows: list = [20, 50, 200]
) -> pd.DataFrame:
    """
    Calculate moving averages for specified windows.
    
    Args:
        df: DataFrame with price data
        column: Price column to use
        windows: List of window sizes for moving averages
        
    Returns:
        DataFrame with MA columns added
    """
    df = df.copy()
    
    for window in windows:
        df[f'ma_{window}'] = df[column].rolling(window=window).mean()
    
    return df


def calculate_rsi(df: pd.DataFrame, column: str = 'close', period: int = 14) -> pd.DataFrame:
    """
    Calculate Relative Strength Index (RSI).
    
    Args:
        df: DataFrame with price data
        column: Price column to use
        period: RSI period (default 14)
        
    Returns:
        DataFrame with RSI column added
    """
    df = df.copy()
    
    # Calculate price changes
    delta = df[column].diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    
    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df


def calculate_bollinger_bands(
    df: pd.DataFrame, 
    column: str = 'close',
    window: int = 20,
    num_std: float = 2.0
) -> pd.DataFrame:
    """
    Calculate Bollinger Bands.
    
    Args:
        df: DataFrame with price data
        column: Price column to use
        window: Moving average window
        num_std: Number of standard deviations for bands
        
    Returns:
        DataFrame with Bollinger Bands columns added
    """
    df = df.copy()
    
    # Calculate middle band (SMA)
    df['bb_middle'] = df[column].rolling(window=window).mean()
    
    # Calculate standard deviation
    std = df[column].rolling(window=window).std()
    
    # Calculate upper and lower bands
    df['bb_upper'] = df['bb_middle'] + (std * num_std)
    df['bb_lower'] = df['bb_middle'] - (std * num_std)
    
    return df


def calculate_macd(
    df: pd.DataFrame,
    column: str = 'close',
    fast: int = 12,
    slow: int = 26,
    signal: int = 9
) -> pd.DataFrame:
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    Args:
        df: DataFrame with price data
        column: Price column to use
        fast: Fast EMA period
        slow: Slow EMA period
        signal: Signal line period
        
    Returns:
        DataFrame with MACD columns added
    """
    df = df.copy()
    
    # Calculate EMAs
    ema_fast = df[column].ewm(span=fast, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow, adjust=False).mean()
    
    # Calculate MACD line
    df['macd'] = ema_fast - ema_slow
    
    # Calculate signal line
    df['macd_signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
    
    # Calculate histogram
    df['macd_histogram'] = df['macd'] - df['macd_signal']
    
    return df


def calculate_volatility(
    df: pd.DataFrame,
    column: str = 'close',
    window: int = 20
) -> pd.DataFrame:
    """
    Calculate rolling volatility (standard deviation of returns).
    
    Args:
        df: DataFrame with price data
        column: Price column to use
        window: Rolling window size
        
    Returns:
        DataFrame with volatility column added
    """
    df = df.copy()
    
    # Calculate returns if not already present
    if 'daily_return' not in df.columns:
        df['daily_return'] = df[column].pct_change()
    
    # Calculate rolling volatility
    df['volatility'] = df['daily_return'].rolling(window=window).std()
    
    # Annualize volatility (assuming 252 trading days)
    df['volatility_annualized'] = df['volatility'] * np.sqrt(252)
    
    return df


def add_all_features(df: pd.DataFrame, column: str = 'close') -> pd.DataFrame:
    """
    Add all common technical indicators to the DataFrame.
    
    Args:
        df: DataFrame with price data
        column: Price column to use
        
    Returns:
        DataFrame with all features added
    """
    df = calculate_returns(df, column)
    df = calculate_moving_averages(df, column, [20, 50, 200])
    df = calculate_rsi(df, column)
    df = calculate_bollinger_bands(df, column)
    df = calculate_macd(df, column)
    df = calculate_volatility(df, column)
    
    return df


