# item.py
"""
Defines the Item class for all in-game items.
"""
import random

class Item:
    """Represents an item in the game with a name, slot, value, and potential stat boosts."""

    def __init__(self, name, slot, stats_boost=None, value=0):
        """
        Initializes an Item.

        Args:
            name (str): The name of the item.
            slot (str): The equipment slot (e.g., 'Kopf', 'Brust', 'Waffe').
            stats_boost (dict, optional): A dictionary of stat boosts (e.g., {'Stärke': 1}).
            value (int): The gold value of the item.
        """
        self.name = name
        self.slot = slot
        self.stats_boost = stats_boost if stats_boost else {}
        self.value = value

    def __str__(self):
        """Returns a string representation of the item."""
        boosts = []
        if self.stats_boost:
            for stat, val in self.stats_boost.items():
                boosts.append(f"{'+' if val >= 0 else ''}{val} {stat}")
        boost_str = ", ".join(boosts)

        return f"{self.name} ({self.slot}) [{boost_str}] - {self.value} Gold"

    def get_total_bonus(self):
        """Calculates the sum of all stat boosts of the item."""
        if not self.stats_boost:
            return 0
        return sum(self.stats_boost.values())