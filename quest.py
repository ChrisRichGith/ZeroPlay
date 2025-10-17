# quest.py
"""
Defines the Quest class, which handles quest progression and rewards.
"""
import random
import time
from item import Item
from loot_system import generate_item_for_level

class Quest:
    """Represents a quest that automatically progresses and grants rewards."""

    def __init__(self, description, duration=10):
        """
        Initializes a new quest.

        Args:
            description (str): The description of the quest.
            duration (int): The number of 'ticks' required to complete the quest.
        """
        self.description = description
        self.duration = duration
        self.progress = 0

    def is_complete(self):
        """Checks if the quest is complete."""
        return self.progress >= self.duration

    def advance(self, character):
        """
        Advances the quest progress. This is now just a progress ticker.
        The reward logic is handled by the GUI.
        """
        if not self.is_complete():
            self.progress += 1

            # On completion, inflict a small amount of damage
            if self.is_complete():
                character.current_lp = max(0, character.current_lp - random.randint(5, 15))


    def generate_reward(self, character):
        """
        Generates random gold, XP, and an item, influenced by character's luck.

        Args:
            character (Character): The character receiving the reward.

        Returns:
            tuple: A tuple containing gold, xp, and an Item object (or None).
        """
        luck_bonus = 1 + (character.get_total_stats()['Glück'] / 100) # e.g., 10 luck = 10% bonus

        copper_reward = int((random.randint(50, 250) + self.duration * 10) * luck_bonus)
        xp_reward = int((random.randint(20, 40) + self.duration * 2) * luck_bonus)

        # Luck also slightly increases the chance of finding an item
        item_chance = 0.7 + (character.get_total_stats()['Glück'] / 200) # 10 luck = +5% chance
        if random.random() < min(0.95, item_chance): # Cap at 95%
            item_reward = generate_item_for_level(character.level)
        else:
            item_reward = None

        return copper_reward, xp_reward, item_reward