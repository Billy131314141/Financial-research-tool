"""
Portfolio tracking and performance analysis.
"""
import pandas as pd
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class PortfolioTracker:
    """Tracks and analyzes portfolio performance."""
    
    def __init__(self):
        """Initialize portfolio tracker."""
        self.holdings = {}
    
    def add_holding(
        self,
        ticker: str,
        quantity: float,
        purchase_price: float,
        current_price: float
    ) -> Dict:
        """
        Add or update a holding in the portfolio.
        
        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares
            purchase_price: Average purchase price per share
            current_price: Current market price
            
        Returns:
            Dictionary with holding details
        """
        self.holdings[ticker] = {
            'ticker': ticker,
            'quantity': quantity,
            'purchase_price': purchase_price,
            'current_price': current_price,
            'cost_basis': quantity * purchase_price,
            'current_value': quantity * current_price,
            'unrealized_gain_loss': (current_price - purchase_price) * quantity,
            'unrealized_gain_loss_pct': ((current_price - purchase_price) / purchase_price) * 100
        }
        
        return self.holdings[ticker]
    
    def remove_holding(self, ticker: str) -> bool:
        """
        Remove a holding from the portfolio.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            True if removed, False if not found
        """
        if ticker in self.holdings:
            del self.holdings[ticker]
            return True
        return False
    
    def get_portfolio_summary(self) -> Dict:
        """
        Calculate overall portfolio statistics.
        
        Returns:
            Dictionary with portfolio summary
        """
        if not self.holdings:
            return {
                'total_value': 0,
                'total_cost': 0,
                'total_gain_loss': 0,
                'total_gain_loss_pct': 0,
                'num_holdings': 0
            }
        
        total_value = sum(h['current_value'] for h in self.holdings.values())
        total_cost = sum(h['cost_basis'] for h in self.holdings.values())
        total_gain_loss = total_value - total_cost
        total_gain_loss_pct = (total_gain_loss / total_cost) * 100 if total_cost > 0 else 0
        
        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_gain_loss': total_gain_loss,
            'total_gain_loss_pct': total_gain_loss_pct,
            'num_holdings': len(self.holdings)
        }
    
    def get_holdings_dataframe(self) -> pd.DataFrame:
        """
        Get portfolio holdings as a DataFrame.
        
        Returns:
            DataFrame with all holdings
        """
        if not self.holdings:
            return pd.DataFrame()
        
        return pd.DataFrame(list(self.holdings.values()))
    
    def get_allocation(self) -> pd.DataFrame:
        """
        Calculate portfolio allocation by value.
        
        Returns:
            DataFrame with allocation percentages
        """
        if not self.holdings:
            return pd.DataFrame()
        
        df = self.get_holdings_dataframe()
        total_value = df['current_value'].sum()
        
        df['allocation_pct'] = (df['current_value'] / total_value) * 100
        
        return df[['ticker', 'current_value', 'allocation_pct']].sort_values(
            'allocation_pct', ascending=False
        )


def calculate_portfolio_metrics(
    holdings_df: pd.DataFrame,
    benchmark_returns: pd.Series = None
) -> Dict:
    """
    Calculate advanced portfolio metrics.
    
    Args:
        holdings_df: DataFrame with portfolio holdings
        benchmark_returns: Optional benchmark returns for comparison
        
    Returns:
        Dictionary with portfolio metrics
    """
    if holdings_df.empty:
        return {}
    
    # Calculate weighted average return
    total_value = holdings_df['current_value'].sum()
    holdings_df['weight'] = holdings_df['current_value'] / total_value
    weighted_return = (holdings_df['unrealized_gain_loss_pct'] * holdings_df['weight']).sum()
    
    metrics = {
        'weighted_return': weighted_return,
        'best_performer': holdings_df.loc[holdings_df['unrealized_gain_loss_pct'].idxmax(), 'ticker'],
        'worst_performer': holdings_df.loc[holdings_df['unrealized_gain_loss_pct'].idxmin(), 'ticker'],
        'best_return': holdings_df['unrealized_gain_loss_pct'].max(),
        'worst_return': holdings_df['unrealized_gain_loss_pct'].min()
    }
    
    return metrics


