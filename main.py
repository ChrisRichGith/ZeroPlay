# main.py
"""
Main entry point for the RPG. Launches the start menu and handles game flow.
"""
import tkinter as tk
from start_menu_gui import StartMenu
from rpg_gui import RpgGui, start_game_with_character_creation
from save_load_system import load_game

def main():
    """
    Handles the main game flow: start menu -> character creation/load -> game.
    """
    # Show start menu
    root = tk.Tk()
    start_menu = StartMenu(root)
    root.mainloop()

    choice = start_menu.choice
    character = None

    if choice == 'load':
        character = load_game(start_menu.selected_save)
    elif choice == 'new':
        player_name, player_class = start_game_with_character_creation()
        if player_name and player_class:
            from character import Character # Import here to avoid circular dependency issues
            character = Character(player_name, player_class)
    elif choice == 'quit':
        return # Exit the application

    if character:
        game_root = tk.Tk()
        app = RpgGui(game_root, character)
        game_root.mainloop()

if __name__ == "__main__":
    main()