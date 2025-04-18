"""
GUI Utilities Module

Provides utility classes and functions for the GUI components.
"""

import tkinter as tk

class ToolTip:
    """Create a tooltip for a given widget"""
    
    def __init__(self, widget, text):
        """
        Initialize a tooltip
        
        Args:
            widget: The widget to attach the tooltip to
            text (str): The tooltip text
        """
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.tip_window = None

    def enter(self, event=None):
        """Show the tooltip when mouse enters the widget"""
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Create a toplevel window
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            tw, 
            text=self.text, 
            justify=tk.LEFT,
            background="#ffffe0", 
            relief=tk.SOLID, 
            borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def leave(self, event=None):
        """Hide the tooltip when mouse leaves the widget"""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

def create_button(parent, text, command, width=15, state=tk.NORMAL):
    """
    Create a standardized button
    
    Args:
        parent: Parent widget
        text (str): Button text
        command: Button command
        width (int, optional): Button width
        state: Button state
        
    Returns:
        tk.Button: The created button
    """
    button = tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        state=state
    )
    return button

def create_status_indicator(parent, text, color="yellow"):
    """
    Create a status indicator label
    
    Args:
        parent: Parent widget
        text (str): Label text
        color (str, optional): Background color
        
    Returns:
        tk.Label: The created label
    """
    label = tk.Label(
        parent, 
        text=text, 
        width=8, 
        bg=color, 
        relief=tk.RIDGE
    )
    return label