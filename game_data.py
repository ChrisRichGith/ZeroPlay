# game_data.py
"""
Contains static game data, such as class definitions.
"""

CLASSES = {
    "Krieger": {
        "description": "Ein Meister des Nahkampfs, robust und stark.",
        "attributes": {'Stärke': 8, 'Intelligenz': 3, 'Glück': 4},
        "main_stat": "Stärke",
        "image_path": "assets/krieger.png"
    },
    "Magier": {
        "description": "Ein weiser Gelehrter, der arkane Energien bändigt.",
        "attributes": {'Stärke': 3, 'Intelligenz': 8, 'Glück': 4},
        "main_stat": "Intelligenz",
        "image_path": "assets/magier.png"
    },
    "Schurke": {
        "description": "Ein listiger Halunke, der sein Glück selbst in die Hand nimmt.",
        "attributes": {'Stärke': 5, 'Intelligenz': 5, 'Glück': 7},
        "main_stat": "Glück",
        "image_path": "assets/schurke.png"
    }
}

ITEM_BLUEPRINTS = {
    # Nomen: (Name, Artikel)
    "Waffe": [
        {"name": ("Schwert", "n"), "base_stat": "Stärke", "base_bonus": 2},
        {"name": ("Stab", "m"), "base_stat": "Intelligenz", "base_bonus": 2},
        {"name": ("Dolch", "m"), "base_stat": "Glück", "base_bonus": 1},
    ],
    "Kopf": [
        {"name": ("Helm", "m"), "base_stat": "Stärke", "base_bonus": 1},
        {"name": ("Hut", "m"), "base_stat": "Intelligenz", "base_bonus": 1},
        {"name": ("Kapuze", "f"), "base_stat": "Glück", "base_bonus": 1},
    ],
    "Brust": [
        {"name": ("Plattenpanzer", "m"), "base_stat": "Stärke", "base_bonus": 3},
        {"name": ("Robe", "f"), "base_stat": "Intelligenz", "base_bonus": 3},
        {"name": ("Lederwams", "m"), "base_stat": "Glück", "base_bonus": 2},
    ]
}

RARITIES = {
    "Schlecht":     {"color": "#B0B0B0", "modifier": 0.7, "min_level": 1, "weight": 10},
    "Gewöhnlich":   {"color": "#FFFFFF", "modifier": 1.0, "min_level": 1, "weight": 70},
    "Ungewöhnlich": {"color": "#1EFF00", "modifier": 1.2, "min_level": 5, "weight": 15},
    "Selten":       {"color": "#68AFFF", "modifier": 1.5, "min_level": 15, "weight": 4},
    "Episch":       {"color": "#A335EE", "modifier": 1.8, "min_level": 30, "weight": 1},
    "Legendär":     {"color": "#FF8000", "modifier": 2.2, "min_level": 50, "weight": 0.1},
    "Mythisch":     {"color": "#E5CC80", "modifier": 2.7, "min_level": 75, "weight": 0.01}
}

ITEM_ICONS = {
    "Waffe": "🗡️",
    "Schild": "🛡️",
    "Kopf": "👑",
    "Brust": "👕",
    "Beine": "👖",
    "Füße": "👢",
    "Verbrauchsgut": "🧪"
}

POTIONS = {
    1: {"name": "Kleiner Heiltrank", "type": "LP", "value": 50, "cost": 25},
    10: {"name": "Heiltrank", "type": "LP", "value": 150, "cost": 100},
    25: {"name": "Großer Heiltrank", "type": "LP", "value": 500, "cost": 500},
    50: {"name": "Überragender Heiltrank", "type": "LP", "value": 2000, "cost": 2500},

    # Mana Potions start with a negative key to distinguish them easily if needed
    -1: {"name": "Kleiner Manatrank", "type": "MP", "value": 30, "cost": 35},
    -10: {"name": "Manatrank", "type": "MP", "value": 100, "cost": 120},
    -25: {"name": "Großer Manatrank", "type": "MP", "value": 400, "cost": 600},
    -50: {"name": "Überragender Manatrank", "type": "MP", "value": 1500, "cost": 3000},
}