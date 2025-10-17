# start_menu_gui.py
"""
Defines the GUI for the main start menu.
"""
import tkinter as tk
from tkinter import ttk
from save_load_system import get_save_files

class StartMenu:
    """Manages the start menu GUI."""

    def __init__(self, root):
        self.root = root
        self.root.title("Progress Quest 2.0 - Hauptmenü")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.choice = None # To store user's action: 'load', 'new', 'quit'
        self.selected_save = None

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Verfügbare Spielstände:", font=("Helvetica", 12)).pack(pady=5)

        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.save_listbox = tk.Listbox(list_frame)
        self.save_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.save_listbox.yview)
        self.save_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.populate_save_list()
        self.save_listbox.bind('<<ListboxSelect>>', self.on_select)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        self.load_button = ttk.Button(button_frame, text="Laden", command=self.load_game, state=tk.DISABLED)
        self.load_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        new_game_button = ttk.Button(button_frame, text="Neues Spiel", command=self.new_game)
        new_game_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        quit_button = ttk.Button(button_frame, text="Beenden", command=self.quit_game)
        quit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    def populate_save_list(self):
        """Fills the listbox with available save files."""
        self.save_listbox.delete(0, tk.END)
        for save_name in get_save_files():
            self.save_listbox.insert(tk.END, save_name)

    def on_select(self, event=None):
        """Enables the load button when a save is selected."""
        if self.save_listbox.curselection():
            self.load_button.config(state=tk.NORMAL)
        else:
            self.load_button.config(state=tk.DISABLED)

    def load_game(self):
        self.choice = 'load'
        self.selected_save = self.save_listbox.get(self.save_listbox.curselection())
        self.root.destroy()

    def new_game(self):
        self.choice = 'new'
        self.root.destroy()

    def quit_game(self):
        self.choice = 'quit'
        self.root.destroy()