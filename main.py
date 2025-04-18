#!/usr/bin/env python
"""
Advanced Multi-Strategy Trading Bot

Main entry point for the trading bot application.
"""

import os
import sys
import tkinter as tk
import logging
from tkinter import ttk
import ccxt

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import project modules
from strategies.supertrend import SupertrendStrategy
from strategies.golden_cross import GoldenCrossStrategy
from strategies.bollinger_bands import BollingerBandsStrategy
from strategies.funding_rate import FundingRateStrategy
from core.trading_bot import TradingBot
from gui.main_window import TradingBotGUI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('trading_bot.log')
    ]
)

logger = logging.getLogger(__name__)

def setup_exchange():
    """
    Set up the exchange connection
    
    Returns:
        ccxt.Exchange: The exchange instance
    """
    # Initialize exchange with API keys
    # Note: In a production environment, these should be loaded from
    # environment variables or a secure configuration file
    exchange = ccxt.binance({
        "apiKey": 'my5nw1BwA5Hqv8xxZ5rHd8p1xIsZhlojXDv1PRsn85eVjFvjqafvdNpFKQNFOqym',
        "secret": 'jhOz9nwsXSzWFU54RA4rg700dMJL7sQvYmc0SPhTynJneyJ8B4C7SAKGfbGwoco9'
    })
    
    # Use testnet for testing
    exchange.set_sandbox_mode(True)
    
    logger.info("Exchange connection initialized")
    return exchange

def setup_strategies():
    """
    Set up the trading strategies
    
    Returns:
        list: List of strategy instances
    """
    # Initialize strategies with default parameters
    supertrend = SupertrendStrategy(period=10, multiplier=3)
    golden_cross = GoldenCrossStrategy(short_period=50, long_period=200)
    bollinger_bands = BollingerBandsStrategy(period=20, num_std=2)
    funding_rate = FundingRateStrategy(threshold=0.001)
    
    # Set all strategies active by default
    supertrend.is_active = True
    golden_cross.is_active = True
    bollinger_bands.is_active = True
    funding_rate.is_active = True
    
    logger.info("Trading strategies initialized")
    return [supertrend, golden_cross, bollinger_bands, funding_rate]

def main():
    """Main entry point for the application"""
    try:
        # Setup exchange connection
        exchange = setup_exchange()
        
        # Setup strategies
        strategies = setup_strategies()
        
        # Initialize trading bot
        bot = TradingBot(exchange, strategies)
        
        # Create the main window
        root = tk.Tk()
        root.title("Advanced Multi-Strategy Trading Bot")
        
        # Set style
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        
        # Create the GUI
        app = TradingBotGUI(root, bot, exchange)
        
        # Run the application
        logger.info("Starting application")
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Error in main application: {str(e)}")
        
if __name__ == "__main__":
    main()