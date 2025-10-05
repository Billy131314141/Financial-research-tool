"""
Chart generation utilities for financial data visualization.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, List
import sys
sys.path.append('..')
from config.settings import COLORS, DEFAULT_CHART_HEIGHT


def create_line_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = "",
    y_label: str = "Price",
    color: str = COLORS['info']
) -> go.Figure:
    """
    Create a line chart for stock prices.
    
    Args:
        df: DataFrame with data
        x_column: Column name for x-axis (typically date)
        y_column: Column name for y-axis (typically price)
        title: Chart title
        y_label: Y-axis label
        color: Line color
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_column],
        y=df[y_column],
        mode='lines',
        name=y_label,
        line=dict(color=color, width=2),
        hovertemplate='%{y:$.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=y_label,
        template="plotly_white",
        height=DEFAULT_CHART_HEIGHT,
        hovermode='x unified',
        showlegend=True
    )
    
    return fig


def create_candlestick_chart(
    df: pd.DataFrame,
    title: str = "Stock Price"
) -> go.Figure:
    """
    Create a candlestick chart for stock prices.
    
    Args:
        df: DataFrame with OHLC data
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure(data=[go.Candlestick(
        x=df['date'] if 'date' in df.columns else df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color=COLORS['positive'],
        decreasing_line_color=COLORS['negative']
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=DEFAULT_CHART_HEIGHT,
        xaxis_rangeslider_visible=False
    )
    
    return fig


def create_volume_chart(
    df: pd.DataFrame,
    title: str = "Trading Volume"
) -> go.Figure:
    """
    Create a volume bar chart.
    
    Args:
        df: DataFrame with volume data
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    # Color bars based on price change
    colors = []
    for i in range(len(df)):
        if i == 0:
            colors.append(COLORS['info'])
        else:
            if df.iloc[i]['close'] >= df.iloc[i-1]['close']:
                colors.append(COLORS['positive'])
            else:
                colors.append(COLORS['negative'])
    
    fig = go.Figure(data=[go.Bar(
        x=df['date'] if 'date' in df.columns else df.index,
        y=df['volume'],
        marker_color=colors,
        name='Volume'
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Volume",
        template="plotly_white",
        height=300,
        showlegend=False
    )
    
    return fig


def create_multi_line_chart(
    df: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    title: str = "",
    y_label: str = "Value"
) -> go.Figure:
    """
    Create a multi-line chart for comparing multiple series.
    
    Args:
        df: DataFrame with data
        x_column: Column name for x-axis
        y_columns: List of column names for y-axis
        title: Chart title
        y_label: Y-axis label
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    for col in y_columns:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df[x_column],
                y=df[col],
                mode='lines',
                name=col,
                hovertemplate='%{y:.2f}<extra></extra>'
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=y_label,
        template="plotly_white",
        height=DEFAULT_CHART_HEIGHT,
        hovermode='x unified',
        showlegend=True
    )
    
    return fig


def create_pie_chart(
    df: pd.DataFrame,
    values_column: str,
    names_column: str,
    title: str = ""
) -> go.Figure:
    """
    Create a pie chart for portfolio allocation.
    
    Args:
        df: DataFrame with data
        values_column: Column name for values
        names_column: Column name for labels
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure(data=[go.Pie(
        labels=df[names_column],
        values=df[values_column],
        hole=0.3,
        hovertemplate='%{label}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=title,
        template="plotly_white",
        height=400,
        showlegend=True
    )
    
    return fig


def create_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = "",
    color_column: Optional[str] = None,
    horizontal: bool = False
) -> go.Figure:
    """
    Create a bar chart.
    
    Args:
        df: DataFrame with data
        x_column: Column name for x-axis
        y_column: Column name for y-axis
        title: Chart title
        color_column: Optional column for color coding
        horizontal: Whether to create horizontal bars
        
    Returns:
        Plotly figure object
    """
    # Determine bar colors
    if color_column and color_column in df.columns:
        colors = [COLORS['positive'] if x >= 0 else COLORS['negative'] 
                  for x in df[color_column]]
    else:
        colors = COLORS['info']
    
    if horizontal:
        fig = go.Figure(data=[go.Bar(
            y=df[x_column],
            x=df[y_column],
            orientation='h',
            marker_color=colors
        )])
        fig.update_layout(
            xaxis_title=y_column,
            yaxis_title=x_column
        )
    else:
        fig = go.Figure(data=[go.Bar(
            x=df[x_column],
            y=df[y_column],
            marker_color=colors
        )])
        fig.update_layout(
            xaxis_title=x_column,
            yaxis_title=y_column
        )
    
    fig.update_layout(
        title=title,
        template="plotly_white",
        height=DEFAULT_CHART_HEIGHT,
        showlegend=False
    )
    
    return fig


def create_comparison_chart(
    df: pd.DataFrame,
    title: str = "Performance Comparison"
) -> go.Figure:
    """
    Create a normalized comparison chart for multiple stocks.
    
    Args:
        df: DataFrame with multiple stock prices (columns are tickers)
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    # Normalize all series to start at 100
    df_normalized = df.copy()
    for col in df_normalized.columns:
        if col != 'date':
            df_normalized[col] = (df_normalized[col] / df_normalized[col].iloc[0]) * 100
    
    fig = go.Figure()
    
    for col in df_normalized.columns:
        if col != 'date':
            fig.add_trace(go.Scatter(
                x=df_normalized['date'] if 'date' in df_normalized.columns else df_normalized.index,
                y=df_normalized[col],
                mode='lines',
                name=col,
                hovertemplate='%{y:.2f}%<extra></extra>'
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Normalized Performance (Base = 100)",
        template="plotly_white",
        height=DEFAULT_CHART_HEIGHT,
        hovermode='x unified',
        showlegend=True
    )
    
    return fig


