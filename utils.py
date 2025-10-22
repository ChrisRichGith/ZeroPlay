# utils.py
"""
Contains utility functions for the game, such as currency formatting.
"""

def format_currency(copper_amount):
    """
    Converts a total copper amount into a formatted string (gold, silver, copper).
    100 copper = 1 silver
    100 silver = 1 gold
    """
    if copper_amount == 0:
        return "0c"

    gold = copper_amount // 10000
    silver = (copper_amount % 10000) // 100
    copper = copper_amount % 100

    parts = []
    if gold > 0:
        parts.append(f"{gold}g")
    if silver > 0:
        parts.append(f"{silver}s")
    if copper > 0:
        parts.append(f"{copper}c")

    return " ".join(parts)

def center_window(window):
    """
    Centers a tkinter window on the screen.

    Args:
        window: The tkinter window (Tk or Toplevel) to center.
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')