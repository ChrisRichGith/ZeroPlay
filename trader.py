# trader.py
"""
Defines the Trader class for handling item selling and inventory upgrades.
"""

class Trader:
    """Manages all trading-related logic."""

    def __init__(self):
        """Initializes the trader."""
        self.inventory_upgrade_cost = 100
        self.upgrade_cost_increase_factor = 1.8

    def sell_item(self, character, item_index):
        """
        Sells an item from the character's inventory.

        Args:
            character (Character): The player character.
            item_index (int): The index of the item to sell.

        Returns:
            bool: True if the sale was successful, False otherwise.
        """
        if 0 <= item_index < len(character.inventory):
            item_to_sell = character.inventory.pop(item_index)
            character.gold += item_to_sell.value
            return True
        return False

    def get_upgrade_cost(self):
        """Returns the current cost for the next inventory upgrade."""
        return self.inventory_upgrade_cost

    def buy_inventory_upgrade(self, character):
        """
        Upgrades the character's inventory size if they have enough gold.

        Args:
            character (Character): The player character.

        Returns:
            bool: True if the upgrade was successful, False otherwise.
        """
        if character.gold >= self.inventory_upgrade_cost:
            character.gold -= self.inventory_upgrade_cost
            character.max_inventory_size += 5  # Increase inventory by 5 slots

            # Increase the cost for the next upgrade
            self.inventory_upgrade_cost = int(self.inventory_upgrade_cost * self.upgrade_cost_increase_factor)
            return True
        return False