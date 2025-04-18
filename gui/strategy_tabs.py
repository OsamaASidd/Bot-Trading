"""
Strategy Tabs Module

This module implements the UI tabs for each trading strategy.
"""

import tkinter as tk
from tkinter import ttk
from gui.utils import ToolTip

def create_supertrend_tab(notebook):
    """
    Create Supertrend strategy configuration tab
    
    Args:
        notebook (ttk.Notebook): The parent notebook widget
        
    Returns:
        tuple: (tab frame, variables dictionary)
    """
    supertrend_frame = ttk.Frame(notebook)
    notebook.add(supertrend_frame, text="Supertrend")
    
    # Create a frame for parameters
    params_frame = tk.LabelFrame(supertrend_frame, text="Parameters")
    params_frame.pack(fill=tk.X, padx=10, pady=5)
    
    # Variables to track
    variables = {}
    
    # Activate checkbox
    variables['active'] = tk.BooleanVar(value=True)
    supertrend_check = tk.Checkbutton(
        params_frame, 
        text="Activate Supertrend Strategy", 
        variable=variables['active']
    )
    supertrend_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
    
    # Period parameter
    tk.Label(params_frame, text="Period:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    variables['period'] = tk.StringVar(value="10")
    supertrend_period_entry = tk.Entry(params_frame, textvariable=variables['period'])
    supertrend_period_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    period_tooltip = ToolTip(
        supertrend_period_entry, 
        "Number of periods used to calculate ATR (Average True Range).\n"
        "Higher values create a smoother, less responsive indicator."
    )
    
    # Multiplier parameter
    tk.Label(params_frame, text="Multiplier:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    variables['multiplier'] = tk.StringVar(value="3")
    supertrend_mult_entry = tk.Entry(params_frame, textvariable=variables['multiplier'])
    supertrend_mult_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
    mult_tooltip = ToolTip(
        supertrend_mult_entry, 
        "Multiplier for ATR to set the band width.\n"
        "Higher values create wider bands with fewer signals."
    )
    
    # Explanation text
    explanation_text = """
Supertrend Strategy Explanation:

The Supertrend indicator is a trend-following indicator that uses ATR (Average True Range) to 
calculate upper and lower bands around the price.

How it works:
- When price crosses above the lower band, it signals an uptrend (BUY)
- When price crosses below the upper band, it signals a downtrend (SELL)
- The bands adjust dynamically to follow the price trend

Parameters:
- Period: Number of bars used to calculate ATR (typical values: 7-14)
- Multiplier: Multiplies the ATR value to set band width (typical values: 2-3)

Higher period and multiplier values make the indicator less sensitive, reducing false signals
but potentially entering trends later.
"""
    explanation = tk.Label(
        supertrend_frame, 
        text=explanation_text, 
        justify=tk.LEFT, 
        wraplength=500, 
        bg="#f0f0f0"
    )
    explanation.pack(fill=tk.X, padx=10, pady=10)
    
    return supertrend_frame, variables

def create_golden_cross_tab(notebook):
    """
    Create Golden Cross strategy configuration tab
    
    Args:
        notebook (ttk.Notebook): The parent notebook widget
        
    Returns:
        tuple: (tab frame, variables dictionary)
    """
    gc_frame = ttk.Frame(notebook)
    notebook.add(gc_frame, text="Golden/Death Cross")
    
    # Create a frame for parameters
    params_frame = tk.LabelFrame(gc_frame, text="Parameters")
    params_frame.pack(fill=tk.X, padx=10, pady=5)
    
    # Variables to track
    variables = {}
    
    # Activate checkbox
    variables['active'] = tk.BooleanVar(value=True)
    gc_check = tk.Checkbutton(
        params_frame, 
        text="Activate Golden/Death Cross Strategy", 
        variable=variables['active']
    )
    gc_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
    
    # Short period parameter
    tk.Label(params_frame, text="Short MA Period:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    variables['short_period'] = tk.StringVar(value="50")
    gc_short_period_entry = tk.Entry(params_frame, textvariable=variables['short_period'])
    gc_short_period_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    short_tooltip = ToolTip(
        gc_short_period_entry, 
        "Number of periods for short-term moving average.\n"
        "Typical values are 9, 20, or 50 periods."
    )
    
    # Long period parameter
    tk.Label(params_frame, text="Long MA Period:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    variables['long_period'] = tk.StringVar(value="200")
    gc_long_period_entry = tk.Entry(params_frame, textvariable=variables['long_period'])
    gc_long_period_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
    long_tooltip = ToolTip(
        gc_long_period_entry, 
        "Number of periods for long-term moving average.\n"
        "Typical values are 50, 100, or 200 periods."
    )
    
    # Explanation text
    explanation_text = """
Golden Cross / Death Cross Strategy Explanation:

This strategy uses the crossover of two moving averages to generate buy and sell signals.

How it works:
- Golden Cross (BUY): When the short-term MA crosses above the long-term MA, indicating
  bullish momentum and potential uptrend.
- Death Cross (SELL): When the short-term MA crosses below the long-term MA, indicating
  bearish momentum and potential downtrend.

Parameters:
- Short MA Period: Number of bars for the faster moving average (typically 50)
- Long MA Period: Number of bars for the slower moving average (typically 200)

The classic configuration is the 50/200 day moving average crossover, which is widely
followed by institutional investors. Shorter periods (like 9/50) generate more signals
but can include more false positives.
"""
    explanation = tk.Label(
        gc_frame, 
        text=explanation_text, 
        justify=tk.LEFT, 
        wraplength=500, 
        bg="#f0f0f0"
    )
    explanation.pack(fill=tk.X, padx=10, pady=10)
    
    return gc_frame, variables

def create_bollinger_bands_tab(notebook):
    """
    Create Bollinger Bands strategy configuration tab
    
    Args:
        notebook (ttk.Notebook): The parent notebook widget
        
    Returns:
        tuple: (tab frame, variables dictionary)
    """
    bb_frame = ttk.Frame(notebook)
    notebook.add(bb_frame, text="Bollinger Bands")
    
    # Create a frame for parameters
    params_frame = tk.LabelFrame(bb_frame, text="Parameters")
    params_frame.pack(fill=tk.X, padx=10, pady=5)
    
    # Variables to track
    variables = {}
    
    # Activate checkbox
    variables['active'] = tk.BooleanVar(value=True)
    bb_check = tk.Checkbutton(
        params_frame, 
        text="Activate Bollinger Bands Strategy", 
        variable=variables['active']
    )
    bb_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
    
    # Period parameter
    tk.Label(params_frame, text="Period:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    variables['period'] = tk.StringVar(value="20")
    bb_period_entry = tk.Entry(params_frame, textvariable=variables['period'])
    bb_period_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    period_tooltip = ToolTip(
        bb_period_entry, 
        "Number of periods for moving average and standard deviation calculation.\n"
        "Standard value is 20, but can range from 10-50."
    )
    
    # Standard deviation multiplier
    tk.Label(params_frame, text="Standard Deviation Multiplier:").grid(
        row=2, column=0, sticky=tk.W, padx=5, pady=5
    )
    variables['std_dev'] = tk.StringVar(value="2")
    bb_std_entry = tk.Entry(params_frame, textvariable=variables['std_dev'])
    bb_std_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
    std_tooltip = ToolTip(
        bb_std_entry, 
        "Number of standard deviations for upper and lower bands.\n"
        "Standard value is 2, higher values create wider bands."
    )
    
    # Explanation text
    explanation_text = """
Bollinger Bands Strategy Explanation:

Bollinger Bands consist of a middle band (simple moving average) and two outer bands
that are calculated by adding and subtracting a multiple of the standard deviation.

How it works:
- BUY Signal: When price crosses from below the lower band back into the channel
- SELL Signal: When price crosses from above the upper band back into the channel
- The bands adapt to volatility - wider during high volatility, narrower in low volatility

Parameters:
- Period: Number of bars for the moving average (typically 20)
- Standard Deviation Multiplier: Number of standard deviations for band width (typically 2)

Bollinger Bands are effective in ranging markets and for identifying potential reversals.
The strategy can be combined with volume indicators for more reliability.
"""
    explanation = tk.Label(
        bb_frame, 
        text=explanation_text, 
        justify=tk.LEFT, 
        wraplength=500, 
        bg="#f0f0f0"
    )
    explanation.pack(fill=tk.X, padx=10, pady=10)
    
    return bb_frame, variables

def create_funding_rate_tab(notebook):
    """
    Create Funding Rate strategy configuration tab
    
    Args:
        notebook (ttk.Notebook): The parent notebook widget
        
    Returns:
        tuple: (tab frame, variables dictionary)
    """
    fr_frame = ttk.Frame(notebook)
    notebook.add(fr_frame, text="Funding Rate")
    
    # Create a frame for parameters
    params_frame = tk.LabelFrame(fr_frame, text="Parameters")
    params_frame.pack(fill=tk.X, padx=10, pady=5)
    
    # Variables to track
    variables = {}
    
    # Activate checkbox
    variables['active'] = tk.BooleanVar(value=True)
    fr_check = tk.Checkbutton(
        params_frame, 
        text="Activate Funding Rate Strategy", 
        variable=variables['active']
    )
    fr_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
    
    # Threshold parameter
    tk.Label(params_frame, text="Threshold (%):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    variables['threshold'] = tk.StringVar(value="0.1")
    fr_threshold_entry = tk.Entry(params_frame, textvariable=variables['threshold'])
    fr_threshold_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    threshold_tooltip = ToolTip(
        fr_threshold_entry, 
        "Threshold value for funding rate signals (in %).\n"
        "Higher values filter out weak signals."
    )
    
    # Explanation text
    explanation_text = """
Funding Rate Strategy Explanation:

The funding rate is a mechanism used in perpetual contracts on cryptocurrency exchanges
to ensure the futures price stays close to the index price.

How it works:
- BUY Signal: When funding rate drops below the negative threshold, indicating shorts
  are paying longs and potential for a price reversal upward.
- SELL Signal: When funding rate rises above the positive threshold, indicating longs
  are paying shorts and potential for a price reversal downward.

Parameters:
- Threshold: The absolute value at which funding rates trigger a signal (typically 0.01% to 0.1%)

This strategy works well for mean reversion trading when extreme funding rates indicate
potential market imbalances and imminent reversals.
"""
    explanation = tk.Label(
        fr_frame, 
        text=explanation_text, 
        justify=tk.LEFT, 
        wraplength=500, 
        bg="#f0f0f0"
    )
    explanation.pack(fill=tk.X, padx=10, pady=10)
    
    return fr_frame, variables