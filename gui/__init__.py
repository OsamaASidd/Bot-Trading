"""
GUI package initialization.

This package contains all GUI components for the trading bot.
"""

from gui.main_window import TradingBotGUI
from gui.strategy_tabs import (
    create_supertrend_tab, 
    create_golden_cross_tab,
    create_bollinger_bands_tab,
    create_funding_rate_tab
)
from gui.utils import ToolTip

__all__ = [
    'TradingBotGUI',
    'create_supertrend_tab',
    'create_golden_cross_tab',
    'create_bollinger_bands_tab',
    'create_funding_rate_tab',
    'ToolTip'
]