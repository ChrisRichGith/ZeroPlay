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