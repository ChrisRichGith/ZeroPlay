# loot_system.py
"""
Handles the dynamic generation of loot based on player level.
"""
import random
from item import Item
from game_data import ITEM_BLUEPRINTS, RARITIES

def generate_item_for_level(level, luck):
    """
    Generates a new item with stats, rarity, and value scaled to the given level.

    Args:
        level (int): The player's current level.
        luck (int): The player's luck attribute, influences rarity.

    Returns:
        Item: A newly generated Item object.
    """
    # 1. Choose a rarity based on level and luck
    available_rarities = {r: data for r, data in RARITIES.items() if level >= data["min_level"]}

    rarity_names = list(available_rarities.keys())
    rarity_weights = [data["weight"] for data in available_rarities.values()]

    # Luck increases the chance of finding better items
    luck_factor = 1 + (luck / 100) # 50 luck = 1.5x weight for better items
    for i, r_name in enumerate(rarity_names):
        if r_name not in ["Schlecht", "Gewöhnlich"]:
             rarity_weights[i] *= luck_factor

    chosen_rarity_name = random.choices(rarity_names, weights=rarity_weights, k=1)[0]
    rarity_data = RARITIES[chosen_rarity_name]

    # 2. Select a slot and a blueprint
    slot = random.choice(list(ITEM_BLUEPRINTS.keys()))
    blueprint = random.choice(ITEM_BLUEPRINTS[slot])

    # 3. Assemble the item name
    item_name = f"{chosen_rarity_name} {blueprint['name'][0]}"

    # 4. Calculate stat bonuses
    stats_boost = {}

    # Primary stat bonus calculation
    base_bonus = blueprint["base_bonus"]
    # Formula: Bonus scales with level and is modified by rarity
    primary_stat_value = int((base_bonus + (level * 0.9)) * rarity_data["modifier"])

    # Add some variance (+/- 5%) to create "+" versions implicitly
    primary_stat_value = int(primary_stat_value * random.uniform(0.95, 1.05))
    stats_boost[blueprint["base_stat"]] = max(1, primary_stat_value)

    # Add secondary stats for higher rarities
    all_stats = ["Stärke", "Intelligenz", "Glück"]
    if chosen_rarity_name in ["Episch", "Legendär", "Mythisch"]:
        possible_secondary_stats = [s for s in all_stats if s != blueprint["base_stat"]]
        if possible_secondary_stats:
            secondary_stat = random.choice(possible_secondary_stats)
            secondary_value = int(primary_stat_value * 0.4) # Secondary stat is 40% of primary
            stats_boost[secondary_stat] = max(1, secondary_value)

    if chosen_rarity_name == "Mythisch":
        # A third stat for mythisch items
        possible_tertiary_stats = [s for s in all_stats if s not in stats_boost]
        if possible_tertiary_stats:
            tertiary_stat = random.choice(possible_tertiary_stats)
            tertiary_value = int(primary_stat_value * 0.25) # Tertiary stat is 25% of primary
            stats_boost[tertiary_stat] = max(1, tertiary_value)

    # 5. Calculate item value
    total_stat_points = sum(stats_boost.values())
    value = int((level * 1.5) + (total_stat_points * 2.0) * rarity_data["modifier"])
    value = max(1, value)

    return Item(
        name=item_name,
        slot=slot,
        stats_boost=stats_boost,
        value=value,
        rarity=chosen_rarity_name,
        color=rarity_data["color"]
    )


# Example usage for testing:
if __name__ == '__main__':
    for lvl in [1, 5, 10, 20, 50]:
        print(f"--- Generating Item for Level {lvl} ---")
        for _ in range(3):
            new_item = generate_item_for_level(lvl)
            print(new_item)
        print("-" * 20)