# highscore_gui.py
"""
Defines the GUI window for displaying high scores.
"""
import tkinter as tk
from tkinter import ttk
from highscore_manager import load_highscores
from utils import center_window, format_currency

class HighscoreWindow(tk.Toplevel):
    """A Toplevel window to display the high score list."""

    def __init__(self, parent):
        """Initializes the high score window."""
        super().__init__(parent)
        self.title("Halle der Helden")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.populate_scores()

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        center_window(self)

    def create_widgets(self):
        """Creates and places the widgets for the window."""
        container = ttk.Frame(self, padding="10")
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Define the columns for the Treeview
        columns = ("name", "klasse", "level", "copper", "best_weapon", "best_head", "best_chest")
        self.tree = ttk.Treeview(container, columns=columns, show="headings")

        # Define headings
        self.tree.heading("name", text="Name")
        self.tree.heading("klasse", text="Klasse")
        self.tree.heading("level", text="Level")
        self.tree.heading("copper", text="Gold")
        self.tree.heading("best_weapon", text="Beste Waffe")
        self.tree.heading("best_head", text="Bester Helm")
        self.tree.heading("best_chest", text="Beste Rüstung")

        # Configure column widths
        self.tree.column("name", width=120)
        self.tree.column("klasse", width=80)
        self.tree.column("level", width=50, anchor="center")
        self.tree.column("copper", width=100, anchor="e")
        self.tree.column("best_weapon", width=150)
        self.tree.column("best_head", width=150)
        self.tree.column("best_chest", width=150)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Close button
        close_button = ttk.Button(container, text="Schließen", command=self.destroy)
        close_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))

    def populate_scores(self):
        """Loads scores and inserts them into the Treeview."""
        scores = load_highscores()
        for score in scores:
            copper_formatted = format_currency(score.get("copper", 0))
            self.tree.insert("", tk.END, values=(
                score.get("name", ""),
                score.get("klasse", ""),
                score.get("level", 0),
                copper_formatted,
                score.get("best_weapon", ""),
                score.get("best_head", ""),
                score.get("best_chest", "")
            ))
