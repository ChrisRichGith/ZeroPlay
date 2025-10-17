# game_data.py
"""
Contains static game data, such as class definitions.
"""

CLASSES = {
    "Krieger": {
        "description": "Ein Meister des Nahkampfs, robust und stark.",
        "attributes": {'Stärke': 8, 'Intelligenz': 3, 'Glück': 4}
    },
    "Magier": {
        "description": "Ein weiser Gelehrter, der arkane Energien bändigt.",
        "attributes": {'Stärke': 3, 'Intelligenz': 8, 'Glück': 4}
    },
    "Schurke": {
        "description": "Ein listiger Halunke, der sein Glück selbst in die Hand nimmt.",
        "attributes": {'Stärke': 5, 'Intelligenz': 5, 'Glück': 7}
    }
}

ITEM_BLUEPRINTS = {
    "Waffe": [
        {"name": "Schwert", "base_stat": "Stärke", "base_bonus": 2},
        {"name": "Stab", "base_stat": "Intelligenz", "base_bonus": 2},
        {"name": "Dolch", "base_stat": "Glück", "base_bonus": 1},
    ],
    "Kopf": [
        {"name": "Helm", "base_stat": "Stärke", "base_bonus": 1},
        {"name": "Hut", "base_stat": "Intelligenz", "base_bonus": 1},
        {"name": "Kapuze", "base_stat": "Glück", "base_bonus": 1},
    ],
    "Brust": [
        {"name": "Plattenpanzer", "base_stat": "Stärke", "base_bonus": 3},
        {"name": "Robe", "base_stat": "Intelligenz", "base_bonus": 3},
        {"name": "Lederwams", "base_stat": "Glück", "base_bonus": 2},
    ]
}

ITEM_PREFIXES = {
    -2: "Kaputter",
    -1: "Minderwertiger",
    0: "Gewöhnlicher",
    1: "Verbesserter",
    2: "Seltener",
    3: "Epischer",
    4: "Legendärer"
}