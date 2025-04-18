"""
Golden Cross Strategy Module

Implements the Golden Cross/Death Cross indicator and trading strategy.
"""

import pandas as pd
import numpy as np
from strategies.base_strategy import TradingStrategy

class GoldenCrossStrategy(TradingStrategy):
    """Moving Average Crossover strategy (Golden Cross/Death Cross)"""
    
    def __init__(self, short_period=50, long_period=200):
        """
        Initialize the Golden Cross strategy
        
        Args:
            short_period (int): Period for short-term moving average
            long_period (int): Period for long-term moving average
        """
        super().__init__("Golden Cross")
        self.short_period = short_period
        self.long_period = long_period
    
    def calculate(self, data):
        """
        Calculate moving averages and crossover signals
        
        Args:
            data (pandas.DataFrame): Market data
            
        Returns:
            pandas.DataFrame: Data with moving averages and crossover signals
        """
        data = data.copy()
        
        # Calculate short and long-term moving averages
        data[f'MA_{self.short_period}'] = data['close'].rolling(window=self.short_period).mean()
        data[f'MA_{self.long_period}'] = data['close'].rolling(window=self.long_period).mean()
        
        # Calculate crossover signal
        data['golden_cross'] = False
        data['death_cross'] = False
        
        # Need at least 2 rows of data to calculate crossovers
        if len(data) >= 2:
            for i in range(1, len(data)):
                # Golden Cross: short MA crosses above long MA
                if (data[f'MA_{self.short_period}'].iloc[i-1] <= data[f'MA_{self.long_period}'].iloc[i-1] and 
                    data[f'MA_{self.short_period}'].iloc[i] > data[f'MA_{self.long_period}'].iloc[i]):
                    data.loc[data.index[i], 'golden_cross'] = True
                
                # Death Cross: short MA crosses below long MA
                if (data[f'MA_{self.short_period}'].iloc[i-1] >= data[f'MA_{self.long_period}'].iloc[i-1] and 
                    data[f'MA_{self.short_period}'].iloc[i] < data[f'MA_{self.long_period}'].iloc[i]):
                    data.loc[data.index[i], 'death_cross'] = True
                    
        return data
    
    def plot(self, data, ax):
        """
        Plot moving averages and crossovers
        
        Args:
            data (pandas.DataFrame): Market data with indicators
            ax (matplotlib.axes.Axes): Matplotlib axis to plot on
        """
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.set_index('timestamp', inplace=True, drop=False)
        
        # Plot price
        ax.plot(data.index, data['close'], label='Price', color='black', alpha=0.5)
        
        # Plot moving averages
        ax.plot(data.index, data[f'MA_{self.short_period}'], 
                label=f'{self.short_period}-period MA', color='blue')
        ax.plot(data.index, data[f'MA_{self.long_period}'], 
                label=f'{self.long_period}-period MA', color='orange')
        
        # Plot crossover points
        golden_cross_points = data[data['golden_cross'] == True]
        death_cross_points = data[data['death_cross'] == True]
        
        ax.scatter(golden_cross_points.index, golden_cross_points['close'], 
                   color='green', marker='^', s=100, label='Golden Cross')
        ax.scatter(death_cross_points.index, death_cross_points['close'], 
                   color='red', marker='v', s=100, label='Death Cross')
        
        ax.set_title(f"Moving Average Crossover ({self.short_period}/{self.long_period})")
        ax.legend(loc='upper left')
        ax.grid(True)
    
    def get_signal(self, data):
        """
        Return trading signal based on crossovers
        
        Args:
            data (pandas.DataFrame): Market data with indicators
            
        Returns:
            str: 'buy', 'sell', or 'hold'
        """
        # Check for golden cross (buy signal)
        if data['golden_cross'].iloc[-1]:
            return 'buy'
        # Check for death cross (sell signal)
        elif data['death_cross'].iloc[-1]:
            return 'sell'
        else:
            return 'hold'