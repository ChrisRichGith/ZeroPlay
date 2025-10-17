# start_menu_gui.py
"""
Defines the GUI Frame for the main start menu.
"""
import tkinter as tk
from tkinter import ttk
from save_load_system import get_save_files

class StartMenu(ttk.Frame):
    """Manages the start menu frame."""

    def __init__(self, parent, callbacks):
        super().__init__(parent)
        self.callbacks = callbacks # e.g., {'load': on_load, 'new': on_new, 'quit': on_quit}

        self.selected_save = None

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Verfügbare Spielstände:", font=("Helvetica", 12)).pack(pady=5)

        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.save_listbox = tk.Listbox(list_frame)
        self.save_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.save_listbox.yview)
        self.save_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.populate_save_list()
        self.save_listbox.bind('<<ListboxSelect>>', self.on_select)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.load_button = ttk.Button(button_frame, text="Laden", command=self.load_game, state=tk.DISABLED)
        self.load_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        new_game_button = ttk.Button(button_frame, text="Neues Spiel", command=self.callbacks['new'])
        new_game_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        quit_button = ttk.Button(button_frame, text="Beenden", command=self.callbacks['quit'])
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
            self.selected_save = self.save_listbox.get(self.save_listbox.curselection())
        else:
            self.load_button.config(state=tk.DISABLED)
            self.selected_save = None

    def load_game(self):
        if self.selected_save and self.callbacks['load']:
            self.callbacks['load'](self.selected_save)