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