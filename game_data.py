# game_data.py
"""
Contains static game data, such as class definitions.
"""

CLASSES = {
    "Krieger": {
        "description": "Ein Meister des Nahkampfs, robust und stark.",
        "attributes": {'Stärke': 8, 'Intelligenz': 3, 'Glück': 4},
        "main_stat": "Stärke"
    },
    "Magier": {
        "description": "Ein weiser Gelehrter, der arkane Energien bändigt.",
        "attributes": {'Stärke': 3, 'Intelligenz': 8, 'Glück': 4},
        "main_stat": "Intelligenz"
    },
    "Schurke": {
        "description": "Ein listiger Halunke, der sein Glück selbst in die Hand nimmt.",
        "attributes": {'Stärke': 5, 'Intelligenz': 5, 'Glück': 7},
        "main_stat": "Glück"
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

# Adjektiv-Endungen für (m, f, n) Artikel
ITEM_PREFIXES = {
    -2: "Kaputt",
    -1: "Minderwertig",
    0: "Gewöhnlich",
    1: "Verbessert",
    2: "Selten",
    3: "Episch",
    4: "Legendär"
}