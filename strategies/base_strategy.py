"""
Base Strategy Module

This module defines the base class for all trading strategies.
"""

class TradingStrategy:
    """Base class for all trading strategies"""
    
    def __init__(self, name):
        """
        Initialize a strategy
        
        Args:
            name (str): The name of the strategy
        """
        self.name = name
        self.is_active = False
        
    def calculate(self, data):
        """
        Calculate the strategy indicators and signals
        
        Args:
            data (pandas.DataFrame): The market data
            
        Returns:
            pandas.DataFrame: The data with added indicator columns
        """
        return data
    
    def plot(self, data, ax):
        """
        Plot the strategy on the given matplotlib axis
        
        Args:
            data (pandas.DataFrame): The market data with indicators
            ax (matplotlib.axes.Axes): The matplotlib axis to plot on
        """
        pass
    
    def get_signal(self, data):
        """
        Return the trading signal based on the strategy
        
        Args:
            data (pandas.DataFrame): The market data with indicators
            
        Returns:
            str: 'buy', 'sell', or 'hold'
        """
        return 'hold'
    
    def set_parameters(self, params):
        """
        Update the strategy parameters
        
        Args:
            params (dict): Dictionary of parameter names and values
        """
        for param_name, param_value in params.items():
            if hasattr(self, param_name):
                setattr(self, param_name, param_value)