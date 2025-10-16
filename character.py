# character.py
"""
Defines the Character class, which manages the player's stats, inventory, and equipment.
"""
from item import Item

class Character:
    """Manages character attributes, inventory, and equipment."""

    def __init__(self, name, klasse):
        """
        Initializes a new character.

        Args:
            name (str): The character's name.
            klasse (str): The character's class.
        """
        self.name = name
        self.klasse = klasse
        self.level = 1
        self.gold = 0
        self.attributes = {'Stärke': 5, 'Intelligenz': 5, 'Glück': 5}
        self.inventory = []
        self.equipment = {'Kopf': None, 'Brust': None, 'Waffe': None}

    def add_loot(self, gold, item):
        """
        Adds gold and an item to the character's inventory.

        Args:
            gold (int): The amount of gold to add.
            item (Item): The item to add.
        """
        self.gold += gold
        if item:
            self.inventory.append(item)
        print(f"Loot erhalten: {gold} Gold und {item.name if item else 'nichts'}.")

    def equip(self, item_index):
        """
        Equips an item from the inventory.

        Args:
            item_index (int): The index of the item in the inventory.
        """
        if 0 <= item_index < len(self.inventory):
            item_to_equip = self.inventory[item_index]
            slot = item_to_equip.slot

            if slot in self.equipment:
                # Item ausziehen und ins Inventar legen
                if self.equipment[slot]:
                    self.inventory.append(self.equipment[slot])

                # Neues Item ausrüsten
                self.equipment[slot] = item_to_equip
                self.inventory.pop(item_index)
                print(f"{item_to_equip.name} wurde ausgerüstet.")
            else:
                print("Dieser Gegenstand kann nicht ausgerüstet werden.")
        else:
            print("Ungültiger Inventarplatz.")

    def get_total_stats(self):
        """
        Calculates total stats including bonuses from equipped items.

        Returns:
            dict: A dictionary with the total stats.
        """
        total_stats = self.attributes.copy()
        for slot, item in self.equipment.items():
            if item:
                for stat, boost in item.stats_boost.items():
                    if stat in total_stats:
                        total_stats[stat] += boost
        return total_stats

    def display_status(self):
        """Prints a detailed status screen for the character."""
        total_stats = self.get_total_stats()
        print("\n--- CHARAKTERSTATUS ---")
        print(f"Name: {self.name}, Klasse: {self.klasse}, Level: {self.level}")
        print(f"Gold: {self.gold}")
        print("\nAttribute:")
        for stat, value in total_stats.items():
            base_value = self.attributes.get(stat, 0)
            bonus = value - base_value
            if bonus > 0:
                print(f"  - {stat}: {value} ({base_value} + {bonus})")
            else:
                print(f"  - {stat}: {value}")

        print("\nAusrüstung:")
        for slot, item in self.equipment.items():
            item_name = item.name if item else "Leer"
            print(f"  - {slot}: {item_name}")

        print("\nInventar:")
        if self.inventory:
            for i, item in enumerate(self.inventory):
                print(f"  {i}: {item}")
        else:
            print("  - Leer")
        print("-----------------------\n")