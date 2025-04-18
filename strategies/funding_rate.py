"""
Funding Rate Strategy Module

Implements a trading strategy based on exchange funding rates.
"""

import pandas as pd
import numpy as np
import requests
import time
import json
import logging
from strategies.base_strategy import TradingStrategy

class FundingRateStrategy(TradingStrategy):
    """Funding Rate strategy implementation"""
    
    def __init__(self, threshold=0.001):
        """
        Initialize the Funding Rate strategy
        
        Args:
            threshold (float): Threshold for generating signals (as decimal)
        """
        super().__init__("Funding Rate")
        self.threshold = threshold
        self.logger = logging.getLogger(__name__)
    
    def fetch_funding_rates(self, exchange, symbol):
        """
        Fetch funding rates from the exchange
        
        Args:
            exchange: Exchange connection object
            symbol (str): Trading pair symbol
            
        Returns:
            list: List of funding rates
        """
        try:
            # In a real implementation, you would fetch actual funding rates
            # For demo purposes, we'll simulate funding rate data
            funding_rates = []
            
            # Try to get funding rates from exchange if available
            if hasattr(exchange, 'fetchFundingRates'):
                funding_data = exchange.fetchFundingRates([symbol])
                if symbol in funding_data:
                    return funding_data[symbol]['fundingRate']
            
            return None
        except Exception as e:
            self.logger.error(f"Error fetching funding rates: {str(e)}")
            return None
    
    def calculate(self, data):
        """
        Calculate signals based on funding rate
        
        Args:
            data (pandas.DataFrame): Market data
            
        Returns:
            pandas.DataFrame: Data with funding rate signals
        """
        data = data.copy()
        
        # For demonstration, we'll simulate funding rate data
        # In a real implementation, you would fetch this from an exchange API
        data['funding_rate'] = np.random.normal(0, 0.0005, len(data))
        
        # Calculate signals
        data['fr_buy_signal'] = data['funding_rate'] < -self.threshold
        data['fr_sell_signal'] = data['funding_rate'] > self.threshold
        
        return data
    
    def plot(self, data, ax):
        """
        Plot funding rate
        
        Args:
            data (pandas.DataFrame): Market data with indicators
            ax (matplotlib.axes.Axes): Matplotlib axis to plot on
        """
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.set_index('timestamp', inplace=True, drop=False)
        
        # Create a separate axis for funding rate
        ax2 = ax.twinx()
        
        # Plot price on primary axis
        ax.plot(data.index, data['close'], label='Price', color='black')
        
        # Plot funding rate on secondary axis
        ax2.plot(data.index, data['funding_rate'], label='Funding Rate', color='purple')
        ax2.axhline(y=self.threshold, color='red', linestyle='--', alpha=0.5)
        ax2.axhline(y=-self.threshold, color='green', linestyle='--', alpha=0.5)
        ax2.fill_between(data.index, data['funding_rate'], 0, 
                         where=(data['funding_rate'] > 0), color='red', alpha=0.3)
        ax2.fill_between(data.index, data['funding_rate'], 0, 
                         where=(data['funding_rate'] < 0), color='green', alpha=0.3)
        
        # Set labels
        ax.set_title("Funding Rate Analysis")
        ax2.set_ylabel('Funding Rate')
        
        # Add legend for funding rate
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2, loc='upper left')
    
    def get_signal(self, data):
        """
        Return trading signal based on funding rate
        
        Args:
            data (pandas.DataFrame): Market data with indicators
            
        Returns:
            str: 'buy', 'sell', or 'hold'
        """
        if data['fr_buy_signal'].iloc[-1]:
            return 'buy'
        elif data['fr_sell_signal'].iloc[-1]:
            return 'sell'
        else:
            return 'hold'