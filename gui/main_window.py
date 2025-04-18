"""
Main Window Module

Implements the main application window and coordinates the GUI components.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import logging
import threading
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from gui.utils import ToolTip
from gui.strategy_tabs import (
    create_supertrend_tab, 
    create_golden_cross_tab,
    create_bollinger_bands_tab,
    create_funding_rate_tab
)

class TradingBotGUI:
    """Main GUI class for the trading bot application"""
    
    def __init__(self, root, bot, exchange):
        """
        Initialize the main window
        
        Args:
            root (tk.Tk): Root Tkinter window
            bot: Trading bot instance
            exchange: Exchange connection instance
        """
        self.root = root
        self.root.title("Advanced Trading Bot")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Store references to bot and exchange
        self.bot = bot
        self.exchange = exchange
        
        # Running flag
        self.running = False
        
        # Create the GUI components
        self.create_header()
        self.create_settings_frame()
        self.create_strategy_tabs()
        self.create_charts_frame()
        self.create_console_frame()
        self.create_control_buttons()
    
    def create_header(self):
        """Create header with logo and title"""
        # Header frame
        self.header_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            self.header_frame, 
            text="Advanced Multi-Signal Trading Bot", 
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.TOP, pady=10)
        
        # Version info
        version_label = tk.Label(
            self.header_frame,
            text="v1.0.0",
            font=("Helvetica", 8),
            bg="#f0f0f0"
        )
        version_label.pack(side=tk.TOP)
    
    def create_settings_frame(self):
        """Create frame for general settings"""
        # Settings frame
        self.settings_frame = tk.LabelFrame(self.root, text="General Settings")
        self.settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create a grid layout
        for i in range(3):
            self.settings_frame.columnconfigure(i, weight=1)
        
        # Symbol settings
        tk.Label(self.settings_frame, text="Cryptocurrency Symbol:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.symbol_entry = tk.Entry(self.settings_frame)
        self.symbol_entry.insert(0, "BTC/USDT")
        self.symbol_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        symbol_tooltip = ToolTip(
            self.symbol_entry, 
            "Enter the trading pair symbol (e.g., BTC/USDT, ETH/USDT)"
        )
        
        # Timeframe settings
        tk.Label(self.settings_frame, text="Timeframe:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.timeframe_combo = ttk.Combobox(
            self.settings_frame, 
            values=["1m", "5m", "15m", "30m", "1h", "4h", "1d"]
        )
        self.timeframe_combo.current(3)  # Default to 30m
        self.timeframe_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        timeframe_tooltip = ToolTip(
            self.timeframe_combo, 
            "Select the chart timeframe (1m = 1 minute, 1h = 1 hour, 1d = 1 day)"
        )
        
        # Signal combination mode
        tk.Label(self.settings_frame, text="Signal Combination Mode:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.signal_mode_combo = ttk.Combobox(
            self.settings_frame, 
            values=["majority", "consensus", "any"]
        )
        self.signal_mode_combo.current(0)  # Default to majority
        self.signal_mode_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        mode_tooltip = ToolTip(
            self.signal_mode_combo, 
            "Majority: Most frequent signal wins\n"
            "Consensus: All strategies must agree\n"
            "Any: Take action if any strategy gives a signal"
        )
    
    def create_strategy_tabs(self):
        """Create tabbed interface for strategy configuration"""
        # Create a notebook (tabbed interface)
        self.strategy_notebook = ttk.Notebook(self.root)
        self.strategy_notebook.pack(fill=tk.X, padx=10, pady=5)
        
        # Create tabs for each strategy
        self.supertrend_tab, self.supertrend_vars = create_supertrend_tab(self.strategy_notebook)
        self.gc_tab, self.gc_vars = create_golden_cross_tab(self.strategy_notebook)
        self.bb_tab, self.bb_vars = create_bollinger_bands_tab(self.strategy_notebook)
        self.fr_tab, self.fr_vars = create_funding_rate_tab(self.strategy_notebook)
    
    def create_charts_frame(self):
        """Create frame for charts and visualizations"""
        self.charts_frame = tk.LabelFrame(self.root, text="Chart Analysis")
        self.charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create a figure with subplots for each strategy
        self.fig, self.axs = plt.subplots(2, 2, figsize=(10, 8))
        self.axs = self.axs.flatten()
        
        # Configure the subplots
        for ax in self.axs:
            ax.grid(True)
            ax.set_title("Waiting for data...")
            
        # Create canvas for matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.charts_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_console_frame(self):
        """Create frame for console output"""
        self.console_frame = tk.LabelFrame(self.root, text="Trading Console")
        self.console_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create scrolled text widget for console output
        self.console = scrolledtext.ScrolledText(self.console_frame, height=6)
        self.console.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Add a signal indicator frame
        self.signal_frame = tk.Frame(self.console_frame)
        self.signal_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create signal indicators
        strategies = ["Supertrend", "Golden_Cross", "Bollinger_Bands", "Funding_Rate", "Combined"]
        self.signal_labels = {}
        
        for i, strategy in enumerate(strategies):
            display_name = strategy.replace('_', ' ')
            tk.Label(self.signal_frame, text=f"{display_name}:").grid(row=0, column=i*2, padx=5)
            signal_label = tk.Label(self.signal_frame, text="WAIT", width=5, bg="yellow")
            signal_label.grid(row=0, column=i*2+1, padx=5)
            self.signal_labels[strategy] = signal_label
    
    def create_control_buttons(self):
        """Create control buttons"""
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Start button
        self.start_button = tk.Button(
            button_frame, 
            text="Start Bot", 
            command=self.start_bot, 
            width=15
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_button = tk.Button(
            button_frame, 
            text="Stop Bot", 
            command=self.stop_bot, 
            width=15, 
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Update settings button
        self.update_button = tk.Button(
            button_frame, 
            text="Update Settings", 
            command=self.update_settings, 
            width=15
        )
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        # Clear console button
        self.clear_button = tk.Button(
            button_frame, 
            text="Clear Console", 
            command=self.clear_console, 
            width=15
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
    
    def update_settings(self):
        """Update all strategy settings"""
        try:
            # Update Supertrend strategy
            params = {
                'is_active': self.supertrend_vars['active'].get(),
                'period': int(self.supertrend_vars['period'].get()),
                'multiplier': float(self.supertrend_vars['multiplier'].get())
            }
            self.bot.strategies[0].set_parameters(params)
            
            # Update Golden Cross strategy
            params = {
                'is_active': self.gc_vars['active'].get(),
                'short_period': int(self.gc_vars['short_period'].get()),
                'long_period': int(self.gc_vars['long_period'].get())
            }
            self.bot.strategies[1].set_parameters(params)
            
            # Update Bollinger Bands strategy
            params = {
                'is_active': self.bb_vars['active'].get(),
                'period': int(self.bb_vars['period'].get()),
                'num_std': float(self.bb_vars['std_dev'].get())
            }
            self.bot.strategies[2].set_parameters(params)
            
            # Update Funding Rate strategy
            params = {
                'is_active': self.fr_vars['active'].get(),
                'threshold': float(self.fr_vars['threshold'].get()) / 100.0
            }
            self.bot.strategies[3].set_parameters(params)
            
            self.log("Settings updated successfully")
            
        except Exception as e:
            self.log(f"Error updating settings: {str(e)}")
    
    def start_bot(self):
        """Start the trading bot"""
        self.update_settings()
        self.running = True
        
        # Disable start button, enable stop button
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Log start message
        self.log(f"Starting bot for {self.symbol_entry.get()} on {self.timeframe_combo.get()} timeframe")
        
        # Start the bot thread
        self.bot_thread = threading.Thread(target=self.run_bot)
        self.bot_thread.daemon = True
        self.bot_thread.start()
    
    def stop_bot(self):
        """Stop the trading bot"""
        self.running = False
        
        # Enable start button, disable stop button
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Log stop message
        self.log("Bot stopped.")
    
    def clear_console(self):
        """Clear the console output"""
        self.console.delete(1.0, tk.END)
    
    def log(self, message):
        """Add a message to the console with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.console.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console.see(tk.END)
    
    def update_signal_label(self, strategy, signal):
        """Update the signal indicator for a strategy"""
        if strategy in self.signal_labels:
            label = self.signal_labels[strategy]
            
            if signal == 'buy':
                label.config(text="BUY", bg="green", fg="white")
            elif signal == 'sell':
                label.config(text="SELL", bg="red", fg="white")
            else:
                label.config(text="HOLD", bg="yellow", fg="black")
    
    def run_bot(self):
        """Main bot loop"""
        while self.running:
            try:
                # Fetch data
                symbol = self.symbol_entry.get()
                timeframe = self.timeframe_combo.get()
                data = self.bot.fetch_data(symbol, timeframe)
                
                if data is not None:
                    # Run strategies
                    strategy_results = self.bot.run_strategies()
                    
                    # Update charts
                    self.update_charts(strategy_results)
                    
                    # Update signals
                    for name, result in strategy_results.items():
                        safe_name = name.replace(' ', '_').replace('/', '_')
                        self.update_signal_label(safe_name, result['signal'])
                    
                    # Get combined signal
                    combined_signal = self.bot.get_combined_signal(self.signal_mode_combo.get())
                    self.update_signal_label('Combined', combined_signal)
                    
                    # Execute order if needed
                    if combined_signal in ['buy', 'sell']:
                        order_executed = self.bot.execute_order(symbol, combined_signal)
                        if order_executed:
                            self.log(f"Executed {combined_signal.upper()} order for {symbol}")
                    
                    self.log(f"Analysis completed. Combined signal: {combined_signal.upper()}")
                
                # Update the UI
                self.canvas.draw()
                
                # Wait for the next update
                for i in range(60):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                self.log(f"Error: {str(e)}")
                time.sleep(10)
    
    def update_charts(self, strategy_results):
        """Update all charts with new data"""
        # Clear all subplots
        for ax in self.axs:
            ax.clear()
            ax.grid(True)
        
        # Plot each strategy
        plot_index = 0
        for name, result in strategy_results.items():
            if plot_index < len(self.axs):
                strategy = None
                for s in self.bot.strategies:
                    if s.name == name:
                        strategy = s
                        break
                
                if strategy:
                    strategy.plot(result['data'], self.axs[plot_index])
                plot_index += 1
        
        # Set title for the figure
        symbol = self.symbol_entry.get()
        timeframe = self.timeframe_combo.get()
        self.fig.suptitle(f"{symbol} Analysis - {timeframe} Timeframe", fontsize=14)
        
        # Adjust layout
        self.fig.tight_layout(rect=[0, 0, 1, 0.95])  # Make room for the figure title