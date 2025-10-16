# item.py
"""
Defines the Item class for all in-game items.
"""
import random

class Item:
    """Represents an item in the game with a name, slot, and potential stat boosts."""

    def __init__(self, name, slot, stats_boost=None):
        """
        Initializes an Item.

        Args:
            name (str): The name of the item.
            slot (str): The equipment slot (e.g., 'Kopf', 'Brust', 'Waffe').
            stats_boost (dict, optional): A dictionary of stat boosts (e.g., {'Stärke': 1}).
        """
        self.name = name
        self.slot = slot
        self.stats_boost = stats_boost if stats_boost else {}

    def __str__(self):
        """Returns a string representation of the item."""
        boosts = []
        for stat, value in self.stats_boost.items():
            if value >= 0:
                boosts.append(f"+{value} {stat}")
            else:
                boosts.append(f"{value} {stat}")
        boost_str = ", ".join(boosts)
        return f"{self.name} ({self.slot}) [{boost_str}]"