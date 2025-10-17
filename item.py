# item.py
"""
Defines the Item class for all in-game items.
"""
import random

class Item:
    """Represents an item in the game with a name, type, value, and potential effects."""

    def __init__(self, name, item_type="Ausrüstung", slot=None, stats_boost=None, value=0):
        """
        Initializes an Item.

        Args:
            name (str): The name of the item.
            item_type (str): The type of item ('Ausrüstung' or 'Verbrauchsgut').
            slot (str, optional): The equipment slot for 'Ausrüstung' type.
            stats_boost (dict, optional): Stat boosts or consumable effects (e.g., {'LP': 50}).
            value (int): The gold value of the item.
        """
        self.name = name
        self.item_type = item_type
        self.slot = slot
        self.stats_boost = stats_boost if stats_boost else {}
        self.value = value

    def __str__(self):
        """Returns a string representation of the item."""
        if self.item_type == "Ausrüstung":
            boosts = []
            if self.stats_boost:
                for stat, val in self.stats_boost.items():
                    boosts.append(f"{'+' if val >= 0 else ''}{val} {stat}")
            boost_str = ", ".join(boosts)
            return f"{self.name} ({self.slot}) [{boost_str}] - {self.value} Gold"
        elif self.item_type == "Verbrauchsgut":
            effects = []
            if self.stats_boost:
                for stat, val in self.stats_boost.items():
                    effects.append(f"Stellt {val} {stat} wieder her")
            effect_str = ", ".join(effects)
            return f"{self.name} [{effect_str}] - {self.value} Gold"
        return f"{self.name} - {self.value} Gold"

    def get_weighted_score(self, main_stat, main_stat_weight=1.5):
        """
        Calculates a weighted score for an item based on a main stat.

        Args:
            main_stat (str): The primary stat for the character class.
            main_stat_weight (float): The multiplier for the main stat.

        Returns:
            float: The calculated weighted score of the item.
        """
        if not self.stats_boost:
            return 0

        score = 0
        for stat, value in self.stats_boost.items():
            if stat == main_stat:
                score += value * main_stat_weight
            else:
                score += value # Other stats have a weight of 1
        return score