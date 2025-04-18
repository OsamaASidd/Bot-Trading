"""
Supertrend Strategy Module

Implements the Supertrend indicator and trading strategy.
"""

import pandas as pd
import numpy as np
from strategies.base_strategy import TradingStrategy

class SupertrendStrategy(TradingStrategy):
    """Supertrend strategy implementation"""
    
    def __init__(self, period=10, multiplier=3):
        """
        Initialize the Supertrend strategy
        
        Args:
            period (int): Number of periods for ATR calculation
            multiplier (float): ATR multiplier for band calculation
        """
        super().__init__("Supertrend")
        self.period = period
        self.multiplier = multiplier
        
    def tr(self, data):
        """
        Calculate True Range
        
        Args:
            data (pandas.DataFrame): Market data
            
        Returns:
            pandas.Series: True Range values
        """
        data = data.copy()
        data['previous_close'] = data['close'].shift(1)
        data['high-low'] = abs(data['high'] - data['low'])
        data['high-pc'] = abs(data['high'] - data['previous_close'])
        data['low-pc'] = abs(data['low'] - data['previous_close'])
        tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)
        return tr
    
    def atr(self, data, period):
        """
        Calculate Average True Range
        
        Args:
            data (pandas.DataFrame): Market data
            period (int): Number of periods for ATR calculation
            
        Returns:
            pandas.Series: ATR values
        """
        data = data.copy()
        data['tr'] = self.tr(data)
        atr = data['tr'].rolling(period).mean()
        return atr
    
    def calculate(self, data):
        """
        Calculate Supertrend indicator
        
        Args:
            data (pandas.DataFrame): Market data
            
        Returns:
            pandas.DataFrame: Data with Supertrend indicators
        """
        data = data.copy()
        hl2 = (data['high'] + data['low']) / 2
        data['atr'] = self.atr(data, self.period)
        data['upperband'] = hl2 + (self.multiplier * data['atr'])
        data['lowerband'] = hl2 - (self.multiplier * data['atr'])
        data['in_uptrend'] = True

        for current in range(1, len(data.index)):
            previous = current - 1
            if data['close'].iloc[current] > data['upperband'].iloc[previous]:
                data.loc[data.index[current], 'in_uptrend'] = True
            elif data['close'].iloc[current] < data['lowerband'].iloc[previous]:
                data.loc[data.index[current], 'in_uptrend'] = False
            else:
                data.loc[data.index[current], 'in_uptrend'] = data['in_uptrend'].iloc[previous]

                if data['in_uptrend'].iloc[current] and data['lowerband'].iloc[current] < data['lowerband'].iloc[previous]:
                    data.loc[data.index[current], 'lowerband'] = data['lowerband'].iloc[previous]

                if not data['in_uptrend'].iloc[current] and data['upperband'].iloc[current] > data['upperband'].iloc[previous]:
                    data.loc[data.index[current], 'upperband'] = data['upperband'].iloc[previous]
        
        return data
    
    def plot(self, data, ax):
        """
        Plot Supertrend indicator
        
        Args:
            data (pandas.DataFrame): Market data with indicators
            ax (matplotlib.axes.Axes): Matplotlib axis to plot on
        """
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.set_index('timestamp', inplace=True, drop=False)
        
        # Plot price
        ax.plot(data.index, data['close'], label='Price', color='black')
        
        # Plot upper and lower bands
        ax.plot(data.index, data['upperband'], label='Upper Band', color='green', linestyle='--')
        ax.plot(data.index, data['lowerband'], label='Lower Band', color='red', linestyle='--')
        
        # Color points based on trend
        uptrend = data[data['in_uptrend'] == True]
        downtrend = data[data['in_uptrend'] == False]
        
        ax.scatter(uptrend.index, uptrend['close'], color='green', label='Uptrend')
        ax.scatter(downtrend.index, downtrend['close'], color='red', label='Downtrend')
        
        ax.set_title(f"Supertrend (Period={self.period}, Mult={self.multiplier})")
        ax.legend(loc='upper left')
        ax.grid(True)
    
    def get_signal(self, data):
        """
        Return trading signal based on Supertrend
        
        Args:
            data (pandas.DataFrame): Market data with indicators
            
        Returns:
            str: 'buy', 'sell', or 'hold'
        """
        last_row_index = len(data.index) - 1
        previous_row_index = last_row_index - 1
        
        if previous_row_index < 0:
            return 'hold'
            
        if not data['in_uptrend'].iloc[previous_row_index] and data['in_uptrend'].iloc[last_row_index]:
            return 'buy'
        elif data['in_uptrend'].iloc[previous_row_index] and not data['in_uptrend'].iloc[last_row_index]:
            return 'sell'
        else:
            return 'hold'