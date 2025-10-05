"""
Table display utilities for Streamlit.
"""
import pandas as pd
import streamlit as st
from typing import List, Optional
import sys
sys.path.append('..')
from config.settings import COLORS


def format_currency(value: float) -> str:
    """Format value as currency."""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format value as percentage."""
    return f"{value:.2f}%"


def format_large_number(value: float) -> str:
    """Format large numbers with K, M, B suffixes."""
    if value >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.2f}K"
    else:
        return f"${value:.2f}"


def style_gainers_losers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Style a DataFrame with gainers/losers.
    
    Args:
        df: DataFrame with change_percent column
        
    Returns:
        Styled DataFrame
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Format numeric columns
    if 'current_price' in df.columns:
        df['current_price'] = df['current_price'].apply(lambda x: f"${x:.2f}")
    
    if 'change' in df.columns:
        df['change'] = df['change'].apply(lambda x: f"${x:.2f}")
    
    if 'change_percent' in df.columns:
        df['change_percent'] = df['change_percent'].apply(lambda x: f"{x:.2f}%")
    
    if 'market_cap' in df.columns:
        df['market_cap'] = df['market_cap'].apply(format_large_number)
    
    return df


def display_stock_table(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    title: str = ""
) -> None:
    """
    Display a formatted stock table in Streamlit.
    
    Args:
        df: DataFrame to display
        columns: Optional list of columns to show
        title: Optional table title
    """
    if df.empty:
        st.warning("No data to display")
        return
    
    if title:
        st.subheader(title)
    
    if columns:
        df = df[columns]
    
    st.dataframe(df, use_container_width=True, hide_index=True)


def display_metrics_row(metrics: dict, num_columns: int = 4) -> None:
    """
    Display metrics in a row using Streamlit columns.
    
    Args:
        metrics: Dictionary with metric_name: (value, delta) pairs
        num_columns: Number of columns to use
    """
    cols = st.columns(num_columns)
    
    for i, (label, data) in enumerate(metrics.items()):
        col_idx = i % num_columns
        
        if isinstance(data, tuple):
            value, delta = data
            cols[col_idx].metric(label, value, delta)
        else:
            cols[col_idx].metric(label, data)


def create_summary_card(
    title: str,
    value: str,
    change: Optional[str] = None,
    positive: bool = True
) -> None:
    """
    Create a summary card with title, value, and optional change.
    
    Args:
        title: Card title
        value: Main value to display
        change: Optional change value
        positive: Whether change is positive
    """
    if change:
        st.metric(
            label=title,
            value=value,
            delta=change,
            delta_color="normal" if positive else "inverse"
        )
    else:
        st.metric(label=title, value=value)


def display_portfolio_table(holdings_df: pd.DataFrame) -> None:
    """
    Display portfolio holdings table with formatting.
    
    Args:
        holdings_df: DataFrame with portfolio holdings
    """
    if holdings_df.empty:
        st.info("No holdings in portfolio")
        return
    
    # Format the DataFrame
    display_df = holdings_df.copy()
    
    # Format columns
    if 'purchase_price' in display_df.columns:
        display_df['purchase_price'] = display_df['purchase_price'].apply(format_currency)
    
    if 'current_price' in display_df.columns:
        display_df['current_price'] = display_df['current_price'].apply(format_currency)
    
    if 'current_value' in display_df.columns:
        display_df['current_value'] = display_df['current_value'].apply(format_currency)
    
    if 'cost_basis' in display_df.columns:
        display_df['cost_basis'] = display_df['cost_basis'].apply(format_currency)
    
    if 'unrealized_gain_loss' in display_df.columns:
        display_df['unrealized_gain_loss'] = display_df['unrealized_gain_loss'].apply(format_currency)
    
    if 'unrealized_gain_loss_pct' in display_df.columns:
        display_df['unrealized_gain_loss_pct'] = display_df['unrealized_gain_loss_pct'].apply(format_percentage)
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def display_key_stats(stats: dict, columns: int = 3) -> None:
    """
    Display key statistics in a grid.
    
    Args:
        stats: Dictionary of stat_name: value pairs
        columns: Number of columns in grid
    """
    cols = st.columns(columns)
    
    for i, (key, value) in enumerate(stats.items()):
        col_idx = i % columns
        
        # Format value based on type
        if isinstance(value, float):
            if 'percent' in key.lower() or 'return' in key.lower():
                formatted_value = format_percentage(value)
            elif 'price' in key.lower() or 'value' in key.lower():
                formatted_value = format_currency(value)
            else:
                formatted_value = f"{value:.2f}"
        else:
            formatted_value = str(value)
        
        cols[col_idx].metric(
            label=key.replace('_', ' ').title(),
            value=formatted_value
        )


