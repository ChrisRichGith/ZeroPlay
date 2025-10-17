# rpg_gui.py
"""
Defines the graphical user interface for the text-based RPG using tkinter.
"""
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random

from character import Character
from quest import Quest
from trader import Trader
from trader_gui import TraderWindow

# Liste verfügbarer Quests
AVAILABLE_QUESTS = [
    "Rette eine Prinzessin aus einem anderen Schloss",
    "Sammle 10 leere Flaschen für den Alchemisten",
    "Polere die Rüstung des Königs (ohne Bezahlung)",
    "Entwirre die Kopfhörer des Barden",
    "Finde das Rezept für ewige Jugend (und verliere es wieder)"
]

class RpgGui:
    """Manages the main GUI window of the RPG."""

    def __init__(self, root, player_name, player_class):
        """Initializes the GUI with a created character."""
        self.root = root
        self.root.title("Progress Quest 2.0 - GUI Edition")
        self.root.geometry("800x600")
        self.root.minsize(700, 550)

        self.player = Character(player_name, player_class)
        self.trader = Trader()
        self.current_quest = None
        self.is_auto_questing = False

        self._setup_string_vars()
        self.create_widgets()
        self.update_display()

    def _setup_string_vars(self):
        """Creates tkinter StringVars to link data to labels."""
        self.char_name_var = tk.StringVar()
        self.char_level_var = tk.StringVar()
        self.char_gold_var = tk.StringVar()
        self.stats_vars = {stat: tk.StringVar() for stat in ['Stärke', 'Intelligenz', 'Glück']}
        self.equipment_vars = {slot: tk.StringVar() for slot in ['Kopf', 'Brust', 'Waffe']}
        self.quest_label_var = tk.StringVar(value="Keine aktive Quest.")
        self.inventory_label_var = tk.StringVar()
        self.quest_status_var = tk.StringVar()


    def create_widgets(self):
        """Creates and places all the widgets in the window."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        left_pane = ttk.Frame(main_frame, width=300)
        left_pane.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        self._create_character_frame(left_pane)
        self._create_actions_frame(left_pane)

        right_pane = ttk.Frame(main_frame)
        right_pane.grid(row=0, column=1, sticky="nsew")
        right_pane.columnconfigure(0, weight=1)
        right_pane.rowconfigure(1, weight=1)
        self._create_equipment_frame(right_pane)
        self._create_inventory_frame(right_pane)

    def _create_character_frame(self, parent):
        char_frame = ttk.LabelFrame(parent, text="Charakterstatus", padding="10")
        char_frame.pack(fill=tk.X, pady=(0, 10))
        labels = {"Name:": self.char_name_var, "Level:": self.char_level_var, "Gold:": self.char_gold_var}
        for i, (text, var) in enumerate(labels.items()):
            ttk.Label(char_frame, text=text).grid(row=i, column=0, sticky="w")
            ttk.Label(char_frame, textvariable=var).grid(row=i, column=1, sticky="w")

        attr_frame = ttk.LabelFrame(char_frame, text="Attribute", padding="5")
        attr_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        for i, (stat, var) in enumerate(self.stats_vars.items()):
            ttk.Label(attr_frame, text=f"{stat}:").grid(row=i, column=0, sticky="w")
            ttk.Label(attr_frame, textvariable=var).grid(row=i, column=1, sticky="w", padx=5)

        # XP Progress Bar
        xp_frame = ttk.LabelFrame(char_frame, text="Erfahrung", padding="5")
        xp_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.xp_bar = ttk.Progressbar(xp_frame, orient='horizontal', mode='determinate')
        self.xp_bar.pack(fill=tk.X, expand=True)
        self.xp_label_var = tk.StringVar()
        ttk.Label(xp_frame, textvariable=self.xp_label_var, anchor="center").pack()

    def _create_actions_frame(self, parent):
        actions_frame = ttk.LabelFrame(parent, text="Aktionen", padding="10")
        actions_frame.pack(fill=tk.X)

        self.quest_button = ttk.Button(actions_frame, text="Neue Quest beginnen", command=self.start_quest)
        self.quest_button.pack(fill=tk.X, pady=5)

        self.auto_quest_button = ttk.Button(actions_frame, text="Auto-Quest starten", command=self.toggle_auto_quest)
        self.auto_quest_button.pack(fill=tk.X, pady=5)

        self.trader_button = ttk.Button(actions_frame, text="Händler besuchen", command=self.open_trader_window)
        self.trader_button.pack(fill=tk.X, pady=5)

        self.equip_button = ttk.Button(actions_frame, text="Gegenstand ausrüsten", command=self.equip_item)
        self.equip_button.pack(fill=tk.X, pady=5)

        # Quest Progress
        self.progress_bar = ttk.Progressbar(actions_frame, orient='horizontal', mode='determinate', length=200)
        self.progress_bar.pack(fill=tk.X, pady=(10, 5))
        ttk.Label(actions_frame, textvariable=self.quest_label_var, wraplength=250, justify=tk.CENTER).pack()
        ttk.Label(actions_frame, textvariable=self.quest_status_var, foreground="gray").pack()


    def _create_equipment_frame(self, parent):
        equip_frame = ttk.LabelFrame(parent, text="Ausrüstung", padding="10")
        equip_frame.grid(row=0, column=0, sticky="new")
        for i, (slot, var) in enumerate(self.equipment_vars.items()):
            ttk.Label(equip_frame, text=f"{slot}:").grid(row=i, column=0, sticky="w")
            ttk.Label(equip_frame, textvariable=var).grid(row=i, column=1, sticky="w", padx=5)

    def _create_inventory_frame(self, parent):
        self.inv_frame = ttk.LabelFrame(parent, text="Inventar", padding="10")
        self.inv_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.inv_frame.rowconfigure(0, weight=1)
        self.inv_frame.columnconfigure(0, weight=1)
        self.inventory_listbox = tk.Listbox(self.inv_frame)
        self.inventory_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(self.inv_frame, orient=tk.VERTICAL, command=self.inventory_listbox.yview)
        self.inventory_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

    def update_display(self):
        """Updates all GUI elements with the current player data."""
        self.char_name_var.set(f"{self.player.name} ({self.player.klasse})")
        self.char_level_var.set(self.player.level)
        self.char_gold_var.set(self.player.gold)
        total_stats = self.player.get_total_stats()
        for stat, var in self.stats_vars.items():
            base = self.player.attributes.get(stat, 0)
            total = total_stats.get(stat, 0)
            bonus = total - base
            var.set(f"{total} ({base} {'+' if bonus >= 0 else ''}{bonus})") if bonus != 0 else var.set(total)
        for slot, var in self.equipment_vars.items():
            item = self.player.equipment.get(slot)
            var.set(item.name if item else "Leer")

        self.inv_frame.config(text=f"Inventar ({len(self.player.inventory)}/{self.player.max_inventory_size})")
        self.inventory_listbox.delete(0, tk.END)
        for i, item in enumerate(self.player.inventory):
            self.inventory_listbox.insert(tk.END, str(item))
            if self.player.is_upgrade(item):
                self.inventory_listbox.itemconfig(i, {'bg': '#90EE90'}) # LightGreen
            else:
                self.inventory_listbox.itemconfig(i, {'bg': 'white'})

        # Update XP Bar
        self.xp_label_var.set(f"{self.player.xp} / {self.player.xp_to_next_level} XP")
        self.xp_bar['value'] = (self.player.xp / self.player.xp_to_next_level) * 100

        # Disable/Enable buttons based on state
        is_questing = self.current_quest is not None
        self.quest_button.config(state=tk.DISABLED if is_questing else tk.NORMAL)
        self.trader_button.config(state=tk.DISABLED if is_questing else tk.NORMAL)
        self.auto_quest_button.config(state=tk.DISABLED if is_questing and not self.is_auto_questing else tk.NORMAL)

        self.root.update_idletasks()

    def toggle_auto_quest(self):
        """Starts or stops the auto-questing mode."""
        self.is_auto_questing = not self.is_auto_questing
        if self.is_auto_questing:
            self.auto_quest_button.config(text="Auto-Quest stoppen")
            self.quest_status_var.set("Auto-Quest Modus aktiv...")
            self.start_quest()
        else:
            self.auto_quest_button.config(text="Auto-Quest starten")
            self.quest_status_var.set("Auto-Quest Modus gestoppt.")

    def start_quest(self):
        """Starts a new quest, either manually or via auto-quest."""
        if self.current_quest:
            if not self.is_auto_questing:
                messagebox.showwarning("Quest aktiv", "Bitte schließe erst die aktuelle Quest ab.")
            return

        if len(self.player.inventory) >= self.player.max_inventory_size:
            self.quest_status_var.set("Inventar voll! Auto-Quest gestoppt.")
            messagebox.showinfo("Inventar voll", "Dein Inventar ist voll. Besuche den Händler!")
            if self.is_auto_questing:
                self.toggle_auto_quest() # Stop auto-questing
            return

        quest_desc = random.choice(AVAILABLE_QUESTS)
        self.current_quest = Quest(quest_desc)
        self.quest_label_var.set(quest_desc)
        self.progress_bar['value'] = 0
        self.update_display() # Update button states
        self.advance_quest()

    def advance_quest(self):
        """Advances quest progress and updates the GUI."""
        if self.current_quest is None: return

        if self.current_quest.is_complete():
            gold, xp, item = self.current_quest._generate_reward()

            # Add loot and XP
            item_added = self.player.add_loot(gold, item)
            level_up_info = self.player.add_xp(xp)

            # Build messages
            loot_message = f"Loot: {gold} Gold, {xp} XP"
            if item:
                if item_added:
                    loot_message += f" und '{item.name}'"
                else:
                    loot_message += f" (aber '{item.name}' passte nicht ins Inventar!)"
            self.quest_status_var.set(loot_message)

            # Show level up message if applicable
            if level_up_info:
                level_up_summary = f"Level Up! Du bist jetzt Level {self.player.level}!\n\nAttribut-Boni:\n" + "\n".join(level_up_info)
                messagebox.showinfo("Level Aufstieg!", level_up_summary)

            self.current_quest = None
            self.quest_label_var.set("Keine aktive Quest.")
            self.progress_bar['value'] = 0

            if self.is_auto_questing:
                self.root.after(1000, self.start_quest) # Start next quest after a delay

        else:
            self.current_quest.progress += 1
            progress_percent = (self.current_quest.progress / self.current_quest.duration) * 100
            self.progress_bar['value'] = progress_percent
            self.root.after(150, self.advance_quest) # Schedule next update

        self.update_display()

    def equip_item(self):
        """Equips the selected item from the inventory."""
        selected_indices = self.inventory_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Ausrüsten", "Bitte wähle zuerst einen Gegenstand aus dem Inventar aus.")
            return
        item_index = selected_indices[0]
        self.player.equip(item_index)
        self.update_display()

    def open_trader_window(self):
        """Opens the trader interface."""
        self.trader_button.config(state=tk.DISABLED)
        TraderWindow(self.root, self.player, self.trader, on_close_callback=self.on_trader_close)

    def on_trader_close(self):
        """Callback function for when the trader window is closed."""
        self.update_display() # Refresh main GUI in case gold/inventory changed
        self.trader_button.config(state=tk.NORMAL)


def start_game_with_character_creation():
    """Handles character creation and starts the main GUI."""
    root_window = tk.Tk()
    root_window.withdraw()

    player_name = simpledialog.askstring("Charakter erstellen", "Gib den Namen deines Helden ein:", parent=root_window)
    if player_name is None: root_window.destroy(); return
    player_class = simpledialog.askstring("Charakter erstellen", "Gib die Klasse deines Helden ein:", parent=root_window)
    if player_class is None: root_window.destroy(); return

    if not player_name: player_name = "Held"
    if not player_class: player_class = "Anfänger"

    root_window.deiconify()
    app = RpgGui(root_window, player_name, player_class)
    root_window.mainloop()

if __name__ == '__main__':
    start_game_with_character_creation()