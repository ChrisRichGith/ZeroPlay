# start_menu_gui.py
"""
Defines the GUI Frame for the main start menu.
"""
import tkinter as tk
from tkinter import ttk
from save_load_system import get_save_files

from save_load_system import get_save_files, load_game

class StartMenu(ttk.Frame):
    """Manages the start menu frame."""

    def __init__(self, parent, callbacks):
        super().__init__(parent)
        self.callbacks = callbacks # e.g., {'load': on_load, 'new': on_new, 'quit': on_quit}

        self.selected_save = None

        self._setup_vars()
        self.create_widgets()

    def _setup_vars(self):
        """Sets up StringVars for the preview display."""
        self.preview_name_var = tk.StringVar(value="Name: -")
        self.preview_level_var = tk.StringVar(value="Level: -")
        self.preview_gold_var = tk.StringVar(value="Gold: -")
        self.preview_stats_vars = {
            'Stärke': tk.StringVar(value="Stärke: -"),
            'Intelligenz': tk.StringVar(value="Intelligenz: -"),
            'Glück': tk.StringVar(value="Glück: -"),
        }

    def create_widgets(self):
        self.master.title("Chronicle of the Idle Hero - Hauptmenü")

        # Introduction Text
        intro_text_content = (
            "Willkommen bei Chronicle of the Idle Hero!\n\n"
            "Wähle einen Spielstand oder erstelle einen neuen Helden. "
            "Dein Held wird automatisch Quests erledigen. Deine Aufgabe ist es, "
            "seine Ausrüstung zu verwalten und Tränke zu kaufen.\n\n"
            "ACHTUNG: Wenn dein Held stirbt, wird sein Spielstand endgültig gelöscht!"
        )
        intro_frame = ttk.LabelFrame(self, text="Spielanleitung", padding=10)
        intro_frame.pack(fill=tk.X, padx=10, pady=10)
        intro_label = ttk.Label(intro_frame, text=intro_text_content, wraplength=550, justify=tk.LEFT)
        intro_label.pack()

        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left side: Save file list
        list_frame = ttk.Frame(main_pane, padding=5)
        main_pane.add(list_frame, weight=1)
        ttk.Label(list_frame, text="Verfügbare Spielstände:", font=("Helvetica", 12)).pack(pady=5)
        self.save_listbox = tk.Listbox(list_frame)
        self.save_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.save_listbox.yview)
        self.save_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.populate_save_list()
        self.save_listbox.bind('<<ListboxSelect>>', self.on_select)

        # Right side: Character Preview
        preview_frame = ttk.LabelFrame(main_pane, text="Vorschau", padding=10)
        main_pane.add(preview_frame, weight=1)

        ttk.Label(preview_frame, textvariable=self.preview_name_var).pack(anchor=tk.W)
        ttk.Label(preview_frame, textvariable=self.preview_level_var).pack(anchor=tk.W)
        ttk.Label(preview_frame, textvariable=self.preview_gold_var).pack(anchor=tk.W, pady=(0, 10))

        for stat in ['Stärke', 'Intelligenz', 'Glück']:
            ttk.Label(preview_frame, textvariable=self.preview_stats_vars[stat]).pack(anchor=tk.W)

        # Bottom buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)

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
        """Loads character data and displays it in the preview."""
        if not self.save_listbox.curselection():
            self.load_button.config(state=tk.DISABLED)
            self.selected_save = None
            self.clear_preview()
            return

        self.load_button.config(state=tk.NORMAL)
        self.selected_save = self.save_listbox.get(self.save_listbox.curselection())

        # Load character data for preview
        char = load_game(self.selected_save)
        if char:
            self.preview_name_var.set(f"Name: {char.name} ({char.klasse})")
            self.preview_level_var.set(f"Level: {char.level}")
            self.preview_gold_var.set(f"Gold: {char.copper}")
            for stat, var in self.preview_stats_vars.items():
                var.set(f"{stat}: {char.attributes.get(stat, 0)}")
        else:
            self.clear_preview()

    def clear_preview(self):
        """Resets the preview labels to their default state."""
        self.preview_name_var.set("Name: -")
        self.preview_level_var.set("Level: -")
        self.preview_gold_var.set("Gold: -")
        for stat, var in self.preview_stats_vars.items():
            var.set(f"{stat}: -")

    def load_game(self):
        if self.selected_save and self.callbacks['load']:
            self.callbacks['load'](self.selected_save)