# character.py
"""
Defines the Character class, which manages the player's stats, inventory, and equipment.
"""
import random
from item import Item
from game_data import CLASSES

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
        self.xp = 0
        self.xp_to_next_level = 100
        self.copper = 0
        # Load base attributes and image path from the selected class
        class_data = CLASSES.get(klasse, {})
        self.attributes = class_data.get("attributes", {'Stärke': 5, 'Intelligenz': 5, 'Glück': 5}).copy()
        self.image_path = class_data.get("image_path", None)  # Store the image path
        self.inventory = []
        self.max_inventory_size = 10
        self.equipment = {'Kopf': None, 'Brust': None, 'Waffe': None}

        # Derived stats
        self.max_lp = 0
        self.current_lp = 0
        self.max_mp = 0
        self.current_mp = 0
        self.update_derived_stats(heal_on_update=True) # Initial calculation and full heal

    def update_derived_stats(self, heal_on_update=False):
        """
        Calculates derived stats like LP and MP based on base attributes.
        Does not heal the character unless specified (e.g., on level up).
        """
        total_stats = self.get_total_stats()
        old_max_lp = self.max_lp
        old_max_mp = self.max_mp

        self.max_lp = 50 + total_stats['Stärke'] * 5
        self.max_mp = 30 + total_stats['Intelligenz'] * 3

        # Keep current values unless they exceed the new max
        self.current_lp = min(self.current_lp, self.max_lp)
        self.current_mp = min(self.current_mp, self.max_mp)

        if heal_on_update:
            self.current_lp = self.max_lp
            self.current_mp = self.max_mp

    def _calculate_xp_for_next_level(self):
        """Calculates the XP needed for the next level."""
        return int(100 * (self.level ** 1.5))

    def add_xp(self, amount):
        """
        Adds XP to the character and checks for level ups.

        Returns:
            list: A list of strings describing the attribute increases on level up, or empty list.
        """
        self.xp += amount
        level_up_messages = []
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            level_up_messages.extend(self.level_up())
        return level_up_messages

    def level_up(self):
        """Handles the character's level up process."""
        self.level += 1
        self.xp_to_next_level = self._calculate_xp_for_next_level()

        stat_increases = []
        # Increase 1 to 2 random stats
        stats_to_increase = random.sample(list(self.attributes.keys()), k=random.randint(1, 2))
        for stat in stats_to_increase:
            increase = random.randint(1, 2)
            self.attributes[stat] += increase
            stat_increases.append(f"{stat} +{increase}")

        self.update_derived_stats(heal_on_update=True) # Recalculate LP/MP and heal on level up
        return stat_increases

    def use_item(self, item_index):
        """Uses a consumable item from the inventory."""
        if not (0 <= item_index < len(self.inventory)):
            return False, "Ungültiger Gegenstand."

        item = self.inventory[item_index]
        if item.item_type != "Verbrauchsgut":
            return False, "Dieser Gegenstand kann nicht benutzt werden."

        effect = item.stats_boost
        if "LP" in effect:
            self.current_lp = min(self.max_lp, self.current_lp + effect["LP"])
        if "MP" in effect:
            self.current_mp = min(self.max_mp, self.current_mp + effect["MP"])

        self.inventory.pop(item_index)
        return True, f"{item.name} benutzt."

    def add_loot(self, copper, item):
        """
        Adds copper and an item to the character's inventory if there is space.

        Returns:
            bool: True if the item was added, False otherwise.
        """
        self.copper += copper
        if item:
            if len(self.inventory) < self.max_inventory_size:
                self.inventory.append(item)
                return True
            else:
                return False
        return True

    def is_upgrade(self, item_from_inventory):
        """
        Checks if an item in the inventory is an upgrade over the equipped item.

        Args:
            item_from_inventory (Item): The item to check.

        Returns:
            bool: True if the item is an upgrade, False otherwise.
        """
        if item_from_inventory.item_type != "Ausrüstung":
            return False

        equipped_item = self.equipment.get(item_from_inventory.slot)
        main_stat = CLASSES[self.klasse]['main_stat']

        if not equipped_item:
            # Any item is an upgrade if the slot is empty, provided it has a positive score
            return item_from_inventory.get_weighted_score(main_stat) > 0

        # Compare the weighted scores
        new_item_score = item_from_inventory.get_weighted_score(main_stat)
        equipped_item_score = equipped_item.get_weighted_score(main_stat)

        return new_item_score > equipped_item_score

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
                if self.equipment[slot]:
                    self.inventory.append(self.equipment[slot])

                self.equipment[slot] = item_to_equip
                self.inventory.pop(item_index)
                self.update_derived_stats()

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
        """DEPRECATED: Prints a detailed status screen for the character."""
        # This method is no longer used by the GUI but kept for potential CLI debugging.
        total_stats = self.get_total_stats()
        print("\n--- CHARAKTERSTATUS ---")
        print(f"Name: {self.name}, Klasse: {self.klasse}, Level: {self.level}")
        print(f"LP: {self.current_lp}/{self.max_lp} | MP: {self.current_mp}/{self.max_mp}")
        print(f"XP: {self.xp}/{self.xp_to_next_level}")
        print(f"Gold: {self.copper}")
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