"""
Historical performance analysis utilities.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict


def calculate_period_return(
    df: pd.DataFrame,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    price_column: str = 'close'
) -> float:
    """
    Calculate return over a specific period.
    
    Args:
        df: DataFrame with price data
        start_date: Period start date (None = first available)
        end_date: Period end date (None = last available)
        price_column: Column name for prices
        
    Returns:
        Return as percentage
    """
    if df.empty:
        return 0.0
    
    df_filtered = df.copy()
    
    if 'date' in df.columns:
        df_filtered['date'] = pd.to_datetime(df_filtered['date'])
        if start_date:
            df_filtered = df_filtered[df_filtered['date'] >= start_date]
        if end_date:
            df_filtered = df_filtered[df_filtered['date'] <= end_date]
    
    if df_filtered.empty or len(df_filtered) < 2:
        return 0.0
    
    start_price = df_filtered.iloc[0][price_column]
    end_price = df_filtered.iloc[-1][price_column]
    
    return ((end_price - start_price) / start_price) * 100


def calculate_max_drawdown(df: pd.DataFrame, price_column: str = 'close') -> Dict:
    """
    Calculate maximum drawdown.
    
    Args:
        df: DataFrame with price data
        price_column: Column name for prices
        
    Returns:
        Dictionary with max drawdown info
    """
    if df.empty:
        return {'max_drawdown': 0, 'peak': 0, 'trough': 0}
    
    prices = df[price_column].values
    
    # Calculate running maximum
    running_max = np.maximum.accumulate(prices)
    
    # Calculate drawdown
    drawdown = (prices - running_max) / running_max * 100
    
    max_dd_idx = np.argmin(drawdown)
    max_dd = drawdown[max_dd_idx]
    
    # Find the peak before the max drawdown
    peak_idx = np.argmax(running_max[:max_dd_idx + 1])
    
    return {
        'max_drawdown': max_dd,
        'max_drawdown_pct': abs(max_dd),
        'peak_value': prices[peak_idx],
        'trough_value': prices[max_dd_idx],
        'peak_index': peak_idx,
        'trough_index': max_dd_idx
    }


def calculate_volatility(df: pd.DataFrame, price_column: str = 'close') -> Dict:
    """
    Calculate various volatility metrics.
    
    Args:
        df: DataFrame with price data
        price_column: Column name for prices
        
    Returns:
        Dictionary with volatility metrics
    """
    if df.empty or len(df) < 2:
        return {'daily_volatility': 0, 'annualized_volatility': 0}
    
    # Calculate daily returns
    returns = df[price_column].pct_change().dropna()
    
    daily_vol = returns.std()
    annualized_vol = daily_vol * np.sqrt(252)  # 252 trading days per year
    
    return {
        'daily_volatility': daily_vol * 100,
        'annualized_volatility': annualized_vol * 100,
        'mean_return': returns.mean() * 100,
        'median_return': returns.median() * 100
    }


def calculate_sharpe_ratio(
    df: pd.DataFrame,
    price_column: str = 'close',
    risk_free_rate: float = 0.02
) -> float:
    """
    Calculate Sharpe ratio.
    
    Args:
        df: DataFrame with price data
        price_column: Column name for prices
        risk_free_rate: Annual risk-free rate (default 2%)
        
    Returns:
        Sharpe ratio
    """
    if df.empty or len(df) < 2:
        return 0.0
    
    # Calculate daily returns
    returns = df[price_column].pct_change().dropna()
    
    # Annualize returns
    mean_return = returns.mean() * 252
    std_return = returns.std() * np.sqrt(252)
    
    if std_return == 0:
        return 0.0
    
    sharpe = (mean_return - risk_free_rate) / std_return
    
    return sharpe


def calculate_performance_metrics(df: pd.DataFrame, price_column: str = 'close') -> Dict:
    """
    Calculate comprehensive performance metrics.
    
    Args:
        df: DataFrame with price data
        price_column: Column name for prices
        
    Returns:
        Dictionary with all performance metrics
    """
    if df.empty:
        return {}
    
    metrics = {}
    
    # Period returns
    metrics['total_return'] = calculate_period_return(df, price_column=price_column)
    
    # Time-specific returns
    now = datetime.now()
    metrics['ytd_return'] = calculate_period_return(
        df, 
        start_date=datetime(now.year, 1, 1),
        price_column=price_column
    )
    metrics['1y_return'] = calculate_period_return(
        df,
        start_date=now - timedelta(days=365),
        price_column=price_column
    )
    
    # Volatility
    vol_metrics = calculate_volatility(df, price_column)
    metrics.update(vol_metrics)
    
    # Drawdown
    dd_metrics = calculate_max_drawdown(df, price_column)
    metrics.update(dd_metrics)
    
    # Sharpe ratio
    metrics['sharpe_ratio'] = calculate_sharpe_ratio(df, price_column)
    
    # Price statistics
    metrics['current_price'] = df.iloc[-1][price_column]
    metrics['high_52week'] = df[price_column].tail(252).max()
    metrics['low_52week'] = df[price_column].tail(252).min()
    
    return metrics


def compare_performance(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    name1: str = "Asset 1",
    name2: str = "Asset 2"
) -> pd.DataFrame:
    """
    Compare performance of two assets.
    
    Args:
        df1: First asset's price data
        df2: Second asset's price data
        name1: Name of first asset
        name2: Name of second asset
        
    Returns:
        DataFrame with comparison metrics
    """
    metrics1 = calculate_performance_metrics(df1)
    metrics2 = calculate_performance_metrics(df2)
    
    comparison = pd.DataFrame({
        name1: metrics1,
        name2: metrics2
    })
    
    return comparison.T


