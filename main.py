# main.py
"""
The main entry point for the text-based RPG.
This script now launches the graphical user interface.
"""
from rpg_gui import start_game_with_character_creation

def main():
    """
    Launches the GUI version of the RPG.
    """
    start_game_with_character_creation()

if __name__ == "__main__":
    main()