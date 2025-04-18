"""
Strategies package initialization.

This package contains all trading strategy implementations.
"""

from strategies.base_strategy import TradingStrategy
from strategies.supertrend import SupertrendStrategy
from strategies.golden_cross import GoldenCrossStrategy
from strategies.bollinger_bands import BollingerBandsStrategy
from strategies.funding_rate import FundingRateStrategy

__all__ = [
    'TradingStrategy',
    'SupertrendStrategy',
    'GoldenCrossStrategy',
    'BollingerBandsStrategy',
    'FundingRateStrategy'
]