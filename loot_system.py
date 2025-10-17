# loot_system.py
"""
Handles the dynamic generation of loot based on player level.
"""
import random
from item import Item
from game_data import ITEM_BLUEPRINTS, ITEM_PREFIXES

def generate_item_for_level(level):
    """
    Generates a new item with stats and value scaled to the given level.

    Args:
        level (int): The player's current level.

    Returns:
        Item: A newly generated Item object.
    """
    # 1. Randomly select a slot and a blueprint for that slot
    slot = random.choice(list(ITEM_BLUEPRINTS.keys()))
    blueprint = random.choice(ITEM_BLUEPRINTS[slot])

    # 2. Calculate the item's power level and corresponding prefix
    # Higher player level increases the chance for better prefixes
    power_roll = random.randint(-2, 4) + int(level / 5)
    power_level = max(min(power_roll, 4), -2) # Clamp between -2 and 4
    prefix = ITEM_PREFIXES.get(power_level, "Gewöhnlicher")

    # 3. Calculate stat bonus
    base_bonus = blueprint["base_bonus"]
    # Formula: Bonus scales with level and is modified by power level
    stat_bonus = int(base_bonus + (level * 0.8) + (power_level * 2))

    # 4. Calculate item value
    # Formula: Value in copper. Scales with level and is modified by power level.
    value = int((level * 2) + (stat_bonus * 1.5) * (1 + power_level * 0.4))
    value = max(1, value) # Ensure value is at least 1

    # 5. Assemble the item
    item_name = f"{prefix} {blueprint['name']}"
    stats_boost = {blueprint["base_stat"]: stat_bonus}

    return Item(name=item_name, slot=slot, stats_boost=stats_boost, value=value)


# Example usage for testing:
if __name__ == '__main__':
    for lvl in [1, 5, 10, 20, 50]:
        print(f"--- Generating Item for Level {lvl} ---")
        for _ in range(3):
            new_item = generate_item_for_level(lvl)
            print(new_item)
        print("-" * 20)