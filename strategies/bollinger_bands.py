"""
Bollinger Bands Strategy Module

Implements the Bollinger Bands indicator and trading strategy.
"""

import pandas as pd
import numpy as np
from strategies.base_strategy import TradingStrategy

class BollingerBandsStrategy(TradingStrategy):
    """Bollinger Bands strategy implementation"""
    
    def __init__(self, period=20, num_std=2):
        """
        Initialize the Bollinger Bands strategy
        
        Args:
            period (int): Number of periods for moving average
            num_std (float): Number of standard deviations for band width
        """
        super().__init__("Bollinger Bands")
        self.period = period
        self.num_std = num_std
    
    def calculate(self, data):
        """
        Calculate Bollinger Bands
        
        Args:
            data (pandas.DataFrame): Market data
            
        Returns:
            pandas.DataFrame: Data with Bollinger Bands indicators
        """
        data = data.copy()
        
        # Calculate middle band (simple moving average)
        data['bb_middle'] = data['close'].rolling(window=self.period).mean()
        
        # Calculate standard deviation
        data['bb_std'] = data['close'].rolling(window=self.period).std()
        
        # Calculate upper and lower bands
        data['bb_upper'] = data['bb_middle'] + (data['bb_std'] * self.num_std)
        data['bb_lower'] = data['bb_middle'] - (data['bb_std'] * self.num_std)
        
        # Calculate if price is outside bands
        data['above_upper'] = data['close'] > data['bb_upper']
        data['below_lower'] = data['close'] < data['bb_lower']
        
        # Calculate signals (oversold/overbought conditions)
        data['bb_buy_signal'] = False
        data['bb_sell_signal'] = False
        
        # Mark buy signals (price crosses from below to inside the bands)
        for i in range(1, len(data)):
            if data['below_lower'].iloc[i-1] and not data['below_lower'].iloc[i]:
                data.loc[data.index[i], 'bb_buy_signal'] = True
            
            # Mark sell signals (price crosses from above to inside the bands)
            if data['above_upper'].iloc[i-1] and not data['above_upper'].iloc[i]:
                data.loc[data.index[i], 'bb_sell_signal'] = True
        
        return data
    
    def plot(self, data, ax):
        """
        Plot Bollinger Bands
        
        Args:
            data (pandas.DataFrame): Market data with indicators
            ax (matplotlib.axes.Axes): Matplotlib axis to plot on
        """
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.set_index('timestamp', inplace=True, drop=False)
        
        # Plot price
        ax.plot(data.index, data['close'], label='Price', color='black')
        
        # Plot Bollinger Bands
        ax.plot(data.index, data['bb_upper'], label='Upper Band', color='red', linestyle='--')
        ax.plot(data.index, data['bb_middle'], label='Middle Band', color='blue')
        ax.plot(data.index, data['bb_lower'], label='Lower Band', color='green', linestyle='--')
        
        # Plot signals
        buy_signals = data[data['bb_buy_signal'] == True]
        sell_signals = data[data['bb_sell_signal'] == True]
        
        ax.scatter(buy_signals.index, buy_signals['close'], 
                  color='green', marker='^', s=100, label='Buy Signal')
        ax.scatter(sell_signals.index, sell_signals['close'], 
                  color='red', marker='v', s=100, label='Sell Signal')
        
        ax.set_title(f"Bollinger Bands (Period={self.period}, StdDev={self.num_std})")
        ax.legend(loc='upper left')
        ax.grid(True)
    
    def get_signal(self, data):
        """
        Return trading signal based on Bollinger Bands
        
        Args:
            data (pandas.DataFrame): Market data with indicators
            
        Returns:
            str: 'buy', 'sell', or 'hold'
        """
        if data['bb_buy_signal'].iloc[-1]:
            return 'buy'
        elif data['bb_sell_signal'].iloc[-1]:
            return 'sell'
        else:
            return 'hold'