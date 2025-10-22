# item.py
"""
Defines the Item class for all in-game items.
"""
import random
from utils import format_currency
from game_data import ITEM_ICONS

class Item:
    """Represents an item in the game with a name, type, value, and potential effects."""

    def __init__(self, name, item_type="Ausrüstung", slot=None, stats_boost=None, value=0, rarity="Gewöhnlich", color="#ffffff"):
        """
        Initializes an Item.

        Args:
            name (str): The name of the item.
            item_type (str): The type of item ('Ausrüstung' or 'Verbrauchsgut').
            slot (str, optional): The equipment slot for 'Ausrüstung' type.
            stats_boost (dict, optional): Stat boosts or consumable effects (e.g., {'LP': 50}).
            value (int): The copper value of the item.
            rarity (str): The rarity of the item.
            color (str): The hex color code for the item's rarity.
        """
        self.name = name
        self.item_type = item_type
        self.slot = slot
        self.stats_boost = stats_boost if stats_boost else {}
        self.value = value
        self.rarity = rarity
        self.color = color

        # Assign an icon based on the item type/slot
        self.icon = "❔" # Default icon
        if self.item_type == "Ausrüstung" and self.slot:
            self.icon = ITEM_ICONS.get(self.slot, "❔")
        elif self.item_type == "Verbrauchsgut":
            self.icon = ITEM_ICONS.get("Verbrauchsgut", "❔")


    def __str__(self):
        """Returns a string representation of the item, including its icon."""
        value_str = format_currency(self.value)
        display_name = f"{self.icon} {self.name}"

        if self.item_type == "Ausrüstung":
            boosts = []
            if self.stats_boost:
                for stat, val in self.stats_boost.items():
                    boosts.append(f"{'+' if val >= 0 else ''}{val} {stat}")
            boost_str = ", ".join(boosts)
            return f"{display_name} ({self.slot}) [{boost_str}] - {value_str}"
        elif self.item_type == "Verbrauchsgut":
            effects = []
            if self.stats_boost:
                for stat, val in self.stats_boost.items():
                    effects.append(f"Stellt {val} {stat} wieder her")
            effect_str = ", ".join(effects)
            return f"{display_name} [{effect_str}] - {value_str}"
        return f"{display_name} - {value_str}"

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