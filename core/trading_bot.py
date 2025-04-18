"""
Trading Bot Core Module

This module implements the main trading bot engine that coordinates
data fetching, strategy execution, and order placement.
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime

class TradingBot:
    """Main trading bot class that handles data fetching and strategy execution"""
    
    def __init__(self, exchange, strategies=None):
        """
        Initialize the trading bot
        
        Args:
            exchange: Exchange connection object
            strategies (list, optional): List of strategy objects
        """
        self.exchange = exchange
        self.strategies = strategies or []
        self.data = None
        self.in_position = False
        self.current_signals = {}
        self.logger = logging.getLogger(__name__)
        
    def add_strategy(self, strategy):
        """
        Add a strategy to the bot
        
        Args:
            strategy: Strategy object to add
        """
        self.strategies.append(strategy)
        
    def fetch_data(self, symbol, timeframe, limit=100):
        """
        Fetch market data from exchange
        
        Args:
            symbol (str): Trading pair symbol
            timeframe (str): Timeframe (e.g., '1m', '5m', '1h')
            limit (int, optional): Number of candles to fetch
            
        Returns:
            pandas.DataFrame: Market data
        """
        try:
            self.logger.info(f"Fetching data for {symbol} on {timeframe} timeframe")
            bars = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            
            # Create DataFrame from the fetched data
            df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            self.data = df
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching data: {str(e)}")
            return None
    
    def run_strategies(self):
        """
        Run all active strategies
        
        Returns:
            dict: Results from each strategy
        """
        if self.data is None:
            self.logger.warning("No data available to run strategies")
            return {}
        
        results = {}
        for strategy in self.strategies:
            if strategy.is_active:
                # Make a copy of the data for this strategy
                strategy_data = self.data.copy()
                
                try:
                    # Calculate indicators
                    strategy_data = strategy.calculate(strategy_data)
                    
                    # Get signal
                    signal = strategy.get_signal(strategy_data)
                    
                    results[strategy.name] = {
                        'data': strategy_data,
                        'signal': signal
                    }
                    
                    self.logger.info(f"Strategy {strategy.name} returned signal: {signal}")
                    
                except Exception as e:
                    self.logger.error(f"Error running strategy {strategy.name}: {str(e)}")
        
        self.current_signals = {name: result['signal'] for name, result in results.items()}
        return results
    
    def get_combined_signal(self, mode='majority'):
        """
        Combine signals from all active strategies
        
        Args:
            mode (str): Signal combination mode ('majority', 'consensus', or 'any')
            
        Returns:
            str: Combined signal ('buy', 'sell', or 'hold')
        """
        if not self.current_signals:
            return 'hold'
        
        signals = list(self.current_signals.values())
        
        if mode == 'majority':
            # Use majority vote
            buy_count = signals.count('buy')
            sell_count = signals.count('sell')
            hold_count = signals.count('hold')
            
            if buy_count > sell_count and buy_count > hold_count:
                return 'buy'
            elif sell_count > buy_count and sell_count > hold_count:
                return 'sell'
            else:
                return 'hold'
        
        elif mode == 'consensus':
            # Only act if all strategies agree
            if all(signal == 'buy' for signal in signals):
                return 'buy'
            elif all(signal == 'sell' for signal in signals):
                return 'sell'
            else:
                return 'hold'
        
        elif mode == 'any':
            # Act if any strategy gives a signal
            if 'buy' in signals:
                return 'buy'
            elif 'sell' in signals:
                return 'sell'
            else:
                return 'hold'
        
        else:
            return 'hold'
    
    def execute_order(self, symbol, signal, quantity=0.001):
        """
        Execute order based on signal
        
        Args:
            symbol (str): Trading pair symbol
            signal (str): Trading signal ('buy' or 'sell')
            quantity (float, optional): Order quantity
            
        Returns:
            bool: True if order was placed, False otherwise
        """
        if signal == 'buy' and not self.in_position:
            # Place buy order
            try:
                self.logger.info(f"Executing BUY order for {symbol}, quantity: {quantity}")
                # Uncomment to execute real orders:
                # order = self.exchange.create_market_buy_order(symbol, quantity)
                self.in_position = True
                return True
            except Exception as e:
                self.logger.error(f"Error executing buy order: {str(e)}")
                return False
            
        elif signal == 'sell' and self.in_position:
            # Place sell order
            try:
                self.logger.info(f"Executing SELL order for {symbol}, quantity: {quantity}")
                # Uncomment to execute real orders:
                # order = self.exchange.create_market_sell_order(symbol, quantity)
                self.in_position = False
                return True
            except Exception as e:
                self.logger.error(f"Error executing sell order: {str(e)}")
                return False
            
        return False